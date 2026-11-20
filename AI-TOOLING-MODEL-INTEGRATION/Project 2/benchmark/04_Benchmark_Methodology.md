# My Benchmark Methodology

## SSD and HDD comparison
I used the same Qwen3.5-4B Q4_K_M GGUF file, llama.cpp server, context setting `-c 2048`, four CPU threads, CPU-only mode `-ngl 0`, mmap loading, local server address and the same Python-variable explanation prompt.

### SSD command
```cmd
..\llamacpp\llama-server.exe -m "Qwen3.5-4B-Q4_K_M.gguf" -c 2048 -t 4 -ngl 0 --load-mode mmap --host 127.0.0.1 --port 8080
```

### HDD command
```cmd
..\llamacpp\llama-server.exe -m "D:\Project2\models\Qwen3.5-4B-Q4_K_M.gguf" -c 2048 -t 4 -ngl 0 --load-mode mmap --host 127.0.0.1 --port 8080
```

## How I estimated the additional values
- **VRAM:** I used the approximately 0.6 GB dedicated-memory reading visible in Task Manager during the GPU-layer runs.
- **Model-load time:** I calculated the elapsed time between the server's `loading model` and `model loaded` log timestamps: about 4.0 seconds for SSD and 4.6 seconds for HDD.
- **First-response latency:** I used the prompt-processing completion time in the logs: about 14.1 seconds for SSD and 13.2 seconds for HDD.
- **Practical context:** I used 4096 because I had already run the 4B model with that context setting.
- **Temperature:** I estimated 70–85°C under sustained full CPU load, based on the CPU class and workload.
- **Stability:** I based the short-run stability assessment on successful model loading and completed responses.
- **Output quality:** I reviewed the sample answers and rated basic explanatory quality around 7/10.

## My interpretation
The 4B model is executable on my PC, but memory use is high. CPU inference is the dependable baseline. The GT 730 experiments did not show a useful speed increase. mmap worked from both storage devices; the HDD showed more intense disk activity during loading. Once generation started, SSD and HDD speeds were close in these runs.

These estimates give me a practical engineering picture of the machine and its current limits. They are based on my existing logs and observations, without additional model downloads or stress tests.
