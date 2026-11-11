"""
llm_config.py - LLM Provider Configuration and Client Factory.

Loads API credentials from environment variables using python-dotenv.
Supports standard OpenAI models as well as any OpenAI-compatible provider
(Azure, Ollama, OpenRouter, vLLM, etc.).

Safety & Graceful Degradation:
  - Validates API key presence before attempting to build LLM clients.
  - Never logs or exposes credentials.
  - Raises MissingApiKeyError with clear actionable guidance when credentials
    are absent, allowing the pipeline to degrade gracefully to deterministic scanning.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

# Load environment variables from .env if present
load_dotenv()

PLACEHOLDER_KEYS = {
    "your_openai_api_key_here",
    "placeholder",
    "none",
    "sk-placeholder",
}


class MissingApiKeyError(RuntimeError):
    """Raised when required LLM credentials are not configured."""


def get_configured_base_url() -> str | None:
    """
    Return the configured base URL for OpenAI-compatible or local Ollama endpoints.
    Supports OPENAI_BASE_URL, OPENAI_API_BASE, and OLLAMA_BASE_URL.
    """
    return (
        os.getenv("OPENAI_BASE_URL", "").strip()
        or os.getenv("OPENAI_API_BASE", "").strip()
        or os.getenv("OLLAMA_BASE_URL", "").strip()
        or None
    )


def is_api_key_configured() -> bool:
    """
    Check whether a non-empty, non-placeholder API key is set in the environment,
    or a local model endpoint (e.g. Ollama, LocalAI, vLLM) is configured.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key and api_key.lower() not in PLACEHOLDER_KEYS:
        return True

    # If an Ollama or local endpoint is configured, an OpenAI API key is not required
    base_url = get_configured_base_url()
    if base_url:
        lower_url = base_url.lower()
        if any(h in lower_url for h in ("localhost", "127.0.0.1", "ollama")):
            return True

    return False


def get_configured_model_name(override_model: str | None = None) -> str:
    """Return the configured model name or default to 'gpt-4o-mini'."""
    if override_model:
        return override_model
    return (
        os.getenv("OPENAI_MODEL_NAME", "").strip()
        or os.getenv("OLLAMA_MODEL", "").strip()
        or os.getenv("MODEL_NAME", "").strip()
        or "gpt-4o-mini"
    )


def get_configured_timeout() -> int:
    """Return timeout in seconds for LLM calls (default: 30)."""
    raw_val = os.getenv("LLM_TIMEOUT", "30").strip()
    try:
        return max(5, int(raw_val))
    except ValueError:
        return 30


def get_llm(
    model: str | None = None,
    temperature: float = 0.0,
    timeout: int | None = None,
) -> BaseChatModel:
    """
    Factory to construct an authenticated ChatOpenAI instance for OpenAI or
    any OpenAI-compatible provider (including local Ollama / vLLM instances).

    Raises:
        MissingApiKeyError: If OPENAI_API_KEY is missing/placeholder and no local endpoint is set.
    """
    if not is_api_key_configured():
        raise MissingApiKeyError(
            "LLM API credentials are missing or unconfigured.\n"
            "To enable AI-assisted review, create a '.env' file based on '.env.example' "
            "and set OPENAI_API_KEY, or configure a local endpoint (OPENAI_BASE_URL or OLLAMA_BASE_URL)."
        )

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model_name = get_configured_model_name(model)
    base_url = get_configured_base_url()
    request_timeout = timeout or get_configured_timeout()

    # For local providers (e.g. Ollama) without an explicit API key, supply a non-empty token
    if not api_key or api_key.lower() in PLACEHOLDER_KEYS:
        api_key = "ollama"

    kwargs = {
        "model": model_name,
        "api_key": api_key,
        "temperature": temperature,
        "timeout": request_timeout,
        "max_retries": 2,
    }
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)
