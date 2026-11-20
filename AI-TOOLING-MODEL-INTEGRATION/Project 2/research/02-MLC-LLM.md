# MLC LLM

**Repository:** https://github.com/mlc-ai/mlc-llm  
**Main technologies:** Python, C++ and machine-learning compilation components  
**License shown by repository:** Apache-2.0  
**Role in this project:** Cross-platform compiler/runtime candidate.

## What it does

MLC LLM is a machine-learning compiler and deployment engine. It compiles model execution for supported hardware backends and exposes a common engine interface.

## Features relevant to my work

- Model compilation for different target platforms.
- Quantized model deployment options.
- Vulkan, CUDA, ROCm, Metal and WebGPU paths, depending on operating system and device.
- An engine API and an OpenAI-compatible REST interface.
- Deployment paths for desktop, browser and mobile platforms.

Do not assume every backend supports every model or quantization format. The platform support matrix and model-specific documentation need to be checked together.

## Build and dependencies

The project has Python packaging and C++/compiler components, including TVM-related tooling. Installation is more involved than downloading a single executable because the target backend and model generally need to be prepared.

## Fit for my PC

Vulkan support makes it worth checking, but that does not establish compatibility with the GT 730. I need the precise card variant, driver and Vulkan capability before trying it. The CPU-only path and Windows support should also be checked against the current release instructions.

## Risks and limitations

- Compilation and model preparation add setup complexity.
- Backend support varies by platform and GPU.
- A successful compilation does not prove useful performance on older hardware.
- Model and third-party component licenses must be reviewed separately.

## Current decision

**Keep as a secondary candidate.** Consider it if the hardware checks show a usable backend or when testing cross-platform deployment.

## References

- Repository: https://github.com/mlc-ai/mlc-llm
- Documentation: https://llm.mlc.ai/
