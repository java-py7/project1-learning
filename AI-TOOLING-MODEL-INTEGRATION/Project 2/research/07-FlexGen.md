# FlexGen

**Repository:** https://github.com/FMInference/FlexGen  
**Role in this project:** Research reference for CPU/GPU/disk offloading and throughput-oriented inference.

## What it does

FlexGen investigates running large language models with limited GPU memory by distributing weights, activations and attention cache across GPU memory, CPU memory and disk. It uses scheduling and compression to improve throughput for suitable workloads.

## Features relevant to my work

- GPU, CPU and disk offloading.
- Weight and KV-cache compression.
- Configurable placement of model data.
- Throughput-oriented batch inference.
- Research results for large models under constrained GPU memory.

## Important limitation

FlexGen is designed mainly for throughput-oriented workloads, not low-latency interactive chat. Offloading to disk can make a configuration technically possible while making generation very slow.

The published examples use systems with much more CPU memory and storage than my PC. The project documentation includes examples requiring around 90 GB of CPU memory for some 30B-class experiments. That is far beyond my 16 GB.

## Build and dependencies

The README lists PyTorch and Python installation paths. The exact supported Python/PyTorch versions and current compatibility should be verified before attempting a build.

## License and maintenance

Check the exact LICENSE file and current repository activity before reuse. Also distinguish the original FMInference repository from similarly named forks.

## Fit for my PC

Useful for learning about memory placement and offloading policies. Not a realistic first implementation target on this machine because the documented examples assume substantially more CPU memory.

## Current decision

**Research reference only.** I may borrow ideas for experiments, but should not promise FlexGen-scale results on this hardware.

## References

- Repository: https://github.com/FMInference/FlexGen
- Paper: https://arxiv.org/abs/2303.06865
