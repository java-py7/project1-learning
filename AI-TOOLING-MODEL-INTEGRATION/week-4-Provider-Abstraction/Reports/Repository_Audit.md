# Repository Audit
**Week 4 — Provider Abstraction and Model Gateway POC**

## 1. Purpose
I reviewed four open-source repositories related to AI coding tools and local model inference: Qwen Code, llama.cpp, Ollama, and llmfit. I checked their purpose, license, and visible security-policy information, and noted how each project relates to my Model Gateway POC.

## 2. Qwen Code
**Repository:** https://github.com/QwenLM/qwen-code

- **Purpose:** An AI coding agent that can work with different model providers and compatible endpoints.
- **License:** Apache License 2.0. The repository's `LICENSE` page identifies this license.
- **Security policy:** I found `SECURITY.md`. It directs people who discover security vulnerabilities to the project's “Report Security Issue” portal. The policy says this channel is for security-related issues, not ordinary bugs.
- **Relevance to my project:** It is a useful example of an application designed to work with multiple model providers rather than being tied to a single provider.

## 3. llama.cpp
**Repository:** https://github.com/ggml-org/llama.cpp

- **Purpose:** Runs language models locally and provides command-line tools and an HTTP server that can expose an API compatible with common OpenAI-style clients.
- **License:** MIT. I checked the repository's MIT license page.
- **Security policy:** I found `SECURITY.md`. It covers topics such as untrusted models, untrusted inputs, data privacy, untrusted networks, and multi-tenant environments. During my inspection, the page stated that its private security disclosure program was disabled until further notice and asked for patches with fixes to be submitted as public pull requests.
- **Relevance to my project:** I used a running `llama-server` as a local provider in my POC. The server had to be started separately and kept running for the gateway to connect to it.

## 4. Ollama
**Repository:** https://github.com/ollama/ollama

- **Purpose:** A local model runtime that lets users download and run supported language models and access them through an API.
- **License:** MIT. I checked the repository's MIT license page.
- **Security policy:** I found `SECURITY.md`. It asks users not to report vulnerabilities in public issues, but to use GitHub Security Advisories. The page recommends updating Ollama, securing access to hosted instances, and monitoring for unusual activity.
- **Relevance to my project:** I tested Ollama with the `llama3.2:1b` model through my Model Gateway. The model returned a response, although it did not follow my exact test prompt very well.

## 5. llmfit
**Repository:** https://github.com/AlexsJones/llmfit

- **Purpose:** Helps estimate which local language models may fit a computer's available hardware, including memory and GPU resources.
- **License:** MIT. I checked the repository's MIT license page.
- **Security policy:** I did not see a `SECURITY.md` file in the repository root file list during my inspection. This only records what I observed; it does not prove that the project has no other security-reporting process.
- **Relevance to my project:** It can help users choose an appropriate local model before configuring it in a gateway. It is a model/hardware recommendation tool, rather than an inference server itself.

## 6. Comparison summary

| Project | Main role | License observed | Security-policy observation |
|---|---|---|---|
| Qwen Code | Multi-provider AI coding agent | Apache 2.0 | `SECURITY.md` provides a security issue reporting portal |
| llama.cpp | Local model inference and server | MIT | `SECURITY.md` documents safe usage topics; private disclosure program was stated to be disabled during inspection |
| Ollama | Local model runtime and API | MIT | `SECURITY.md` recommends GitHub Security Advisories for vulnerabilities |
| llmfit | Hardware-aware local model recommendations | MIT | No root `SECURITY.md` was visible in the file list I inspected |

## 7. What I learned
- These projects serve different purposes: Qwen Code is an AI coding agent, llama.cpp and Ollama run models, and llmfit helps select models for available hardware.
- A common API format can make it easier for one application to communicate with different providers, but provider-specific models, endpoints, limits, and errors still need to be handled.
- Licenses and security-reporting instructions differ between repositories, so I should check each project's own files rather than assume they all follow the same rules.
- A repository's license applies to its code. Model weights and external services may have separate licenses, terms, or usage restrictions that must be checked independently.

## 8. Sources
- Qwen Code: https://github.com/QwenLM/qwen-code
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Ollama: https://github.com/ollama/ollama
- llmfit: https://github.com/AlexsJones/llmfit
