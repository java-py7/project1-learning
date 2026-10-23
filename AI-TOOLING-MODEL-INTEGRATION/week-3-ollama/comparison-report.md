# Comparison Report: Ollama vs. llama.cpp

## 1. Objective

The objective was to run local language models with Ollama and
llama.cpp, test their responses, and compare the setup process, hardware
usage, speed observations, and developer experience.

## 2. Setup and models used

  --------------------------------------------------------------------------------------------------------------------------------------
  Item                    Ollama                        llama.cpp
  ----------------------- ----------------------------- --------------------------------------------------------------------------------
  Official download       https://ollama.com/download   https://github.com/ggml-org/llama.cpp/releases
  source                                                

  Model source            Ollama model library          https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF

  Model tested            `llama3.2:1b`                 `Qwen3.5-0.8B-Q4_0.gguf`

  Run command             `ollama run llama3.2:1b`      `llama-cli -hf ggml-org/Qwen3.5-0.8B-GGUF -hff Qwen3.5-0.8B-Q4_0.gguf -c 4096`

  Interface tested        Terminal chat and local HTTP  Command-line chat
                          API                           
  --------------------------------------------------------------------------------------------------------------------------------------

The tools used different models, so this was a practical workflow
comparison, not a controlled benchmark.

## 3. Developer experience

### Ollama

-   Installed from the official Ollama download page.
-   Downloaded and ran `llama3.2:1b`.
-   Tested chat through `ollama run`.
-   Sent a request to `http://localhost:11434/api/generate`.
-   Received a JSON response containing the model's answer and
    timing/token information.

### llama.cpp

-   Downloaded the prebuilt Windows x64 CPU archive from the official
    GitHub releases page.
-   Checked the executable with `llama-cli --version`.
-   Loaded a Qwen GGUF model from Hugging Face.
-   Generated a response to `hi`, including
    `Hello! How can I help you today?`

**Observation:** Ollama was simpler to start and test through an API.
llama.cpp involved selecting a build and model file, but exposed direct
command-line options.

## 4. Hardware and resource usage

The PC used for both tests had:

-   **CPU:** Intel Core i5-4570 @ 3.20 GHz
-   **RAM:** 16 GB
-   **GPU:** NVIDIA GeForce GT 730 (4 GB)

### Ollama observation

From the supplied Ollama Task Manager screenshot and server logs:

-   CPU usage in the screenshot: approximately 75%.
-   Memory usage in the screenshot: 9.2 / 16.0 GB (57%).
-   GPU usage at the moment captured: 0%.
-   Ollama logs identified CPU inference and reported
    `total_vram="0 B"`.
-   The log reported a CPU model buffer of about 1252 MiB while loading
    `llama3.2:1b`.

### llama.cpp observation

The new Task Manager screenshot, captured while `llama-cli` was
generating a response, showed:

-   CPU usage: approximately **93%**.
-   Memory usage: **10.1 / 16.0 GB (63%)**.
-   GPU usage: **0%**.
-   CPU speed at that moment: approximately 3.17 GHz.

These are snapshots taken at different moments while using different
models. They suggest that CPU usage was high during both local inference
tests, but they do not prove which tool is generally more
resource-efficient.

## 5. Response speed and output

### Ollama

-   The `/api/generate` request completed and returned JSON.
-   The response included `load_duration`, `prompt_eval_duration`,
    `eval_duration`, and `total_duration`.
-   The terminal model responded to prompts such as `hi` and a request
    to create a one-week study timetable.

### llama.cpp

-   The terminal showed prompt-processing and generation speeds. One
    captured run showed about **76.4 tokens/s prompt processing** and
    **23.4 tokens/s generation**.
-   The model returned `Hello! How can I help you today?` for the prompt
    `hi`.
-   Other prompts sometimes produced long visible thinking text or did
    not follow short instructions as expected.

The displayed speed numbers are from individual runs, not averages.
Ollama and llama.cpp used different models, and the Ollama JSON timing
fields are not directly comparable to the llama.cpp terminal speed
display. Therefore, these results are observations, not a fair speed
ranking.

## 6. Comparison summary

  -----------------------------------------------------------------------
  Category                Ollama                  llama.cpp
  ----------------------- ----------------------- -----------------------
  Setup                   Install Ollama, then    Download/extract CPU
                          download/run a model    build and select a GGUF
                                                  model

  Local inference         Confirmed; generated    Confirmed; generated
                          responses               responses

  API                     `/api/generate` tested  No llama.cpp API server
                          successfully            was tested

  CPU/RAM screenshot      About 75% CPU, 9.2/16   About 93% CPU, 10.1/16
                          GB RAM                  GB RAM

  GPU at capture          0%; logs indicated CPU  0%
                          inference               

  Speed evidence          API returned timing     One run showed 76.4
                          fields; no average      tokens/s prompt
                          calculated              processing and 23.4
                                                  tokens/s generation

  Response behaviour      Clear terminal answer   Clear greeting in the
                          and successful API JSON latest screenshot; some
                                                  other prompts showed
                                                  long thinking text
  -----------------------------------------------------------------------

## 7. Conclusion

Both tools successfully ran a local model on this PC. Ollama was more
convenient for running a model and calling it through a local HTTP API.
llama.cpp required a separate Windows CPU build and GGUF model
selection, and provided direct command-line control.

In the latest screenshots, CPU usage was high and GPU usage was 0%
during both tests. The llama.cpp screenshot showed 93% CPU and 63% RAM
usage; the Ollama screenshot showed 75% CPU and 57% RAM usage. Since the
screenshots were captured at different moments with different models and
prompts, these figures should not be treated as a controlled comparison
or proof that one tool is always faster or more efficient.

A more accurate benchmark would run the same compatible model with
comparable context and generation settings in both tools, repeat each
test, and record average generation speed, CPU usage, RAM usage, and
response quality.

## 8. Evidence

Screenshots in the `screenshots` folder:

-   `01-ollama-model.png` --- Ollama terminal response
-   `02-ollama-api.png` --- local API request and JSON response
-   `03-llama-cpp-version.png` --- llama.cpp version output
-   `04-llama-cpp-model-test.png` --- llama.cpp model response and Task
    Manager performance

Related files:

-   `week3-notes.md`
-   `ollama-logs.md`
-   `llama-cpp-notes.md`
