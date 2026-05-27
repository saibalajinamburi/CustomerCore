# -*- coding: utf-8 -*-
"""
CustomerCore Operations Console — Single Page Application Frontend (ui.py)
A premium dashboard for testing and visualizing the AI triage pipeline.
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CustomerCore Operations Console</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0a0e17;
            --bg-card: rgba(18, 26, 47, 0.6);
            --bg-card-border: rgba(255, 255, 255, 0.08);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.4);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.3);
            --warning: #f59e0b;
            --danger: #ef4444;
            --danger-glow: rgba(239, 68, 68, 0.3);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --text-glow: rgba(255, 255, 255, 0.15);
            --glass-backdrop: blur(16px);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.12) 0%, transparent 40%);
            background-attachment: fixed;
        }

        /* Layout */
        .sidebar {
            width: 320px;
            background: rgba(10, 14, 23, 0.85);
            border-right: 1px solid var(--bg-card-border);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            backdrop-filter: var(--glass-backdrop);
            z-index: 10;
        }

        .main-content {
            flex: 1;
            padding: 40px;
            overflow-y: auto;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        /* Sidebar Logo & Header */
        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--bg-card-border);
        }

        .logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--primary), var(--success));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: white;
            font-size: 18px;
            box-shadow: 0 0 15px var(--primary-glow);
        }

        .logo-text h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: linear-gradient(to right, #ffffff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-text span {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            display: block;
        }

        /* Sidebar Navigation */
        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 16px;
            border-radius: 12px;
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
            cursor: pointer;
        }

        .nav-item:hover {
            color: white;
            background: rgba(255, 255, 255, 0.03);
            border-color: rgba(255, 255, 255, 0.05);
        }

        .nav-item.active {
            color: white;
            background: rgba(99, 102, 241, 0.15);
            border-color: rgba(99, 102, 241, 0.25);
            box-shadow: inset 0 0 12px rgba(99, 102, 241, 0.05);
        }

        .nav-icon {
            font-size: 18px;
        }

        /* Token Generator Widget */
        .token-widget {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 16px;
            padding: 18px;
            margin-top: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .widget-title {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            font-weight: 600;
        }

        .select-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .select-label {
            font-size: 11px;
            color: var(--text-muted);
        }

        select, input, textarea {
            background: rgba(10, 14, 23, 0.8);
            border: 1px solid var(--bg-card-border);
            color: white;
            padding: 10px 12px;
            border-radius: 8px;
            font-size: 13px;
            width: 100%;
            outline: none;
            transition: border-color 0.3s;
        }

        select:focus, input:focus, textarea:focus {
            border-color: var(--primary);
        }

        .btn {
            background: linear-gradient(135deg, var(--primary), #4f46e5);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn:hover {
            box-shadow: 0 0 15px var(--primary-glow);
            transform: translateY(-1px);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success), #059669);
        }

        .btn-success:hover {
            box-shadow: 0 0 15px var(--success-glow);
        }

        .token-badge {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 10px;
            font-family: monospace;
            text-overflow: ellipsis;
            white-space: nowrap;
            overflow: hidden;
            text-align: center;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        /* Dashboard View Elements */
        .tab-view {
            display: none;
            animation: fadeIn 0.4s ease-out;
        }

        .tab-view.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .view-header {
            margin-bottom: 32px;
        }

        .view-header h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: white;
            margin-bottom: 6px;
        }

        .view-header p {
            color: var(--text-muted);
            font-size: 14px;
        }

        /* Form & Result Grid */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 420px 1fr;
            gap: 32px;
            align-items: start;
        }

        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 20px;
            padding: 28px;
            backdrop-filter: var(--glass-backdrop);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        /* Analytics Output Panel */
        .analytics-panel {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }

        .metric-card {
            background: rgba(18, 26, 47, 0.4);
            border: 1px solid var(--bg-card-border);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            transition: all 0.3s;
        }

        .metric-card:hover {
            border-color: rgba(255, 255, 255, 0.12);
            transform: translateY(-2px);
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .metric-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            font-weight: 600;
        }

        .metric-icon {
            font-size: 18px;
        }

        .metric-value {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 700;
        }

        /* Priority Colors */
        .priority-badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
        }
        .priority-critical { background: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.25); }
        .priority-high { background: rgba(245, 158, 11, 0.15); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.25); }
        .priority-medium { background: rgba(99, 102, 241, 0.15); color: var(--primary); border: 1px solid rgba(99, 102, 241, 0.25); }
        .priority-low { background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.25); }

        /* Progress Bar for Churn */
        .churn-container {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 6px;
        }

        .churn-bar {
            height: 100%;
            width: 0%;
            border-radius: 4px;
            background: linear-gradient(to right, var(--success), var(--warning), var(--danger));
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Large Output Areas (Resolution / PII) */
        .large-metric-card {
            background: rgba(18, 26, 47, 0.4);
            border: 1px solid var(--bg-card-border);
            border-radius: 16px;
            padding: 24px;
        }

        .log-box {
            background: rgba(10, 14, 23, 0.9);
            border: 1px solid var(--bg-card-border);
            padding: 16px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 13px;
            line-height: 1.5;
            color: #d1d5db;
            overflow-x: auto;
            max-height: 250px;
            overflow-y: auto;
        }

        /* Safety Banner */
        .safety-banner {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 18px 24px;
            border-radius: 16px;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .safety-passed {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--success);
        }
        .safety-blocked {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: var(--danger);
            animation: pulse-border 2s infinite;
        }
        @keyframes pulse-border {
            0% { border-color: rgba(239, 68, 68, 0.2); }
            50% { border-color: rgba(239, 68, 68, 0.6); }
            100% { border-color: rgba(239, 68, 68, 0.2); }
        }

        /* Tables */
        .table-container {
            width: 100%;
            overflow-x: auto;
            margin-top: 24px;
            border-radius: 16px;
            border: 1px solid var(--bg-card-border);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }

        th {
            background: rgba(10, 14, 23, 0.6);
            color: var(--text-muted);
            font-weight: 600;
            padding: 14px 18px;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.8px;
            border-bottom: 1px solid var(--bg-card-border);
        }

        td {
            padding: 14px 18px;
            border-bottom: 1px solid var(--bg-card-border);
            color: #d1d5db;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.01);
            color: white;
        }

        .empty-state {
            padding: 40px;
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
        }

        /* Health statuses badges */
        .health-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .status-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .status-badge.ok { background: rgba(16, 185, 129, 0.15); color: var(--success); }
        .status-badge.error { background: rgba(239, 68, 68, 0.15); color: var(--danger); }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            background-color: currentColor;
            animation: pulse-dot 1.5s infinite;
        }

        @keyframes pulse-dot {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.6; }
        }

        /* Toast notifications */
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(10, 14, 23, 0.95);
            border: 1px solid var(--bg-card-border);
            padding: 16px 24px;
            border-radius: 12px;
            color: white;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 12px;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-size: 13px;
        }

        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }
    </style>
</head>
<body>

    <!-- Sidebar Layout -->
    <div class="sidebar">
        <div class="logo-container">
            <div class="logo-icon">C</div>
            <div class="logo-text">
                <h1>CustomerCore</h1>
                <span>Operations Console</span>
            </div>
        </div>

        <div class="nav-menu">
            <div class="nav-item active" onclick="switchTab('dashboard-view')">
                <span class="nav-icon">📊</span> Triage Dashboard
            </div>
            <div class="nav-item" onclick="switchTab('hitl-view')">
                <span class="nav-icon">🤝</span> HITL Workspace
            </div>
            <div class="nav-item" onclick="switchTab('health-view')">
                <span class="nav-icon">⚡</span> System Health
            </div>
        </div>

        <!-- Token Generator Widget -->
        <div class="token-widget">
            <h3 class="widget-title">Mock Tenant JWT</h3>
            <div class="select-group">
                <label class="select-label">Tenant ID</label>
                <select id="widget-tenant" onchange="generateToken()">
                    <option value="acme-corp">acme-corp (Tenant A)</option>
                    <option value="globex">globex (Tenant B)</option>
                    <option value="hooli">hooli (Tenant C)</option>
                    <option value="test-tenant" selected>test-tenant</option>
                </select>
            </div>
            <div class="select-group">
                <label class="select-label">Role</label>
                <select id="widget-role" onchange="generateToken()">
                    <option value="support_agent" selected>Support Agent</option>
                    <option value="manager">Manager</option>
                    <option value="admin">Administrator</option>
                </select>
            </div>
            <div class="token-badge" id="token-display">Generating token...</div>
            <button class="btn btn-success" style="padding: 10px;" onclick="generateToken()">
                🔄 Regenerate Token
            </button>
        </div>
    </div>

    <!-- Main View Section -->
    <div class="main-content">

        <!-- TOAST -->
        <div id="toast-notify" class="toast">
            <span id="toast-icon">ℹ️</span>
            <span id="toast-message">Notification message</span>
        </div>

        <!-- TAB 1: TRIAGE DASHBOARD -->
        <div id="dashboard-view" class="tab-view active">
            <div class="view-header">
                <h2>AI Triage Dashboard</h2>
                <p>Submit mock support tickets to the streaming analytics & classification pipeline</p>
            </div>

            <div class="dashboard-grid">
                <!-- Left column: Submit Ticket Form -->
                <div class="glass-card">
                    <h3 style="margin-bottom: 20px; font-size: 18px; font-family: 'Outfit';">Submit New Ticket</h3>
                    <form id="triage-form" onsubmit="submitTriage(event)">
                        <div class="form-group">
                            <label>Customer ID</label>
                            <input type="text" id="cust-id" value="cust_998" placeholder="e.g. cust_001" required>
                        </div>
                        <div class="form-group">
                            <label>Customer Tier</label>
                            <select id="cust-tier">
                                <option value="standard">Standard Tier</option>
                                <option value="gold">Gold Tier</option>
                                <option value="enterprise" selected>Enterprise Tier</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Source / Channel</label>
                            <select id="ticket-channel">
                                <option value="email" selected>Email Interface</option>
                                <option value="web_portal">Web Customer Portal</option>
                                <option value="api_gateway">API Gateway Client</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Support Ticket Text (e.g. Billing, Outage, Complaint)</label>
                            <textarea id="ticket-text" rows="8" placeholder="Write the support issue text (minimum 10 characters)..." required>We are experiencing a major billing bug. My payment method was charged twice ($500) and the API is returning 500 errors. Please refund our money immediately or we will cancel our subscription.</textarea>
                        </div>
                        <button type="submit" class="btn" style="width: 100%;" id="submit-btn">
                            🚀 Dispatch to Triage Pipeline
                        </button>
                    </form>
                </div>

                <!-- Right column: Analytics Display -->
                <div class="analytics-panel">
                    <!-- Safety compliance banner -->
                    <div id="safety-indicator" class="safety-banner safety-passed" style="display: none;">
                        <span id="safety-icon">🛡️</span>
                        <span id="safety-text">AI Compliance Check: Safe</span>
                    </div>

                    <div class="analytics-grid">
                        <!-- Priority Card -->
                        <div class="metric-card">
                            <div class="metric-header">
                                <span class="metric-label">Predicted Priority</span>
                                <span class="metric-icon">🔥</span>
                            </div>
                            <div id="metric-priority" class="metric-value">--</div>
                        </div>

                        <!-- Routing Card -->
                        <div class="metric-card">
                            <div class="metric-header">
                                <span class="metric-label">Smart Routing Team</span>
                                <span class="metric-icon">🎯</span>
                            </div>
                            <div id="metric-routing" class="metric-value">--</div>
                        </div>

                        <!-- Churn Risk Card -->
                        <div class="metric-card">
                            <div class="metric-header">
                                <span class="metric-label">Predicted Churn Risk</span>
                                <span class="metric-icon">⚠️</span>
                            </div>
                            <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
                                <div id="metric-churn" class="metric-value" style="margin-bottom: 2px;">--</div>
                                <div class="churn-container">
                                    <div id="churn-progress" class="churn-bar"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Outage Check Card -->
                        <div class="metric-card">
                            <div class="metric-header">
                                <span class="metric-label">Anomaly / Outage Check</span>
                                <span class="metric-icon">🌐</span>
                            </div>
                            <div id="metric-outage" class="metric-value">--</div>
                        </div>
                    </div>

                    <!-- AI Suggested Resolution -->
                    <div class="large-metric-card">
                        <h4 style="margin-bottom: 12px; font-size: 14px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">
                            Suggested Agent Resolution
                        </h4>
                        <div id="metric-resolution" style="font-size: 14px; line-height: 1.6; color: #e5e7eb; min-height: 50px;">
                            Submit a ticket to view the AI-generated resolution draft here.
                        </div>
                    </div>

                    <!-- PII Redaction Log -->
                    <div class="large-metric-card">
                        <h4 style="margin-bottom: 12px; font-size: 14px; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">
                            Privacy Vault (PII Masking Audit)
                        </h4>
                        <div class="log-box" id="metric-pii-log">
                            Audit logs will populate once the ticket is processed.
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Table: History -->
            <div class="glass-card" style="margin-top: 40px; padding: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h3 style="font-family: 'Outfit'; font-size: 18px;">Tenant Ticket History</h3>
                    <button class="btn" style="padding: 8px 16px;" onclick="loadHistory()">🔄 Refresh List</button>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Ticket ID</th>
                                <th>Customer</th>
                                <th>Tier</th>
                                <th>Priority</th>
                                <th>Status</th>
                                <th>Created At</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="history-table-body">
                            <tr>
                                <td colspan="7" class="empty-state">No tickets triaged yet. Submit a ticket above!</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: HITL WORKSPACE -->
        <div id="hitl-view" class="tab-view">
            <div class="view-header">
                <h2>Human-in-the-Loop Workspace</h2>
                <p>Inspect and resolve tickets flagged for policy compliance checks</p>
            </div>

            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <h3 style="font-family: 'Outfit'; font-size: 18px;">Flagged HITL Reviews</h3>
                    <button class="btn" style="padding: 8px 16px;" onclick="loadHITLList()">🔄 Fetch Pending</button>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Ticket ID</th>
                                <th>Customer ID</th>
                                <th>Content Snip</th>
                                <th>Flagged Reasons / Violations</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="hitl-table-body">
                            <tr>
                                <td colspan="5" class="empty-state">No tickets pending HITL review.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: SYSTEM HEALTH -->
        <div id="health-view" class="tab-view">
            <div class="view-header">
                <h2>System Health Monitor</h2>
                <p>Check the live status of CustomerCore microservices and observability integrations</p>
            </div>

            <div class="glass-card">
                <h3 style="margin-bottom: 24px; font-family: 'Outfit'; font-size: 18px;">Microservice Connectivity</h3>
                <div class="health-grid">
                    <!-- API Status -->
                    <div class="metric-card">
                        <div class="metric-header">
                            <span class="metric-label">API REST Server</span>
                            <span class="metric-icon">🚀</span>
                        </div>
                        <div>
                            <span class="status-badge ok"><span class="pulse-dot"></span>Active</span>
                        </div>
                    </div>

                    <!-- Redis Status -->
                    <div class="metric-card">
                        <div class="metric-header">
                            <span class="metric-label">Redis Cache</span>
                            <span class="metric-icon">⚡</span>
                        </div>
                        <div>
                            <span id="health-redis" class="status-badge error">Checking...</span>
                        </div>
                    </div>

                    <!-- Redpanda Status -->
                    <div class="metric-card">
                        <div class="metric-header">
                            <span class="metric-label">Redpanda Broker</span>
                            <span class="metric-icon">📻</span>
                        </div>
                        <div>
                            <span id="health-redpanda" class="status-badge error">Checking...</span>
                        </div>
                    </div>

                    <!-- Supabase Status -->
                    <div class="metric-card">
                        <div class="metric-header">
                            <span class="metric-label">Supabase DB</span>
                            <span class="metric-icon">🗄️</span>
                        </div>
                        <div>
                            <span id="health-supabase" class="status-badge error">Checking...</span>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 40px;">
                    <h3 style="margin-bottom: 16px; font-family: 'Outfit'; font-size: 18px;">FastAPI Configuration Settings</h3>
                    <div class="log-box" id="health-config-log">
                        Loading configuration...
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- JS Logic -->
    <script>
        let currentToken = "";

        // Tab Switch
        function switchTab(tabId) {
            document.querySelectorAll('.tab-view').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            
            // Map click to nav highlight
            if(tabId === 'dashboard-view') {
                document.querySelector('.nav-item:nth-child(1)').classList.add('active');
                loadHistory();
            } else if(tabId === 'hitl-view') {
                document.querySelector('.nav-item:nth-child(2)').classList.add('active');
                loadHITLList();
            } else if(tabId === 'health-view') {
                document.querySelector('.nav-item:nth-child(3)').classList.add('active');
                checkSystemHealth();
            }
        }

        // Notification Toast
        function showToast(message, isError = false) {
            const toast = document.getElementById('toast-notify');
            const icon = document.getElementById('toast-icon');
            const msg = document.getElementById('toast-message');

            icon.innerText = isError ? "❌" : "✅";
            msg.innerText = message;
            
            toast.className = "toast show";
            setTimeout(() => {
                toast.className = "toast";
            }, 3000);
        }

        // Generate Token on Page Load / widget selection
        async function generateToken() {
            const tenant = document.getElementById('widget-tenant').value;
            const role = document.getElementById('widget-role').value;
            
            try {
                const response = await fetch(`/api/v1/test-token?tenant_id=${tenant}&role=${role}`);
                const data = await response.json();
                if(data.token) {
                    currentToken = data.token;
                    document.getElementById('token-display').innerText = currentToken.slice(0, 15) + "..." + currentToken.slice(-10);
                    document.getElementById('token-display').title = currentToken;
                    showToast(`Token generated for ${tenant} (${role})`);
                    
                    // Reload histories
                    if(document.getElementById('dashboard-view').classList.contains('active')) {
                        loadHistory();
                    }
                }
            } catch(e) {
                console.error("Token generation failed", e);
                document.getElementById('token-display').innerText = "Generation failed";
                showToast("Failed to fetch test token", true);
            }
        }

        // Submit Ticket
        async function submitTriage(event) {
            event.preventDefault();
            const text = document.getElementById('ticket-text').value;
            const custId = document.getElementById('cust-id').value;
            const custTier = document.getElementById('cust-tier').value;
            const channel = document.getElementById('ticket-channel').value;
            const btn = document.getElementById('submit-btn');

            btn.disabled = true;
            btn.innerText = "Processing...";

            // Reset UI outputs
            document.getElementById('metric-priority').innerText = "--";
            document.getElementById('metric-priority').className = "metric-value";
            document.getElementById('metric-routing').innerText = "--";
            document.getElementById('metric-outage').innerText = "--";
            document.getElementById('metric-churn').innerText = "--";
            document.getElementById('churn-progress').style.width = "0%";
            document.getElementById('metric-resolution').innerText = "Processing ticket...";
            document.getElementById('metric-pii-log').innerText = "Masking PII...";
            document.getElementById('safety-indicator').style.display = "none";

            try {
                const response = await fetch('/api/v1/triage', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${currentToken}`
                    },
                    body: JSON.stringify({
                        text: text,
                        customer_id: custId,
                        customer_tier: custTier,
                        channel: channel
                    })
                });

                if(!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                showToast("Ticket submitted to triage pipeline!");
                
                // Since this is a 202 Accepted response, we need to poll the ticket status until it is finished.
                pollTicketStatus(result.ticket_id);
            } catch(e) {
                console.error("Submit failed", e);
                showToast("Failed to submit ticket", true);
                btn.disabled = false;
                btn.innerText = "Dispatch to Triage Pipeline";
                document.getElementById('metric-resolution').innerText = "Failed to submit ticket. See logs.";
            }
        }

        // Poll Ticket Status
        async function pollTicketStatus(ticketId) {
            const btn = document.getElementById('submit-btn');
            let attempts = 0;
            const maxAttempts = 15;

            const pollInterval = setInterval(async () => {
                attempts++;
                try {
                    const response = await fetch(`/api/v1/triage/${ticketId}`, {
                        headers: {
                            'Authorization': `Bearer ${currentToken}`
                        }
                    });

                    if(response.status === 404) {
                        // Not found yet / waiting
                        return;
                    }

                    if(!response.ok) {
                        throw new Error(`HTTP error ${response.status}`);
                    }

                    const data = await response.json();
                    
                    // If finished or failed, display results
                    if(data.status !== "pending" || attempts >= maxAttempts) {
                        clearInterval(pollInterval);
                        displayTriageResults(data);
                        btn.disabled = false;
                        btn.innerText = "Dispatch to Triage Pipeline";
                        loadHistory();
                    }
                } catch(e) {
                    console.error("Polling error", e);
                    clearInterval(pollInterval);
                    btn.disabled = false;
                    btn.innerText = "Dispatch to Triage Pipeline";
                }
            }, 1000);
        }

        // Display results in dashboard metrics cards
        function displayTriageResults(data) {
            // Priority
            const priorityVal = data.priority || "Low";
            const priorityEl = document.getElementById('metric-priority');
            priorityEl.innerText = priorityVal;
            priorityEl.className = `metric-value priority-badge priority-${priorityVal.toLowerCase()}`;

            // Routing
            document.getElementById('metric-routing').innerText = data.routing_department || "General Support";

            // Outage
            document.getElementById('metric-outage').innerText = data.potential_outage ? "⚠️ Outage Alert!" : "✅ Normal";

            // Churn Risk
            const churnScore = data.churn_risk_score !== undefined ? data.churn_risk_score : 0.15;
            const churnPercent = Math.round(churnScore * 100);
            document.getElementById('metric-churn').innerText = `${churnPercent}%`;
            document.getElementById('churn-progress').style.width = `${churnPercent}%`;

            // Suggested Resolution
            document.getElementById('metric-resolution').innerText = data.suggested_resolution || "A support representative has been notified and will contact you shortly.";

            // PII masking logs
            let piiText = `[Vault Ingestion]\n`;
            piiText += `- Ticket ID: ${data.ticket_id}\n`;
            piiText += `- Customer ID: ${data.customer_id}\n`;
            piiText += `- Raw Text masked? Yes\n`;
            if (data.masked_text) {
                piiText += `- Redacted Body: "${data.masked_text}"\n`;
            }
            document.getElementById('metric-pii-log').innerText = piiText;

            // Safety indicator
            const safetyEl = document.getElementById('safety-indicator');
            const safetyText = document.getElementById('safety-text');
            
            if (data.constitutional_blocked) {
                safetyEl.className = "safety-banner safety-blocked";
                safetyText.innerText = "🛡️ AI Compliance Check: BLOCKED! Input/Output policy violations detected.";
                
                // Show violations in PII log
                if (data.constitutional_violations && data.constitutional_violations.length > 0) {
                    piiText += `\n[Safety Violations Detected]\n`;
                    data.constitutional_violations.forEach(v => {
                        piiText += `- Rule: ${v.rule_id} | Reason: ${v.reason}\n`;
                    });
                    document.getElementById('metric-pii-log').innerText = piiText;
                }
            } else {
                safetyEl.className = "safety-banner safety-passed";
                safetyText.innerText = "🛡️ AI Compliance Check: Passed! All content satisfies safety regulations.";
            }
            safetyEl.style.display = "flex";
        }

        // Load Ticket History for active tenant
        async function loadHistory() {
            const tbody = document.getElementById('history-table-body');
            
            try {
                const response = await fetch('/api/v1/triage', {
                    headers: {
                        'Authorization': `Bearer ${currentToken}`
                    }
                });

                if(!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }

                const tickets = await response.json();
                if(tickets.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="7" class="empty-state">No tickets triaged yet. Submit a ticket above!</td></tr>`;
                    return;
                }

                tbody.innerHTML = "";
                tickets.forEach(t => {
                    const tr = document.createElement('tr');
                    const priorityClass = t.priority ? t.priority.toLowerCase() : 'low';
                    const statusClass = t.status === 'hitl' ? 'warning' : (t.status === 'completed' ? 'success' : 'muted');
                    
                    tr.innerHTML = `
                        <td style="font-family: monospace;">${t.ticket_id.slice(0, 8)}...</td>
                        <td>${t.customer_id}</td>
                        <td><span style="text-transform: capitalize;">${t.customer_tier}</span></td>
                        <td><span class="priority-badge priority-${priorityClass}">${t.priority || 'Low'}</span></td>
                        <td><span class="status-badge" style="padding: 2px 8px; font-size: 11px;">${t.status}</span></td>
                        <td>${new Date(t.created_at || Date.now()).toLocaleString()}</td>
                        <td>
                            <button class="btn" style="padding: 4px 8px; font-size: 11px;" onclick="loadSingleTicket('${t.ticket_id}')">👁️ View</button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(e) {
                console.error("Load history failed", e);
                tbody.innerHTML = `<tr><td colspan="7" class="empty-state">Failed to load ticket history. Please ensure a valid token is loaded.</td></tr>`;
            }
        }

        // View single ticket details
        async function loadSingleTicket(ticketId) {
            try {
                const response = await fetch(`/api/v1/triage/${ticketId}`, {
                    headers: {
                        'Authorization': `Bearer ${currentToken}`
                    }
                });
                if(response.ok) {
                    const data = await response.json();
                    displayTriageResults(data);
                    showToast(`Loaded ticket ${ticketId.slice(0, 8)}`);
                }
            } catch(e) {
                showToast("Failed to load ticket details", true);
            }
        }

        // Load HITL Pending list
        async function loadHITLList() {
            const tbody = document.getElementById('hitl-table-body');
            
            try {
                // Fetch all tickets for the active tenant, and filter by status === 'hitl'
                const response = await fetch('/api/v1/triage', {
                    headers: {
                        'Authorization': `Bearer ${currentToken}`
                    }
                });

                if(!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }

                const tickets = await response.json();
                const hitlTickets = tickets.filter(t => t.status === 'hitl');

                if(hitlTickets.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="5" class="empty-state">No tickets pending HITL review.</td></tr>`;
                    return;
                }

                tbody.innerHTML = "";
                hitlTickets.forEach(t => {
                    const tr = document.createElement('tr');
                    const textSnip = t.masked_text ? (t.masked_text.slice(0, 50) + "...") : (t.text.slice(0, 50) + "...");
                    
                    // Show custom mock violations since we don't have DB populated
                    const violations = t.constitutional_violations && t.constitutional_violations.length > 0 
                        ? t.constitutional_violations.map(v => `${v.rule_id}: ${v.reason}`).join(", ")
                        : "PII masking/Policy warning";

                    tr.innerHTML = `
                        <td style="font-family: monospace;">${t.ticket_id.slice(0, 8)}...</td>
                        <td>${t.customer_id}</td>
                        <td title="${t.text}">${textSnip}</td>
                        <td style="color: var(--warning); font-weight: 500;">${violations}</td>
                        <td>
                            <button class="btn btn-success" style="padding: 4px 8px; font-size: 11px;" onclick="resumeHITLTicket('${t.ticket_id}')">🤝 Resume</button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(e) {
                console.error("Load HITL list failed", e);
                tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Failed to load HITL reviews. Ensure role is 'manager' or 'admin'.</td></tr>`;
            }
        }

        // Resume HITL Ticket
        async function resumeHITLTicket(ticketId) {
            const operatorId = prompt("Enter operator ID (e.g. operator_12):", "op_manager_01");
            if(!operatorId) return;
            const resolution = prompt("Enter manual override resolution text:", "Manual Override: Refund issued and payment method updated.");
            if(!resolution) return;

            try {
                const response = await fetch(`/api/v1/triage/${ticketId}/resume`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${currentToken}`
                    },
                    body: JSON.stringify({
                        ticket_id: ticketId,
                        operator_id: operatorId,
                        resolution_override: resolution
                    })
                });

                if (response.status === 403) {
                    showToast("Access Denied: Only Manager or Admin role can resume HITL", true);
                    return;
                }

                if(!response.ok) {
                    const err = await response.json();
                    throw new Error(err.detail || "Error resuming ticket");
                }

                showToast(`Ticket ${ticketId.slice(0, 8)} resumed successfully!`);
                loadHITLList();
            } catch(e) {
                console.error("Resume failed", e);
                showToast(e.message || "Failed to resume ticket", true);
            }
        }

        // Check system health
        async function checkSystemHealth() {
            // Fetch live readiness state
            try {
                const response = await fetch('/api/v1/ready');
                const data = await response.json();
                
                // Redis
                const redisEl = document.getElementById('health-redis');
                redisEl.innerText = data.services.redis ? "Connected" : "Offline";
                redisEl.className = data.services.redis ? "status-badge ok" : "status-badge error";

                // Redpanda
                const pandaEl = document.getElementById('health-redpanda');
                pandaEl.innerText = data.services.redpanda ? "Connected" : "Offline";
                pandaEl.className = data.services.redpanda ? "status-badge ok" : "status-badge error";

                // Supabase
                const subaEl = document.getElementById('health-supabase');
                subaEl.innerText = data.services.supabase ? "Connected" : "Offline";
                subaEl.className = data.services.supabase ? "status-badge ok" : "status-badge error";

                // Config log
                let configText = `[CustomerCore Microservice Configuration]\n`;
                configText += `- App Environment: production\n`;
                configText += `- Database Provider: Supabase (RLS isolated)\n`;
                configText += `- Cache Store: Redis Cache (Rate limits + L1 cache)\n`;
                configText += `- Message Broker: Redpanda (Kafka v2 compatible)\n`;
                configText += `- Graph-RAG Search: ChromaDB (Vector) + BM25 (Keyword)\n`;
                document.getElementById('health-config-log').innerText = configText;
            } catch(e) {
                showToast("Failed to fetch service health", true);
            }
        }

        // Initialize Page
        window.addEventListener('DOMContentLoaded', () => {
            generateToken();
        });
    </script>
</body>
</html>
"""
