# Week 4 Notes — Provider Abstraction + POC

## 1. What I was asked to do
The goal of Week 4 was to understand provider abstraction and build a proof of concept (POC) that can switch between different AI model providers. The project also required a compatibility matrix, repository audit, security report, license/terms notes, and a short demonstration.

## 2. Key concepts

### Provider vs. model
- **Provider:** The service or runtime that gives access to a model, such as Gemini, OpenAI, Ollama, or a llama.cpp server.
- **Model:** The specific AI model selected through that provider, such as `gemini-2.5-flash` or `llama3.2:1b`.
- One provider may offer several models. A provider and a model are not the same thing.

### Provider abstraction
Provider abstraction means giving different providers a common interface. The rest of the application calls the same methods instead of needing completely different code for every provider.

### Adapter
An adapter translates the common gateway methods into the format required by a specific provider. For example, the Ollama adapter communicates with the Ollama API, while the llama.cpp adapter communicates with the local llama-server API.

### Provider switching
The application can choose a provider through configuration or the dashboard. In my POC, I switched providers from the dashboard without restarting the FastAPI backend.

## 3. Model Gateway interface
The Week 4 mini-project called for a common interface with methods such as:

- `testConnection()` — checks whether a provider can be reached or validated.
- `getModels()` — retrieves the models available through the provider.
- `generate()` — sends a prompt and returns generated text.
- `stream()` — optional method for returning generated text in chunks.

The exact API request and response formats can differ between providers, so each adapter handles those differences.

## 4. My project setup
- **Frontend:** HTML, CSS, and JavaScript in `index.html`.
- **Backend:** Python with FastAPI.
- **HTTP client:** `httpx`.
- **Configuration:** environment variables loaded from `.env`.
- **Local providers tested:** Ollama and llama.cpp Server.
- **Cloud providers tested:** Gemini and OpenAI; I also checked the Qwen-compatible API connection.
- **Backend command:**

```bash
uvicorn main:app --reload
```

I used the FastAPI backend locally at `http://127.0.0.1:8000`. The llama.cpp server ran separately at the configured local endpoint, so its terminal needed to remain open while I tested it.

## 5. Configuration and security
The project uses environment variables for provider settings, including API keys, local base URLs, timeouts, and allowed CORS origins.

Important practices:
- Keep real API keys in `.env` and keep `.env` out of Git.
- Use placeholder values in `.env.example`.
- Never put API keys in frontend JavaScript or show them in screenshots and recordings.
- Keep local inference servers on `127.0.0.1` for a local demo unless secure remote access is deliberately configured.
- Restrict CORS to the frontend origins actually used.
- Handle timeouts, quota errors, and provider failures without exposing secrets.

## 6. Practical test results

| Provider / model | Observed result |
|---|---|
| Ollama — `llama3.2:1b` | Connection and model listing passed. Text generation returned a response, but the answer did not follow my exact prompt very well. |
| llama.cpp Server — `ggml-org/Qwen3.5-0.8B-GGUF` | Connection, model listing, and text generation passed after I started `llama-server`. |
| Gemini — `gemini-2.5-flash` | Text generation passed and returned “Hello! How can I help you today?” |
| Gemini — `gemini-2.5-pro` | The request returned HTTP 404 for the requested model or endpoint. |
| Gemini — `nano-banana-pro-preview` | The request returned a quota/rate-limit error. |
| OpenAI | Connection test passed and reported 110 accessible models, but chat generation returned HTTP 429 / quota or rate-limit error. |
| Qwen-compatible API (DashScope) | I tested the connection, but a confirmed successful generation result was not recorded in my notes. |

### What I learned from testing
A connection test, model listing, and text-generation test measure different things. A provider can connect successfully but fail to generate text because of a quota limit, unsupported model, or endpoint mismatch. A generated response can also be low quality even when the request succeeds.

## 7. Repository audit notes

### Qwen Code
- Repository: https://github.com/QwenLM/qwen-code
- License observed: Apache License 2.0.
- I found `SECURITY.md`, which points vulnerability reports to a security issue reporting portal.
- It is an example of a coding agent designed to work with different model providers.

### llama.cpp
- Repository: https://github.com/ggml-org/llama.cpp
- License observed: MIT.
- I found `SECURITY.md`, which discusses untrusted models and inputs, privacy, untrusted networks, and multi-tenant environments.
- The security page I inspected said its private disclosure program was disabled and requested patches with fixes through public pull requests.
- I used its local HTTP server in my POC.

### Ollama
- Repository: https://github.com/ollama/ollama
- License observed: MIT.
- I found `SECURITY.md`, which directs vulnerability reports to GitHub Security Advisories and recommends securing hosted instances.
- I tested it with `llama3.2:1b`.

### llmfit
- Repository: https://github.com/AlexsJones/llmfit
- License observed: MIT.
- I did not see a `SECURITY.md` file in the repository root file list during my inspection.
- It helps estimate which local models may fit available hardware. It is a model-selection aid, not an inference server.

## 8. License and terms notes
- Qwen Code's repository uses Apache 2.0; the other three repositories use MIT.
- MIT permits use, modification, distribution, and commercial use, subject to retaining the required copyright and permission notices.
- Apache 2.0 permits use, modification, and distribution subject to its conditions, including relevant notices and patent terms.
- A repository's code license does not automatically apply to every model weight, dataset, dependency, or hosted API.
- I should check each model's own license and each provider's API terms before redistribution or deployment.

## 9. Main security points
- Keep API keys private and out of source control.
- Do not expose local inference ports publicly without suitable access controls.
- Treat model files, prompts, and generated output as potentially untrusted.
- Validate incoming requests and use timeouts.
- Do not log API keys or sensitive request headers.
- Handle HTTP 404 and 429 responses clearly and avoid repeated retries without backoff.
- Review each repository's security instructions before reporting a vulnerability.

## 10. Final learning summary
During Week 4, I learned how provider abstraction and adapters make it possible to connect different model services through a common gateway. I demonstrated switching providers from the dashboard and tested connection checks, model listing, and text generation. I also compared the four open-source repositories, checked their licenses and visible security policies, and recorded practical security considerations for my POC.

## 11. References
- Qwen Code: https://github.com/QwenLM/qwen-code
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Ollama: https://github.com/ollama/ollama
- llmfit: https://github.com/AlexsJones/llmfit
