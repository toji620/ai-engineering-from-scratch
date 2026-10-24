"""Lesson 0.4: the same Claude call made with the SDK and with raw HTTP.

Reads ANTHROPIC_API_KEY from the environment or from a .env file in the
current directory. Prints both full responses (Exercise 2) and turns API
errors into readable messages instead of crashing (Exercise 3).
"""
import json
import os
import urllib.error
import urllib.request

import anthropic

PROMPT = "What is a neural network in one sentence?"


def load_dotenv(path=".env"):
    """Minimal .env loader: KEY=VALUE lines, # comments, optional quotes."""
    try:
        with open(path) as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def call_with_sdk(model):
    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model=model,
            max_tokens=256,
            messages=[{"role": "user", "content": PROMPT}],
        )
    except anthropic.AuthenticationError as e:
        print(f"401 AuthenticationError: {e.message}")
        return
    except anthropic.RateLimitError as e:
        print(f"429 RateLimitError, wait and retry: {e.message}")
        return
    except anthropic.APIStatusError as e:
        print(f"{e.status_code} {type(e).__name__}: {e.message}")
        return
    print("Full SDK response object:")
    print(response)
    print(f"\nAnswer: {response.content[0].text}")
    print(f"Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")


def call_raw_http(model):
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({
            "model": model,
            "max_tokens": 256,
            "messages": [{"role": "user", "content": PROMPT}],
        }).encode(),
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
        return
    print("Full raw JSON response:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    load_dotenv()
    model = os.environ.get("LLM_MODEL", "claude-sonnet-5")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("No ANTHROPIC_API_KEY found. Put it in .env or export it first.")
        raise SystemExit(1)
    print(f"Model: {model}\n\n=== 1. SDK ===")
    call_with_sdk(model)
    print("\n=== 2. Raw HTTP ===")
    call_raw_http(model)
