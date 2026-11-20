# vLLM

**Repository:** https://github.com/vllm-project/vllm  
**Main language:** Python and C++/GPU kernels  
**License shown by repository:** Apache-2.0  
**Role in this project:** Reference for efficient model serving and batching.

## What it does

vLLM is an inference and serving library. It is known for techniques such as PagedAttention and continuous batching, which help use accelerator memory efficiently when serving requests.

## Features relevant to my work

- High-throughput inference serving.
- PagedAttention and KV-cache management.
- Continuous batching and streaming.
- OpenAI-compatible API server.
- Parallel execution options and a broad model support list.
- CPU installation paths exist, but feature support differs from GPU paths.

## Build and dependencies

The project requires a supported Python version and PyTorch, plus build tools and hardware-specific packages. Current installation documentation lists CPU and multiple accelerator paths. Use the exact installation instructions for the target platform rather than copying a generic CUDA command.

## Fit for my PC

Not a first choice for the i5-4570/16 GB/GT 730 machine. Although CPU support exists, vLLM's main strengths are serving throughput, batching and accelerator memory management. It is more useful as an architecture reference and comparison point than as my first constrained-PC runtime.

## Risks and limitations

- Large dependency stack and compiled components.
- Feature availability differs across hardware backends.
- CPU support does not mean every model or serving feature is practical on an older desktop CPU.

## Current decision

**Keep for comparison and architecture study; defer local installation.**

## References

- Repository: https://github.com/vllm-project/vllm
- Installation: https://docs.vllm.ai/en/latest/getting_started/installation/
- CPU installation: https://docs.vllm.ai/en/latest/getting_started/installation/cpu/
