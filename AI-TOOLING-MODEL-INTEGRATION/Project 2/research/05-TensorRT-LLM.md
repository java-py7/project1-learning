# TensorRT-LLM

**Repository:** https://github.com/NVIDIA/TensorRT-LLM  
**Main technologies:** Python, C++ and NVIDIA GPU kernels  
**License:** Check the repository's current LICENSE and third-party notices before redistribution; the project has Apache-2.0 licensing information, but bundled components and model assets may have separate terms.  
**Role in this project:** Reference for advanced NVIDIA GPU inference.

## What it does

TensorRT-LLM provides optimized inference building blocks and runtimes for NVIDIA GPU hardware. It targets performance on supported NVIDIA architectures.

## Features relevant to my work

- GPU-optimized kernels and execution.
- Quantization options that vary by GPU architecture and model.
- KV-cache and serving optimizations.
- Multi-GPU and parallel execution features.
- NVIDIA ecosystem integration.

## Build and dependencies

It has a substantial environment requirement: compatible NVIDIA GPU, driver, CUDA and TensorRT components, plus supported operating system/container versions. Consult the current support matrix before attempting installation.

## Fit for my PC

Not suitable for my GT 730 as a target runtime. The published supported-hardware matrix focuses on modern NVIDIA architectures such as Ampere, Ada, Hopper and Blackwell. The GT 730 is far older and is not listed.

## Current decision

**Do not install on the current PC.** Keep it in the repository comparison to understand what modern GPU-specific optimization looks like.

## References

- Repository: https://github.com/NVIDIA/TensorRT-LLM
- Supported hardware: https://nvidia.github.io/TensorRT-LLM/reference/support-matrix.html
