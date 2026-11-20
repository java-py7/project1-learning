# ExLlamaV2

**Repository:** https://github.com/turboderp-org/exllamav2  
**Main language:** Python with compiled extensions  
**License shown by repository:** MIT  
**Role in this project:** Reference for low-bit GPU inference, not a likely runtime for my current PC.

## What it does

ExLlamaV2 is an inference library aimed at running language models locally on modern consumer-class GPUs. Its focus is fast GPU inference and quantized model formats.

## Features relevant to my work

- GPTQ model support.
- EXL2 quantization, with mixed bits-per-weight settings.
- GPU splitting for multi-GPU setups.
- Prompt caching and KV-cache-related features.
- Speculative decoding support in its generation stack.

## Build and dependencies

The repository instructions call for Python, a compatible PyTorch build, CUDA Toolkit and platform build tools. CUDA/PyTorch version compatibility is important when installing compiled extensions.

## Maintenance note

The repository README says ExLlamaV2 is archived for now and that development continues in ExLlamaV3. Treat V2 as a reference implementation unless there is a specific reason to test it. Check the V3 repository separately before choosing a current ExLlama path.

## Fit for my PC

Low priority. The project is designed around modern NVIDIA GPUs and CUDA. Our GT 730 is not a suitable assumption for a supported modern CUDA inference setup. Do not spend time installing it before verifying GPU architecture and supported CUDA capability.

## Current decision

**Research reference only for now.** It is useful for understanding EXL2 and GPU-focused inference trade-offs.

## References

- Repository: https://github.com/turboderp-org/exllamav2
- Successor: https://github.com/turboderp-org/exllamav3
