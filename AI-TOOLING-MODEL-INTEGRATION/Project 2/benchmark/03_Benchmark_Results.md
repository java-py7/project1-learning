# My Benchmark Results

## Small-model performance
Qwen3.5-0.8B Q4_0 ran through llama.cpp at approximately 19.85–20.46 tokens/second. Ollama `llama3.2:1b` generated 293 tokens in 22.939 seconds, with 12.77 t/s generation and 65.24 t/s prompt evaluation.

## Qwen3.5-4B Q4_K_M
The 4B model generated approximately 4.0–4.7 tokens/second. RAM usage reached around 12.4–13.0 GB of my 16 GB, while CPU utilization reached 100%. Based on this, I decided not to test larger models on this PC.

## GPU usage
I tested `-ngl 1` and `-ngl 5`. Task Manager showed around 0.6 GB dedicated GPU memory during the captured runs. Generation speed remained close to CPU-only performance, so the GT 730 did not provide a meaningful speed improvement in my tests.

## SSD and HDD loading
I ran the same Qwen3.5-4B model with mmap, context 2048, four CPU threads and no GPU layers.

| Metric | SSD (C:) | HDD (D:) |
|---|---:|---:|
| Estimated model-load time | ~4.0 s | ~4.6 s |
| Prompt processing | 24.17 t/s | 25.86 t/s |
| Generation | ~4.1 t/s | ~3.9–4.5 t/s |
| RAM usage | 12.6 GB | 12.4 GB |
| Disk activity | Brief activity during loading, low afterwards | Briefly reached nearly 100% active time |

Both drives successfully loaded the model. The HDD had a larger disk-activity spike, but generation speed was broadly similar once the model was running.

## Latency
From the server logs, prompt processing completed at approximately 14.11 seconds on SSD and 13.18 seconds on HDD. I use these as approximate first-response latency values for this comparison. Model-load time was approximately 4.0 seconds on SSD and 4.6 seconds on HDD.

## Context capacity
I successfully ran the 4B model with a 4096-token context setting in an earlier test. I therefore use 4096 as my practical tested context setting. Since the model already uses around 12.4–13.0 GB RAM, I expect larger context settings to put substantial pressure on the remaining memory.

## Temperature and stability
During inference, CPU utilization reached 100%. Based on the CPU workload and typical cooling behaviour for this class of desktop, I estimate sustained CPU temperature could be around 70–85°C. I consider this a rough engineering estimate, not a sensor reading.

The model completed the recorded short inference sessions without crashing. I consider short-run operation stable, while longer sessions may be affected by high RAM use and sustained CPU load.

## Output quality
The simple Python explanation prompts produced generally clear and understandable answers. One generated response contained an incomplete code example. Based on these samples, I rate the output quality at approximately 7/10 for basic explanatory tasks. This is my qualitative assessment rather than a formal evaluation score.
