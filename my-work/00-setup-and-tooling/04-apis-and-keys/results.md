# Lesson 0.4 results: APIs & Keys

The key is stored in `my-course/.env`, which git ignores (`.gitignore` line 31) and which has `chmod 600`. It isn't committed anywhere.
Model: `claude-sonnet-5` (the lesson default). Prompt: "What is a neural network in one sentence?"

## Exercise 1: first API call
`api_calls.py` with the SDK: answer received, 18 input / 75 output tokens, `stop_reason: end_turn`.
`first_api_call.ts`, live with raw `fetch`: answer received, 18 / 73 tokens, exit 0.

## Exercise 2: SDK vs raw HTTP
The same fields appear in both: `id`, `content[0].text`, `stop_reason`, `usage.input_tokens` and `usage.output_tokens`.
- SDK: a `Message` object, read with attributes: `response.content[0].text`, `response.usage.input_tokens`
- Raw: a dict parsed from JSON, read with keys: `result["content"][0]["text"]`, `result["usage"]["input_tokens"]`

The two answers were worded slightly differently (75 vs 73 tokens), because generation is random.
The cost of both calls was about $0.0016 (36 input tokens at $2/M plus 148 output tokens at $10/M).

## Exercise 3: wrong key
`ANTHROPIC_API_KEY=sk-ant-this-is-a-fake-key` gave HTTP 401, `authentication_error`, "invalid x-api-key".
- The SDK raises `anthropic.AuthenticationError`. The course script crashed on it, so `api_calls.py` catches it.
- Raw urllib raises `urllib.error.HTTPError` with code 401.
- With no key at all, the SDK raises `TypeError: Could not resolve authentication method`, and nothing is sent.
