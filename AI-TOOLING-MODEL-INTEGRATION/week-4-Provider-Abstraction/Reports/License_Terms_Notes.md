# License and Terms Notes
**Week 4 — Provider Abstraction and Model Gateway POC**

## 1. Purpose
I reviewed the licenses shown in the repositories used during my Week 4 audit. These notes summarize the main conditions I need to remember when using or distributing the projects. This is a practical summary, not legal advice.

## 2. License summary

| Project | Repository license I observed | Main points to remember |
|---|---|---|
| Qwen Code | Apache License 2.0 | Permits use, modification, distribution, and commercial use, subject to the license conditions. Preserve required copyright and license notices. It includes express patent-related terms and does not grant permission to use project trademarks freely. |
| llama.cpp | MIT | Permits use, modification, distribution, and commercial use. Include the copyright and permission notice in copies or substantial portions. The software is provided “as is,” without warranty. |
| Ollama | MIT | Permits use, modification, distribution, and commercial use. Include the copyright and permission notice in copies or substantial portions. The software is provided “as is,” without warranty. |
| llmfit | MIT | Permits use, modification, distribution, and commercial use. Include the copyright and permission notice in copies or substantial portions. The software is provided “as is,” without warranty. |

## 3. What this means for my project
- If I copy, modify, or redistribute code from these repositories, I should retain the relevant license and copyright notices as required.
- For Apache 2.0 code, I should also review its conditions for redistributions, notices of changed files, and patent terms when applicable.
- I should not treat an open-source license as permission to use a project's name or trademarks without restriction.
- MIT and Apache 2.0 licenses do not remove the need to check the terms of any hosted API or service I use.

## 4. Repository license versus model and API terms
The repository license covers the code that the project licenses. It does **not automatically establish the license or terms for every model weight, dataset, external dependency, or hosted provider service**.

For my POC:
- **Ollama:** the Ollama repository's MIT license is separate from the license or terms of a model downloaded and run through Ollama.
- **llama.cpp:** the repository's MIT license is separate from the license or terms attached to a particular model file, such as a GGUF model.
- **Gemini, OpenAI, and Qwen-compatible APIs:** I must follow the relevant provider's API terms, usage policies, rate limits, and billing/quota rules in addition to any license applying to my own code.
- **Qwen Code:** the Apache 2.0 license identified in its repository applies to the project code under that license; it should not be assumed to govern all models that Qwen Code can connect to.

## 5. Practical checklist
- [ ] Keep license and copyright notices when required.
- [ ] Check the license before redistributing third-party code.
- [ ] Check the model card or model repository for the model's own license and use restrictions.
- [ ] Review the provider's terms before using a hosted API.
- [ ] Keep API keys private and out of source control.
- [ ] Record any third-party libraries and their licenses when preparing a release.

## 6. Sources checked
- Qwen Code: https://github.com/QwenLM/qwen-code
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Ollama: https://github.com/ollama/ollama
- llmfit: https://github.com/AlexsJones/llmfit

## 7. What I learned
The four repositories I inspected use permissive open-source licenses: Qwen Code uses Apache 2.0, while llama.cpp, Ollama, and llmfit use MIT. However, I should check model-specific and API-specific terms separately instead of assuming the repository license covers every part of a complete AI setup.
