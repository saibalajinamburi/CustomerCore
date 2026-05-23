import json
import hashlib
import os
import structlog
from typing import List
from src.agent.state import AgentState
from src.rag.hybrid_retriever import get_retriever
from src.rag.graph_rag import GraphRAGEngine
from src.rag.llm_client import get_client
from src.rag.multilingual import detect_language, SUPPORTED_LANGUAGES

log = structlog.get_logger()

# Thread-safe in-memory cache for local fallback when Redis is absent
_local_semantic_cache = {}

def get_redis_client():
    """Attempt to get redis client if REDIS_URL is configured."""
    redis_url = os.environ.get("REDIS_URL", "")
    if not redis_url:
        return None
    try:
        import redis
        return redis.from_url(redis_url, decode_responses=True)
    except Exception as e:
        log.warning("redis_connection_failed_using_local_fallback", error=str(e))
        return None

def lookup_cache(tenant_id: str, body: str) -> dict | None:
    """Look up ticket resolution in Redis semantic cache or local fallback."""
    key_hash = hashlib.sha256(f"{tenant_id}:{body.strip()}".encode("utf-8")).hexdigest()
    cache_key = f"cc:semcache:{key_hash}"
    
    redis_client = get_redis_client()
    if redis_client:
        try:
            cached_val = redis_client.get(cache_key)
            if cached_val:
                log.info("semantic_cache_hit_redis", tenant_id=tenant_id)
                return json.loads(cached_val)
        except Exception as e:
            log.warning("redis_lookup_failed", error=str(e))
            
    # Fallback to local in-memory dict
    if cache_key in _local_semantic_cache:
        log.info("semantic_cache_hit_local", tenant_id=tenant_id)
        return _local_semantic_cache[cache_key]
        
    return None

def store_cache(tenant_id: str, body: str, data: dict):
    """Store ticket resolution in Redis semantic cache or local fallback."""
    key_hash = hashlib.sha256(f"{tenant_id}:{body.strip()}".encode("utf-8")).hexdigest()
    cache_key = f"cc:semcache:{key_hash}"
    
    redis_client = get_redis_client()
    if redis_client:
        try:
            redis_client.setex(cache_key, 3600 * 24, json.dumps(data)) # 24 hour TTL
            log.info("semantic_cache_stored_redis", tenant_id=tenant_id)
            return
        except Exception as e:
            log.warning("redis_store_failed", error=str(e))
            
    # Fallback to local in-memory dict
    _local_semantic_cache[cache_key] = data
    log.info("semantic_cache_stored_locally", tenant_id=tenant_id)

def rag_agent_node(state: AgentState) -> AgentState:
    ticket = state["ticket"]
    body = ticket["body"]
    tenant_id = ticket["tenant_id"]
    
    models_used: List[str] = state.get("models_used") or []
    
    # 1. Check Redis / Local Semantic Cache first
    cached_result = lookup_cache(tenant_id, body)
    if cached_result:
        models_used.append("redis-semantic-cache-v1")
        return {
            **state,
            "summary": cached_result["summary"],
            "suggested_resolution": cached_result["suggested_resolution"],
            "kb_citations": cached_result["kb_citations"],
            "current_step": "rag_agent",
            "models_used": models_used,
        }
        
    # 2. Cache Miss: Run Hybrid Vector + Graph-RAG Retrieval
    log.info("semantic_cache_miss_running_graph_rag", tenant_id=tenant_id)
    retriever = get_retriever()
    engine = GraphRAGEngine(retriever=retriever)
    
    # Run Graph-RAG query
    rag_result = engine.query(
        tenant_id=tenant_id,
        question=body,
        k=5,
        include_sql=True
    )
    
    # 3. Detect ticket language
    lang = detect_language(body)
    lang_display = SUPPORTED_LANGUAGES.get(lang, "English")
    
    # 4. Invoke cloud LLM via LiteLLM client wrapper
    client = get_client()
    
    system_prompt = (
        "You are an expert enterprise support triage agent. Your job is to analyze the support ticket "
        "and generate a short summary, a detailed suggested resolution, and a list of knowledge base citation IDs.\n\n"
        "You are provided with rich tenant context and similar past resolved tickets from our Graph-RAG engine.\n\n"
        "=== CRITICAL INSTRUCTIONS ===\n"
        f"1. The ticket is written in {lang_display}. You MUST output the 'summary' and 'suggested_resolution' in {lang_display}.\n"
        "2. The summary must be a single concise sentence summarizing the core issue (max 300 characters).\n"
        "3. The suggested resolution must be highly specific, technical, and actionable (max 1000 characters).\n"
        "4. Output a list of knowledge base citation IDs. Valid IDs MUST start with 'KB-', 'TICKET-', or 'DOC-'. "
        "Extract these from the provided similar past tickets or tenant profile where applicable. If none exist, output an empty list.\n"
        "5. You MUST return your response as a strict JSON object with exactly three keys: 'summary', 'suggested_resolution', and 'kb_citations'. "
        "Do not include any markdown framing, backticks, or text before/after the JSON."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{rag_result.combined_context}\n\nTicket Body: {body}"}
    ]
    
    try:
        response = client.call_cloud(messages=messages, temperature=0.1)
        if response.success:
            models_used.append(response.model_used)
            # Parse the JSON response
            clean_content = response.content.strip()
            if clean_content.startswith("```json"):
                clean_content = clean_content.split("```json")[1].split("```")[0].strip()
            elif clean_content.startswith("```"):
                clean_content = clean_content.split("```")[1].split("```")[0].strip()
                
            parsed = json.loads(clean_content)
            summary = parsed.get("summary", "")
            suggested_resolution = parsed.get("suggested_resolution", "")
            kb_citations = parsed.get("kb_citations", [])
            
            # Clean and validate citations
            valid_citations = []
            for citation in kb_citations:
                citation_str = str(citation).upper().strip()
                if citation_str.startswith(("KB-", "TICKET-", "DOC-")):
                    valid_citations.append(citation_str)
                else:
                    # Fix formatting if possible
                    if citation_str.isalnum():
                        valid_citations.append(f"KB-{citation_str}")
            
            # Ensure they are non-empty and satisfy length constraints
            if not summary:
                summary = body[:100] + "..." if len(body) > 100 else body
            if not suggested_resolution:
                suggested_resolution = "Our team is investigating this issue. We will update you shortly."
                
            # Store in cache
            result_data = {
                "summary": summary,
                "suggested_resolution": suggested_resolution,
                "kb_citations": valid_citations,
            }
            store_cache(tenant_id, body, result_data)
            
            log.info("rag_agent_completed_successfully", model=response.model_used)
            return {
                **state,
                "summary": summary,
                "suggested_resolution": suggested_resolution,
                "kb_citations": valid_citations,
                "current_step": "rag_agent",
                "models_used": models_used,
            }
            
    except Exception as e:
        log.error("rag_agent_llm_failed_using_fallback", error=str(e))
        
    # Heuristic fallback if LLM call or parsing fails
    summary = body[:150] + "..." if len(body) > 150 else body
    suggested_resolution = (
        f"A support agent has been notified of this ticket. "
        f"Language detected: {lang_display}. Category classified: {state.get('category', 'unknown')}."
    )
    kb_citations = ["KB-FALLBACK"]
    models_used.append("heuristic-rag-fallback-v1.0")
    
    return {
        **state,
        "summary": summary,
        "suggested_resolution": suggested_resolution,
        "kb_citations": kb_citations,
        "current_step": "rag_agent_fallback",
        "models_used": models_used,
    }
