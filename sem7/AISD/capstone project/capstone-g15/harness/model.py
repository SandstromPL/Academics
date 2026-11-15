"""One function for every model call: call_model(messages, model) -> dict.

Same client as the labs (lab-12 agent.py): openai.OpenAI with OPENAI_BASE_URL and
OPENAI_API_KEY from your workspace (your OWN key), gateway model "main" (or "aux").
The SDK retries 429, 5xx and connection errors MAX_RETRIES times with backoff.
Every result carries the gateway's response id, so trace rows can be joined to
gateway rows.
"""
import os
import time

TIMEOUT_S = 60      # per model call
MAX_RETRIES = 2     # SDK retries on 429 / 5xx / network errors
_client = None


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        base = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
        key = os.environ.get("OPENAI_API_KEY")
        if not base or not key:
            raise RuntimeError("set OPENAI_BASE_URL and OPENAI_API_KEY (your own gateway key)")
        _client = OpenAI(base_url=base, api_key=key, max_retries=MAX_RETRIES, timeout=TIMEOUT_S)
    return _client


def call_model(messages, model="main", max_tokens=2000, temperature=0.0):
    """Returns {"text", "prompt_tokens", "completion_tokens", "latency_ms", "model",
    "response_id", "finish_reason"}."""
    t0 = time.time()
    resp = _get_client().chat.completions.create(model=model, messages=messages,
                                                 max_tokens=max_tokens, temperature=temperature)
    usage = resp.usage
    choice = resp.choices[0]
    return {
        "text": choice.message.content or "",
        "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
        "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
        "latency_ms": int((time.time() - t0) * 1000),
        "model": resp.model or model,
        "response_id": resp.id,
        "finish_reason": choice.finish_reason,
    }
