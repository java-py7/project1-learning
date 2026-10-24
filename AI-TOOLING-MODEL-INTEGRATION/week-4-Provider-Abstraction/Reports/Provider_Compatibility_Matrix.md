# Provider Compatibility Matrix
**Week 4 — Model Gateway POC**

## Overview
This document summarizes the provider tests I performed for my Model Gateway proof of concept. I tested whether each provider could connect, list models, and generate a response. These are separate checks: a successful connection does not always mean chat generation will work.

## Test results

| Provider / model | Connection test | Model listing | Chat generation | Result from my testing |
|---|---|---|---|---|
| Ollama — `llama3.2:1b` | Passed | Passed | Passed | The model returned a response, but it did not follow my exact test prompt very well. |
| llama.cpp Server — `ggml-org/Qwen3.5-0.8B-GGUF` | Passed after I started `llama-server` | Passed | Passed | The model returned a response through the local server. I need to keep the server terminal running while testing it. |
| Google Gemini — `gemini-2.5-flash` | Passed in my test | Passed | Passed | It returned: “Hello! How can I help you today?” |
| Google Gemini — `gemini-2.5-pro` | Not confirmed separately | Request returned 404 | Failed in this test | The requested model or endpoint was not found. |
| Google Gemini — `nano-banana-pro-preview` | Not confirmed separately | Not confirmed | Failed in this test | The request returned a quota or rate-limit error. |
| OpenAI | Passed; the test endpoint reported 110 accessible models | Passed | Failed in my chat test | Chat generation returned HTTP 429, indicating a quota or rate-limit problem. |
| Qwen-compatible API (DashScope) | I tested the connection | Not confirmed in these notes | Not confirmed in these notes | I have not recorded a confirmed successful generation result here. |

## What I learned
- **Connection test:** checks whether the provider can be reached or validated.
- **Model listing:** checks whether the gateway can retrieve the provider's available models.
- **Chat generation:** confirms whether a prompt actually returns a response.
- **HTTP 404:** in my Gemini test, the requested model or endpoint was not found.
- **HTTP 429:** in my OpenAI test, the request was limited by quota or rate limits.
- A provider may connect successfully but still fail when generating a response.
- A model can generate a response but still give a poor answer to the prompt, as I observed with Ollama.

## Conclusion
I demonstrated provider switching from the dashboard without restarting the FastAPI backend. During my tests, Ollama, llama.cpp Server, and Gemini `gemini-2.5-flash` generated responses. The OpenAI connection test passed, but the chat request returned HTTP 429. The Gemini Pro request returned 404, and the Gemini preview-model request returned a quota/rate-limit error. I tested the Qwen-compatible API connection, but I have not recorded a confirmed chat-generation result for it in this matrix.

## Notes
These results reflect the tests I actually performed during this POC. They are not a guarantee that every model or account will behave the same way. I will use my screenshots and demonstration recording as supporting evidence.
