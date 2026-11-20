# llama.cpp

**Repository:** https://github.com/ggml-org/llama.cpp  
**Main language:** C/C++  
**License shown by repository:** MIT  
**Role in this project:** Candidate for the first local inference experiments.

## What it does

llama.cpp is a local inference implementation built on the ggml tensor library. It is designed to run supported language models across different hardware, including CPU-only machines. It commonly uses GGUF model files.

## Features relevant to my work

- Quantized model formats, including low-bit GGUF variants.
- CPU inference.
- Optional GPU backends and CPU/GPU layer offloading.
- Memory-mapped model loading.
- KV-cache configuration and quantized cache types.
- A command-line interface and an HTTP server example.

The exact formats and features depend on the model architecture and the selected build/backend. A quantization label does not guarantee the same memory use or quality for every model.

## Build and dependencies

The project uses CMake and a C/C++ compiler. GPU acceleration is optional and requires a compatible backend and its toolchain. The official build guide lists CPU, CUDA, Vulkan, Metal and other backend paths.

## Fit for my PC

This is the most sensible first candidate because CPU inference does not depend on the GT 730. I should start with a CPU build and record a baseline before testing optional acceleration.

The GT 730 must not be assumed to support a current CUDA or Vulkan build. Identify the exact GPU variant and verify backend requirements first.

## Risks and limitations

- Disk mapping does not make a model's computation free; memory pressure and storage speed still matter.
- Offloading can reduce VRAM requirements but may reduce generation speed.
- GGUF compatibility depends on the model architecture and runtime version.
- Model files have their own licenses, separate from the runtime's MIT license.

## Current decision

**Keep as the primary candidate for the first proof of concept.** This is a research selection, not yet a benchmark result.

## References

- Repository: https://github.com/ggml-org/llama.cpp
- Build guide: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- README: https://github.com/ggml-org/llama.cpp/blob/master/README.md
