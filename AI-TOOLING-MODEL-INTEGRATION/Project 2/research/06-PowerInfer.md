# PowerInfer

**Repository:** https://github.com/SJTU-IPADS/PowerInfer  
**Role in this project:** Research reference for activation-aware CPU/GPU hybrid inference.

## What it does

PowerInfer explores the observation that neural network activations are not uniformly active. Its approach places frequently used parts of computation on the GPU and uses the CPU for other parts, with the goal of reducing GPU memory pressure.

## Features relevant to my work

- CPU/GPU hybrid inference research.
- Activation locality and prediction.
- Sparse computation ideas.
- A research-oriented approach to reducing accelerator memory requirements.

## Build and dependencies

The repository's setup and supported GPU requirements should be checked from its current README and scripts. Do not assume it is a drop-in backend for llama.cpp.

## Fit for my PC

Conceptually relevant because my GPU memory is limited. Practical compatibility is uncertain and must be tested against its current hardware requirements. Its published research results should not be treated as predictions for a GT 730.

## License and maintenance

**Not yet verified in this audit.** Inspect the repository's LICENSE file, recent commits, issues and dependency versions before adopting or redistributing it.

## Current decision

**Keep as a research reference.** It may help us understand workload placement and hybrid inference even if it is not the engine I run.

## References

- Repository: https://github.com/SJTU-IPADS/PowerInfer
- Paper: https://arxiv.org/abs/2312.12456
