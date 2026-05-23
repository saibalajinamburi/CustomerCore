import pytest
import os

@pytest.fixture(autouse=True)
def set_test_env_vars():
    os.environ["APP_ENV"] = "test"
    os.environ["LITELLM_MASTER_KEY"] = "sk-test"
    yield
