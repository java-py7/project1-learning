# My Benchmark Test Matrix

My test machine: Intel Core i5-4570, 16 GB RAM, NVIDIA GT 730, Windows 10, SSD C: and HDD D:. GGUF tests used llama.cpp build 11840.

| ID | Model / runtime | Configuration | Storage / context | My result |
|---|---|---|---|---|
| B01 | Qwen3.5-0.8B Q4_0 / llama.cpp | CPU | C:, 4096 | 19.85–20.46 tokens/s |
| B02 | llama3.2:1b / Ollama | CPU | Local, 4096 | 293 tokens in 22.939 s; 12.77 t/s generation; 65.24 t/s prompt evaluation |
| B03 | Qwen3.5-4B Q4_K_M / llama.cpp | CPU | C:, 4096 | 4.3–4.7 t/s |
| B04 | Qwen3.5-4B / llama.cpp | `-t 4 -ngl 0` | C:, 2048 | 4.32–4.59 t/s; RAM around 12.7 GB |
| B05 | Qwen3.5-4B / llama.cpp | `-ngl 1` | C:, 2048 | 4.51–4.71 t/s; around 0.6 GB dedicated GPU memory in the captured snapshot |
| B06 | Qwen3.5-4B / llama.cpp | `-ngl 5` | C:, 2048 | Around 4.52 t/s; around 0.6 GB dedicated GPU memory in the captured snapshot |
| B07 | Qwen3.5-4B / llama.cpp | CPU, mmap, `-t 4 -ngl 0` | SSD C:, 2048 | RAM 12.6 GB; prompt 24.17 t/s; generation about 4.1 t/s |
| B08 | Qwen3.5-4B / llama.cpp | CPU, mmap, `-t 4 -ngl 0` | HDD D:, 2048 | RAM 12.4 GB; prompt 25.86 t/s; generation 3.9–4.5 t/s |

## Additional estimates from my existing runs

| Metric | My estimated result | How I derived it |
|---|---|---|
| VRAM during GPU-layer tests | About 0.6 GB dedicated VRAM used | Task Manager snapshots during `-ngl 1` and `-ngl 5` |
| SSD model-load time | About 4.0 seconds | Server log: loading started around 0.05 s; model loaded around 4.08 s |
| HDD model-load time | About 4.6 seconds | Server log: loading started around 0.05 s; model loaded around 4.63 s |
| SSD first response latency | About 14 seconds | Prompt processing completed around 14.11 s |
| HDD first response latency | About 13 seconds | Prompt processing completed around 13.18 s |
| Practical context used | 4096 tokens | I successfully ran the 4B model at 4096 in an earlier test |
| Expected CPU temperature under sustained load | Roughly 70–85°C | Estimate based on 100% CPU utilization on this older desktop CPU; actual cooling can shift this |
| Short-run stability | Stable during the recorded short sessions | Model loaded and generated output in each completed run |
| Output quality | Around 7/10 for simple explanations | Answers were generally understandable; one response was incomplete |

I treat 4096 as my highest demonstrated context setting, not a tested hardware limit. My 4B model used around 12.4–13.0 GB RAM, so I consider 4096 a practical upper tested setting on this 16 GB machine. I expect longer sessions or other open applications to increase memory pressure.
