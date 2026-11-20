# Repository Comparison — Project 2

## Scope

I compared the seven repositories I researched for Project 2: llama.cpp, MLC LLM, ExLlamaV2, vLLM, TensorRT-LLM, PowerInfer and FlexGen. This is a documentation-based technical comparison, not a result from installing or benchmarking these runtimes on my PC.

## Comparison

| Project | Main purpose | Relevant techniques / features | Hardware and setup considerations | Decision for my project |
|---|---|---|---|---|
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Local inference across different hardware, including CPU-only systems | GGUF quantization, CPU inference, optional GPU backends and layer offload, memory-mapped loading, KV-cache configuration, CLI and HTTP server | C/C++, CMake and a C/C++ compiler. GPU acceleration requires a compatible backend and toolchain. | **Primary candidate.** Start with CPU-only inference to establish a baseline without depending on the GT 730. |
| [MLC LLM](https://github.com/mlc-ai/mlc-llm) | Compiler-based model deployment across supported platforms | Model compilation, quantized deployment, Vulkan/CUDA/ROCm/Metal/WebGPU paths where supported, engine API and OpenAI-compatible REST interface | Python, C++, TVM-related compiler components and backend-specific setup. Backend, model and platform support must be checked together. | **Secondary candidate.** Investigate after checking the GT 730's exact Vulkan capability and current Windows instructions. |
| [ExLlamaV2](https://github.com/turboderp-org/exllamav2) | Fast local inference on modern consumer NVIDIA GPUs | GPTQ, EXL2 mixed bits-per-weight, GPU splitting, prompt/KV-cache features and speculative decoding | Python, compatible PyTorch, CUDA Toolkit and build tools. The V2 repository is archived; development moved to ExLlamaV3. | **Research reference.** Useful for studying low-bit GPU inference, but not a sensible first runtime for this PC. |
| [vLLM](https://github.com/vllm-project/vllm) | High-throughput inference serving | PagedAttention, KV-cache management, continuous batching, streaming and an OpenAI-compatible API server | Python, PyTorch, build tools and hardware-specific packages. CPU installation exists, but feature support differs by backend. | **Architecture reference.** Its serving and batching ideas are relevant, but its stack and main strengths do not make it the first choice for this older desktop. |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | Optimized inference on supported NVIDIA GPUs | GPU-optimized kernels, quantization options, KV-cache and serving optimizations, multi-GPU execution | Requires a compatible NVIDIA GPU, driver, CUDA and TensorRT environment. The researched support matrix lists modern GPU architectures; the GT 730 is not listed. | **Do not target the current PC.** Keep it as a reference for modern NVIDIA-specific optimization. |
| [PowerInfer](https://github.com/SJTU-IPADS/PowerInfer) | Research into activation-aware CPU/GPU hybrid inference | Activation locality and prediction, sparse computation, and placement of frequently active computation on the GPU | Current build instructions and supported GPU requirements need to be checked. It should not be assumed to be a drop-in backend for llama.cpp. | **Research reference.** Its hybrid placement ideas are relevant, but compatibility with my hardware is unverified. |
| [FlexGen](https://github.com/FMInference/FlexGen) | Throughput-oriented inference using GPU, CPU and disk placement | Weight, activation and KV-cache placement; offloading; compression and scheduling | Python and PyTorch. Some documented 30B-class examples require around 90 GB of CPU memory, well beyond my 16 GB. Disk offload can also make generation slow. | **Research reference.** Useful for studying offloading policies, but not a realistic first implementation target on this PC. |

## Comparison findings

1. **CPU-first inference:** llama.cpp is the clearest starting point because it supports CPU-only execution and does not require the GT 730 to be usable.
2. **Compiler-based deployment:** MLC LLM is worth investigating for cross-platform deployment, but its backend support must be validated for the exact GPU, driver, operating system and model.
3. **GPU-focused approaches:** ExLlamaV2 and TensorRT-LLM are not suitable first targets for the current machine. ExLlamaV2 is archived, while TensorRT-LLM's documented supported hardware focuses on much newer NVIDIA GPUs.
4. **Serving architecture:** vLLM is useful for understanding PagedAttention, KV-cache management and continuous batching. Its CPU support does not mean every feature or model will be practical on an older CPU.
5. **Hybrid and disk offloading:** PowerInfer and FlexGen provide useful research ideas. Their published approaches and hardware assumptions should not be treated as proof that the same performance is achievable on my PC.

## What this comparison does not establish

- I have not installed or benchmarked any of these seven projects as part of this research.
- I have not confirmed CUDA or Vulkan compatibility for the exact GT 730 variant.
- I have not measured model load time, RAM/VRAM use, time to first token, tokens per second or output quality.
- A feature listed by a project does not guarantee that it is available for every model, operating system or hardware backend.

## Overall decision

I will begin the implementation investigation with **llama.cpp in CPU mode**. MLC LLM is the next candidate only after checking hardware and backend compatibility. The other five projects remain comparison or research references for the specific techniques described above.
