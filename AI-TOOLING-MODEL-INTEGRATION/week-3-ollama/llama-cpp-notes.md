# llama.cpp Notes

## 1. What is llama.cpp?

`llama.cpp` is an open-source project that runs large language models
locally on a computer. It supports CPU inference and can also use
supported GPU backends when the required build and hardware are
available.

Unlike Ollama, which provides a convenient model manager and local API,
llama.cpp provides command-line tools and a server for running model
files directly.

## 2. Where I downloaded it

I used the official llama.cpp GitHub repository:

-   Repository: https://github.com/ggml-org/llama.cpp
-   README / Quick start:
    https://github.com/ggml-org/llama.cpp/blob/master/README.md
-   Pre-built Windows binaries: linked from the repository's README and
    releases page.

I downloaded the Windows x64 CPU build archive named:

``` text
llama-b11840-bin-win-cpu-x64
```

I extracted it and used the files from the extracted folder in Command
Prompt. The folder included `llama-cli.exe` and supporting DLL files.

## 3. Check the installation

I opened Command Prompt in the extracted llama.cpp folder and ran:

``` cmd
llama-cli --version
```

The output showed:

``` text
version: 0.7.0-dev (build 11840, commit 36e36e63a)
built with Clang 20.1.8 for Windows x86_64
```

This confirmed that the command-line program could run on Windows.

## 4. Download and run a model

I used the Qwen3.5-0.8B GGUF model published by `ggml-org` on Hugging
Face:

-   Model page: https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF

Command used:

``` cmd
llama-cli -hf ggml-org/Qwen3.5-0.8B-GGUF -hff Qwen3.5-0.8B-Q4_0.gguf -c 4096
```

What the options mean:

-   `llama-cli`: starts the command-line chat program.
-   `-hf`: identifies the model repository on Hugging Face.
-   `-hff`: selects the GGUF model file.
-   `-c 4096`: sets the context size to 4096 tokens.

The program downloaded the selected model file, loaded it, and opened an
interactive prompt.

## 5. Model format and quantization

The model file used was `Qwen3.5-0.8B-Q4_0.gguf`.

-   **GGUF:** a file format used by llama.cpp to store model weights and
    related model information.
-   **Q4_0:** a 4-bit quantization format. Quantization reduces the
    space needed to store model weights, which can make a model easier
    to run on a computer with limited memory.
-   **0.8B:** indicates a model with roughly 0.8 billion parameters.

The terminal identified the model format as `Q4_0` and the modality as
text.

## 6. Testing the model

I tested the model with prompts including:

``` text
Explain local LLMs in 2 simple sentences.
Reply with exactly one word: bye
The capital of France is
hi
```

The model generated responses in the terminal. However, some prompts
produced long visible `[Start thinking]` or reasoning-style text, and
one-word instructions were not always followed as expected. This shows
that a local model can run successfully while still producing imperfect
or unexpected responses.

The test screenshot is saved as:

``` text
screenshots/04-llama-cpp-model-test.png
```

## 7. Performance observation

The terminal displayed prompt-processing and generation speeds, for
example values around `91 tokens/s` for prompt processing and
`22.9 tokens/s` for generation in one captured run. These are
measurements from that particular run, not guaranteed or average speeds.

The selected archive was the Windows x64 **CPU** build, so this test was
performed using that build rather than a CUDA-specific llama.cpp build.

## 8. Important commands

Check the version:

``` cmd
llama-cli --version
```

Run the downloaded Hugging Face model:

``` cmd
llama-cli -hf ggml-org/Qwen3.5-0.8B-GGUF -hff Qwen3.5-0.8B-Q4_0.gguf -c 4096
```

Exit the interactive session:

``` text
/exit
```

## Summary

I downloaded the Windows x64 CPU build of llama.cpp from its official
GitHub project, verified `llama-cli`, and ran the Qwen3.5-0.8B GGUF
model from Hugging Face. The model loaded and generated responses
locally. The tests also showed that a successful model run does not
guarantee that every response will follow the prompt exactly.
