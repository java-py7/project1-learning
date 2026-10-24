# Ollama Logs and Performance Observations

## 1. Installation and version check

**Command:**

``` cmd
ollama --version
```

**Observed output:**

``` text
ollama version is 0.40.9
```

Ollama was installed successfully and its command-line tool worked.

## 2. Downloaded model

**Command:**

``` cmd
ollama list
```

**Observed model:**

``` text
NAME           SIZE
llama3.2:1b    1.3 GB
```

The `llama3.2:1b` model was downloaded and available locally.

## 3. Run the model

**Command:**

``` cmd
ollama run llama3.2:1b
```

I entered prompts such as `hi` and `create an one week study timetable`.
The model generated answers directly in the Command Prompt.

## 4. Local API test

Ollama provides a local HTTP API at `http://localhost:11434`.

**Endpoint tested:**

``` text
POST http://localhost:11434/api/generate
```

**Command used:**

``` cmd
curl http://localhost:11434/api/generate -d "{\"model\":\"llama3.2:1b\",\"prompt\":\"Explain local LLMs in 2 simple sentences.\",\"stream\":false}"
```

**Observed result:** The request returned JSON containing the model
name, generated response, completion status, and timing/token
statistics. The response included `"done": true`, confirming that
generation finished.

## 5. Server logs

The supplied Ollama server logs show that the local server started
successfully:

``` text
Listening on 127.0.0.1:11434 (version 0.40.9)
```

The logs also show successful API requests. For example:

``` text
200 ... POST "/api/generate"
```

HTTP status `200` means the API request succeeded. The logs also record
requests such as `GET /api/tags`, which Ollama uses to list available
models.

## 6. Hardware detection

The server log detected the following system resources:

``` text
CPU: Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz
System memory: 16.0 GiB
Inference compute: CPU
Available memory at detection: approximately 7.0–9.5 GiB
```

The Task Manager screenshot showed the NVIDIA GeForce GT 730 (4 GB) and
16 GB of RAM. The Ollama log reported CPU inference and
`total_vram="0 B"`, so the model was running on the CPU rather than
using GPU VRAM for inference.

## 7. Model loading

The server logs show the model-loading process, including:

-   Ollama started its local server.
-   Ollama launched its `llama-server` runner for `llama3.2:1b`.
-   The model file was loaded into CPU memory.
-   The logs reported a CPU model buffer of about `1252 MiB`.
-   The runner reported `model loaded` and began listening on a local
    port.
-   The `/api/generate` request then completed successfully.

These entries are evidence of model loading and local inference, rather
than just the interactive command working.

## 8. Performance observations

The Task Manager screenshot taken while the model was responding showed:

-   CPU usage: approximately 75%
-   Memory usage: 9.2 / 16.0 GB (57%)
-   GPU usage: 0% at the moment captured

These are observations from one screenshot, not fixed or average usage
values. Usage changes with the prompt and while the model is loading or
generating.

The API JSON response also included fields such as `prompt_eval_count`,
`eval_count`, `prompt_eval_duration`, `eval_duration`, `load_duration`,
and `total_duration`. These fields report token counts and durations for
that particular request.

## 9. Evidence files

The following evidence was collected during testing:

-   `screenshots/01-ollama-model.png` --- interactive Ollama model
    response
-   `screenshots/02-ollama-api.png` --- local API request and JSON
    response
-   `screenshots/03-llama-cpp-version.png` --- llama.cpp version
-   `screenshots/04-llama-cpp-model-test.png` --- Qwen model loaded and
    tested with llama.cpp
-   `server.log` and `server-1.log` --- Ollama server logs supplied for
    review
-   Task Manager screenshot --- CPU, memory, and GPU usage at the time
    of the test

## Summary

Ollama `0.40.9` ran `llama3.2:1b` locally. The local `/api/generate`
endpoint returned a completed JSON response, and the server logs
recorded successful requests and model-loading events. The logs show
CPU-based inference on the tested PC. The resource measurements above
are observations from the captured run, not general performance
guarantees.
