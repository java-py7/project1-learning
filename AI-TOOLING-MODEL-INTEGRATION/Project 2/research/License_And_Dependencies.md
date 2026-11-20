# License and Dependency Notes — Project 2

## Scope

These notes summarize the license and dependency information recorded in my seven repository audits. They are an initial screening, not legal advice or final approval for redistribution. A runtime's repository license does not automatically cover model weights, datasets, downloaded assets, bundled libraries or every dependency.

## Repository license and dependency overview

| Project | License recorded in my audit | Main technologies / dependency areas recorded | Follow-up before reuse |
|---|---|---|---|
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | MIT | C/C++, CMake, C/C++ compiler; optional CUDA, Vulkan, Metal, HIP and other backend toolchains | Review third-party notices and the license for each GGUF model. Confirm the selected backend's build requirements. |
| [MLC LLM](https://github.com/mlc-ai/mlc-llm) | Apache-2.0 | Python, C++, TVM/MLC compiler components and platform-specific backend SDKs | Review third-party components, backend requirements and model redistribution terms. |
| [ExLlamaV2](https://github.com/turboderp-org/exllamav2) | MIT | Python, PyTorch, CUDA Toolkit, C++ extensions and platform build tools | V2 is archived and development moved to ExLlamaV3. Check the successor separately before selecting a current implementation. |
| [vLLM](https://github.com/vllm-project/vllm) | Apache-2.0 | Python, PyTorch, CMake/Ninja, compiled kernels and backend-specific packages | Follow the installation path for the intended hardware and operating system; review dependency notices and model terms. |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | The audit notes Apache-2.0 licensing information; verify the current repository LICENSE and notices before redistribution | Python, C++, NVIDIA driver, CUDA, TensorRT, GPU kernels and supported OS/container environment | Verify the current license files, third-party notices, supported GPU, release compatibility and model terms. |
| [PowerInfer](https://github.com/SJTU-IPADS/PowerInfer) | **Not verified in my audit** | Project-specific C++/GPU toolchain and model dependencies; exact requirements need inspection | Inspect the repository's LICENSE, requirements, commit history and issue activity before adopting or redistributing it. |
| [FlexGen](https://github.com/FMInference/FlexGen) | **Not verified in my audit** | Python, PyTorch and model tooling | Check the original FMInference repository's LICENSE and current activity. Distinguish it from similarly named forks. |

## Important distinction: runtime license vs. model license

A permissive runtime license does not mean every model downloaded for that runtime is permissively licensed. I need to review the model card and model-weight terms separately, including restrictions on commercial use, modification and redistribution.

The same caution applies to datasets, tokenizer files, adapters, quantized model files and other downloaded assets. Their terms may differ from the runtime's license.

## Checks before adopting or redistributing a project

1. Read the current `LICENSE` file in the exact repository and record the release or commit being used.
2. Review third-party notices and the licenses of bundled or installed dependencies.
3. Check model cards and model-weight licenses separately from the runtime license.
4. Confirm whether the intended use permits commercial use, modification and redistribution.
5. Preserve copyright, attribution and notice files where required.
6. Check whether the repository is archived or has moved to a successor project.
7. Record the versions of Python, PyTorch, CUDA, compiler tools and backend packages used for the tested setup.
8. Recheck licenses and dependencies before packaging or distributing the final application.

## Current status

- License information is recorded as MIT for llama.cpp and ExLlamaV2, and Apache-2.0 for MLC LLM and vLLM, based on the repository audits.
- TensorRT-LLM needs a direct check of its current LICENSE and third-party notices before redistribution.
- PowerInfer and FlexGen license status remains **unverified** in this research pass.
- No project is approved for redistribution solely on the basis of this summary.
