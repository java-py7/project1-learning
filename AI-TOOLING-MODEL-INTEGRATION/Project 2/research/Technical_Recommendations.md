# Technical Recommendations — Project 2

## 1. My current PC

The hardware information collected for this project is:

| Component | Detected information |
|---|---|
| CPU | Intel Core i5-4570, 4 cores / 4 threads |
| System RAM | 16 GB |
| GPU | NVIDIA GeForce GT 730 |
| GPU memory shown by Windows | Approximately 4 GB dedicated memory; Windows also showed shared GPU memory, which is borrowed system RAM rather than dedicated VRAM |
| Storage | 512 GB SSD and 500 GB HDD |
| Free space at the time of the audit | Approximately 152 GB on C: and 109 GB on D: |

The exact GT 730 board variant, memory type, CUDA capability and Vulkan support have not been confirmed. I should not assume that a backend supports this GPU just because the project supports CUDA or Vulkan in general.

## 2. Recommended runtime order

### First: llama.cpp — CPU-only baseline

I should start with [llama.cpp](https://github.com/ggml-org/llama.cpp) using a CPU build. It supports CPU inference and GGUF models, so the first experiment does not depend on the GT 730.

The initial run should establish a repeatable baseline before changing hardware settings or trying acceleration. I should record the model file, quantization, runtime version, command, context length, prompt and system state.

### Second: MLC LLM — conditional investigation

[MLC LLM](https://github.com/mlc-ai/mlc-llm) is the next candidate because it has compiler-based deployment and platform-specific backends, including Vulkan where supported.

I should only attempt it after checking the exact GPU variant, driver, Vulkan capability and current Windows installation instructions. General Vulkan support in MLC LLM does not prove that this particular GT 730 can run it.

### Research references, not initial installation targets

- **PowerInfer:** Study activation-aware CPU/GPU placement and sparse computation. Practical hardware/build compatibility is still unverified.
- **FlexGen:** Study CPU/GPU/disk placement and compression. Its documented examples include 30B-class experiments requiring around 90 GB of CPU memory, far beyond my 16 GB. It is throughput-oriented, and disk offloading may make interactive generation slow.
- **ExLlamaV2:** Study GPTQ and EXL2 low-bit GPU inference ideas. V2 is archived, and its CUDA-focused design is not a good first fit for this PC.
- **vLLM:** Study PagedAttention, KV-cache management and continuous batching. Its CPU installation path does not make the full serving stack a practical first choice for this older desktop.
- **TensorRT-LLM:** Keep as a reference for modern NVIDIA GPU optimization. The researched support matrix does not list the GT 730, so I should not target it on this PC.

## 3. First experiment principle

I should choose one small, known-compatible GGUF model and one quantization variant to validate the llama.cpp toolchain. Then I can increase model size or change quantization one variable at a time.

I should not begin by trying to load a 30B or 70B model. The model-size figures in the project roadmap are investigation targets, not guarantees for this machine. A model that loads but generates too slowly to be useful is not a successful practical configuration.

## 4. Measurements to record

For each experiment, I should capture:

- Model name, exact file, format, quantization and file size
- Runtime version or commit and build configuration
- Exact launch command and context length
- Model load time
- Peak and steady-state system RAM
- Dedicated and shared GPU memory
- CPU and GPU utilization
- Time to first token
- Generation speed in tokens per second
- Prompt length and number of generated tokens
- Temperature and throttling, if available
- Output quality using the same fixed prompt set
- Crashes, out-of-memory errors and whether the result repeats

I have not collected these benchmark measurements yet. They are the measurements needed for the next experimental stage, not results already achieved.

## 5. Open hardware and compatibility checks

Before testing GPU acceleration, I still need to establish:

1. The exact GT 730 board variant and memory type.
2. Which Vulkan version and features its installed driver exposes.
3. Whether the GPU's CUDA capability is supported by any candidate runtime and its current dependencies.
4. Which CPU instruction sets the i5-4570 exposes.
5. How much system RAM is available after Windows and background applications are running.
6. Which model files have licenses suitable for the intended use.

## 6. Current decision

**Proceed with a CPU-first llama.cpp proof of concept.** Treat MLC LLM as the next conditional candidate after hardware checks. Keep PowerInfer, FlexGen, ExLlamaV2, vLLM and TensorRT-LLM as research references for the techniques and trade-offs identified in the repository comparison.

This is a research-based implementation recommendation. No runtime has yet been benchmarked on this PC, and no performance or model-size result is being claimed.
