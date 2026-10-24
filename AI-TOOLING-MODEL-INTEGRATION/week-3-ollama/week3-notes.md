# WEEK THREE NOTES

## 1. What are Local LLMs?

LLM stands for **Large Language Model**. A local LLM is a language model
that runs on your own computer instead of running on a remote server.

When you type a prompt, the model uses your computer's resources to
generate an answer.

### Hosted AI vs. Local AI

**Hosted AI** - The model runs on a provider's remote servers. - Your
application sends a request over the internet and receives a response. -
Access may depend on the provider's service, limits, and API setup.

**Local AI** - The model runs on your own computer. - It can generate
answers without sending each prompt to an online AI service. - It uses
local resources such as RAM and CPU, and may use a compatible GPU.

**Example:** In this week's work, I ran `llama3.2:1b` locally using
Ollama and tested its local API.

## 2. Ollama

### What is Ollama?

Ollama is a tool that makes it easier to download and run language
models on your computer. It can run models in a terminal and provides a
local HTTP API so other applications can send prompts to a model.

**Official download page:** https://ollama.com/download

### Installation and model used

I installed Ollama on Windows and checked the installation using:

``` cmd
ollama --version
```

My terminal showed:

``` text
ollama version is 0.4.0.9
```

I checked which models were available using:

``` cmd
ollama list
```

The model I downloaded was:

``` text
llama3.2:1b
```

### Running a local model

I ran the model using:

``` cmd
ollama run llama3.2:1b
```

Ollama opened an interactive prompt. I entered a question asking it to
explain local LLMs in simple sentences, and the model generated an
answer.

### Testing the Ollama API

Ollama's local API uses this address:

``` text
http://localhost:11434
```

`localhost` means the service is running on the same computer. The
`/api/generate` endpoint generates a response from the selected model.

I tested it with this command:

``` cmd
curl http://localhost:11434/api/generate -d "{\"model\":\"llama3.2:1b\",\"prompt\":\"Explain local LLMs in 2 simple sentences.\",\"stream\":false}"
```

Important parts of the request:

-   `model`: selects `llama3.2:1b`.
-   `prompt`: contains the question sent to the model.
-   `stream: false`: asks for one complete JSON response rather than a
    stream of partial responses.

**Result:** The command returned JSON containing the model name,
generated response, and timing/token information.

**What I learned:** Ollama can run a model locally and let another
application communicate with it through an HTTP API. This local test did
not require an online provider API key.

## 3. llama.cpp

### What is llama.cpp?

`llama.cpp` is a project for running language models locally. It
includes command-line programs, including `llama-cli`, that can load a
compatible model and generate text.

**Official repository:** https://github.com/ggml-org/llama.cpp

### Download and installation

From the repository's releases page, I selected **Windows x64 (CPU)**
because my PC uses a 64-bit Intel processor. I downloaded the prebuilt
archive and extracted it.

**Official releases page:**
https://github.com/ggml-org/llama.cpp/releases

I checked that the command-line program worked by running:

``` cmd
llama-cli --version
```

The output showed:

``` text
version: 0.7.0-dev (build 11840, commit 36e36e63a)
built with Clang 20.1.8 for Windows x86_64
```

This confirmed that the `llama-cli` executable could start.

### What is GGUF?

GGUF(GPT-Generated Unified Format) is a model file format used by llama.cpp. A compatible GGUF file
contains the model data and information needed by the program to load
it.

### Model used: Qwen3.5-0.8B

**Model page:** https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF

I used the `Qwen3.5-0.8B-GGUF` model repository and loaded the file:

``` text
Qwen3.5-0.8B-Q4_0.gguf
```

The `0.8B` part refers to a model with about 0.8 billion parameters.
`Q4_0` is a 4-bit quantization format. Quantization stores model values
at a lower precision and can reduce the memory needed to run a model,
though it can affect output quality.

### Running the model

I ran this command from the folder containing `llama-cli`:

``` cmd
llama-cli -hf ggml-org/Qwen3.5-0.8B-GGUF -hff Qwen3.5-0.8B-Q4_0.gguf -c 4096
```

Meaning of the main options:

-   `-hf`: identifies the model repository on Hugging Face.
-   `-hff`: selects the GGUF file.
-   `-c 4096`: sets the context size to 4096 tokens for this run.

The terminal showed the model name, `Q4_0` format, and text modality
after loading.

### Test result

I tried prompts such as `hi` and simple questions. The model sometimes
produced replies such as `Hello there!`, showing that it could generate
text. At other times, it displayed a long thinking trace and did not
give a clear final answer.

**Result:** The model downloaded, loaded, and generated some responses,
but its visible response behaviour was inconsistent during my test.

## 4. Ollama vs. llama.cpp

  -----------------------------------------------------------------------
  Point                   Ollama                  llama.cpp
  ----------------------- ----------------------- -----------------------
  Main purpose            Conveniently download   Run models through
                          and run models;         command-line tools and
                          provides a local API    other interfaces

  Model tested            `llama3.2:1b`           `Qwen3.5-0.8B-Q4_0`

  How I ran it            `ollama run`            `llama-cli`

  API test                Tested `/api/generate`  Tested command-line
                          at `localhost:11434`    inference

  Observed result         Returned a model answer Loaded the model and
                          in the terminal and     generated some replies,
                          JSON from the API       but sometimes showed a
                                                  long thinking trace
  -----------------------------------------------------------------------

### What I learned from the comparison

Both tools can run language models locally, but they offer different
workflows.

-   **Ollama** was straightforward to install, run, and test through a
    local API.
-   **llama.cpp** required downloading a Windows build and choosing a
    GGUF model, and it gave direct control through command-line options.
-   In my tests, the Ollama API returned a clear JSON response. The
    llama.cpp model loaded successfully, but its visible response was
    not always clear.
-   I did not perform a controlled comparison of RAM usage or response
    speed, so I have not recorded a measured winner for those areas.

## 5. Important Terms

  -----------------------------------------------------------------------
  Term                                Easy meaning
  ----------------------------------- -----------------------------------
  Local LLM                           A language model running on your
                                      own computer

  Hosted AI                           An AI model running on a remote
                                      server

  Inference                           Using a trained model to generate
                                      an answer

  Local API                           An endpoint that an application can
                                      call on the same computer

  `localhost`                         Refers to the current computer

  GGUF                                A model file format used by
                                      llama.cpp

  Quantization                        Storing model values at lower
                                      precision to reduce resource needs

  `llama-cli`                         A command-line program included
                                      with llama.cpp

  Context size                        The token capacity set for the
                                      model's current run
  -----------------------------------------------------------------------

**Remember:** Ollama provides a convenient local model workflow and API.
llama.cpp provides direct ways to run compatible models, including GGUF
files, from the command line.
