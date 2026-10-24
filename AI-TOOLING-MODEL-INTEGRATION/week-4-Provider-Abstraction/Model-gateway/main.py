import os
import ipaddress
import socket
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Configuration and Initialization
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent

# Explicitly load .env file from the project directory
load_dotenv(dotenv_path=APP_DIR / ".env")

try:
    TIMEOUT = float(os.getenv("PROVIDER_TIMEOUT_SECONDS", "45"))
except ValueError:
    TIMEOUT = 45.0

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
LLAMACPP_URL = os.getenv("LLAMACPP_BASE_URL", "http://127.0.0.1:8080").rstrip("/")

cors_env = os.getenv(
    "CORS_ORIGINS",
    "http://127.0.0.1:8000,http://localhost:8000,http://127.0.0.1:5500,http://localhost:5500",
)
FRONTEND_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

app = FastAPI(
    title="Model Gateway",
    description="Unified API gateway abstraction for Cloud and Local AI models",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Request & Response Models
# -----------------------------------------------------------------------------
class ChatRequest(BaseModel):
    category: str = Field(pattern="^(cloud|local)$")
    provider: str = Field(min_length=1, max_length=40)
    model: str = Field(min_length=1, max_length=160)
    message: str = Field(min_length=1, max_length=12000)
    custom_base_url: str | None = Field(default=None, max_length=500)


class TestRequest(BaseModel):
    category: str = Field(pattern="^(cloud|local)$")
    provider: str = Field(min_length=1, max_length=40)
    model: str | None = Field(default=None, max_length=160)
    custom_base_url: str | None = Field(default=None, max_length=500)


# -----------------------------------------------------------------------------
# Security & Helper Functions
# -----------------------------------------------------------------------------
def validate_custom_url(url: str | None) -> str:
    """Validate user-supplied custom OpenAI-compatible base URLs to prevent SSRF."""
    if not url or not url.strip():
        raise HTTPException(
            status_code=400,
            detail="A custom OpenAI-compatible base URL is required.",
        )

    clean_url = url.strip().rstrip("/")
    parsed = urlparse(clean_url)

    if parsed.scheme.lower() != "https":
        raise HTTPException(
            status_code=400,
            detail="Custom API URLs must use HTTPS. Unencrypted HTTP is prohibited.",
        )

    if not parsed.hostname:
        raise HTTPException(
            status_code=400,
            detail="Custom API URL must include a valid hostname.",
        )

    if parsed.username or parsed.password:
        raise HTTPException(
            status_code=400,
            detail="Custom API URLs must not contain embedded user credentials.",
        )

    host = parsed.hostname.lower()

    if (
        host in ("localhost", "localhost.localdomain")
        or host.endswith(".local")
        or host.endswith(".internal")
    ):
        raise HTTPException(
            status_code=400,
            detail="Localhost and internal domain names are forbidden for custom cloud endpoints.",
        )

    port = parsed.port or 443

    # Check if host is a raw IP literal
    try:
        ip = ipaddress.ip_address(host)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or not ip.is_global
        ):
            raise HTTPException(
                status_code=400,
                detail="Private and local IP addresses are forbidden for custom cloud endpoints.",
            )
        return clean_url
    except ValueError:
        pass

    # Resolve hostname via DNS and check all returned IP addresses
    try:
        addr_info = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        if not addr_info:
            raise HTTPException(
                status_code=400,
                detail=f"Hostname '{host}' could not be resolved.",
            )
        for item in addr_info:
            ip_str = item[4][0]
            ip = ipaddress.ip_address(ip_str)
            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_multicast
                or ip.is_reserved
                or not ip.is_global
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Hostname '{host}' resolves to non-public address ({ip_str}), which is blocked for security.",
                )
    except socket.gaierror:
        raise HTTPException(
            status_code=400,
            detail=f"Hostname '{host}' could not be resolved via DNS.",
        )
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise
        raise HTTPException(status_code=400, detail=f"URL validation error: {exc}")

    return clean_url


async def request_json(
    method: str,
    url: str,
    provider_label: str = "Provider",
    **kwargs,
) -> dict:
    """Execute an HTTP request with uniform timeout, error sanitization, and security rules."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=False) as client:
            response = await client.request(method, url, **kwargs)
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail=f"Request to {provider_label} timed out after {int(TIMEOUT)}s. Check network connectivity or try a faster model.",
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to {provider_label}. Verify that the service is running and the endpoint URL is accessible.",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Network error communicating with {provider_label}: {type(exc).__name__}.",
        )

    if response.status_code in (401, 403):
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed for {provider_label} (HTTP {response.status_code}). Check your API key and permissions in .env.",
        )
    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"The requested endpoint or model was not found on {provider_label} (HTTP 404).",
        )
    if response.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit or quota exceeded for {provider_label}. Check your account billing and quota limits.",
        )
    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail=f"{provider_label} returned HTTP {response.status_code}. Request could not be completed.",
        )

    try:
        return response.json()
    except Exception:
        raise HTTPException(
            status_code=502,
            detail=f"{provider_label} returned a response that is not valid JSON.",
        )


# -----------------------------------------------------------------------------
# Abstract Model Provider
# -----------------------------------------------------------------------------
class ModelProvider(ABC):
    @abstractmethod
    async def test_connection(self) -> dict:
        """Test connection and return status and discovered models."""
        ...

    @abstractmethod
    async def get_models(self) -> list[str]:
        """Discover or return supported models."""
        ...

    @abstractmethod
    async def generate(self, message: str, model: str) -> str:
        """Generate response text for the provided user message."""
        ...


# -----------------------------------------------------------------------------
# Concrete Provider Adapters
# -----------------------------------------------------------------------------
class OpenAIAdapter(ModelProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.base_url = "https://api.openai.com/v1"
        self.default_model = "gpt-4o-mini"
        self.label = "OpenAI"

    def _require_key(self):
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            raise HTTPException(
                status_code=503,
                detail="OPENAI_API_KEY is not configured in .env.",
            )

    async def get_models(self) -> list[str]:
        self._require_key()
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = await request_json(
            "GET",
            f"{self.base_url}/models",
            provider_label=self.label,
            headers=headers,
        )
        models = [
            m.get("id")
            for m in data.get("data", [])
            if isinstance(m, dict) and m.get("id")
        ]
        # Prioritize chat-compatible models
        chat_models = [m for m in models if m.startswith(("gpt-", "o1", "o3", "chatgpt"))]
        sorted_models = sorted(chat_models or models)
        return sorted_models or [self.default_model]

    async def test_connection(self) -> dict:
        models = await self.get_models()
        return {
            "status": "connected",
            "message": f"Successfully connected to OpenAI API ({len(models)} accessible models).",
            "models": models,
        }

    async def generate(self, message: str, model: str) -> str:
        self._require_key()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": [{"role": "user", "content": message}],
        }
        data = await request_json(
            "POST",
            f"{self.base_url}/chat/completions",
            provider_label=self.label,
            headers=headers,
            json=payload,
        )
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise HTTPException(
                status_code=502,
                detail="OpenAI returned an unexpected chat response format.",
            )


class GeminiAdapter(ModelProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.default_model = "gemini-1.5-flash"
        self.label = "Google Gemini"

    def _require_key(self):
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise HTTPException(
                status_code=503,
                detail="GEMINI_API_KEY is not configured in .env.",
            )

    async def get_models(self) -> list[str]:
        self._require_key()
        data = await request_json(
            "GET",
            f"{self.base_url}/models",
            provider_label=self.label,
            params={"key": self.api_key},
        )
        discovered = []
        for m in data.get("models", []):
            name = m.get("name", "")
            methods = m.get("supportedGenerationMethods", [])
            if "generateContent" in methods and name:
                discovered.append(name.removeprefix("models/"))
        return sorted(discovered) or [self.default_model]

    async def test_connection(self) -> dict:
        models = await self.get_models()
        return {
            "status": "connected",
            "message": f"Successfully connected to Google Gemini ({len(models)} content generation models).",
            "models": models,
        }

    async def generate(self, message: str, model: str) -> str:
        self._require_key()
        clean_model = (model or self.default_model).removeprefix("models/")
        if not clean_model:
            raise HTTPException(status_code=400, detail="Choose a valid Gemini model.")

        url = f"{self.base_url}/models/{clean_model}:generateContent"
        payload = {"contents": [{"parts": [{"text": message}]}]}
        data = await request_json(
            "POST",
            url,
            provider_label=self.label,
            params={"key": self.api_key},
            json=payload,
        )

        try:
            candidates = data.get("candidates", [])
            if not candidates:
                # Check for feedback or prompt blocking
                prompt_feedback = data.get("promptFeedback", {})
                block_reason = prompt_feedback.get("blockReason", "prompt was blocked by safety filters")
                raise HTTPException(
                    status_code=400,
                    detail=f"Gemini did not return a response: {block_reason}.",
                )
            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts)
            if not text:
                finish_reason = candidates[0].get("finishReason", "empty response")
                raise HTTPException(
                    status_code=502,
                    detail=f"Gemini generated an empty response (finishReason: {finish_reason}).",
                )
            return text
        except (KeyError, IndexError, TypeError):
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an unexpected candidate response structure.",
            )


class QwenAPIAdapter(ModelProvider):
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
        self.base_url = os.getenv(
            "QWEN_BASE_URL",
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        ).rstrip("/")
        self.default_model = "qwen-plus"
        self.label = "Qwen API"

    def _require_key(self):
        if not self.api_key or self.api_key == "your_dashscope_api_key_here" or self.api_key == "your_qwen_api_key_here":
            raise HTTPException(
                status_code=503,
                detail="DASHSCOPE_API_KEY is not configured in .env.",
            )

    async def get_models(self) -> list[str]:
        self._require_key()
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            data = await request_json(
                "GET",
                f"{self.base_url}/models",
                provider_label=self.label,
                headers=headers,
            )
            models = [
                m.get("id")
                for m in data.get("data", [])
                if isinstance(m, dict) and m.get("id")
            ]
            if models:
                return sorted(models)
        except Exception:
            pass

        # Configured defaults for Qwen DashScope OpenAI compatible interface
        return [
            "qwen-plus",
            "qwen-turbo",
            "qwen-max",
            "qwen-long",
            "qwen2.5-72b-instruct",
            "qwen2.5-32b-instruct",
            "qwen2.5-14b-instruct",
            "qwen2.5-7b-instruct",
        ]

    async def test_connection(self) -> dict:
        models = await self.get_models()
        return {
            "status": "connected",
            "message": f"Successfully connected to Qwen DashScope endpoint ({self.base_url}).",
            "models": models,
        }

    async def generate(self, message: str, model: str) -> str:
        self._require_key()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": [{"role": "user", "content": message}],
        }
        data = await request_json(
            "POST",
            f"{self.base_url}/chat/completions",
            provider_label=self.label,
            headers=headers,
            json=payload,
        )
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise HTTPException(
                status_code=502,
                detail="Qwen API returned an unexpected chat response format.",
            )


class CustomOpenAICompatibleAdapter(ModelProvider):
    def __init__(self, base_url: str):
        self.base_url = validate_custom_url(base_url)
        self.api_key = os.getenv("CUSTOM_API_KEY", "").strip()
        if self.api_key == "your_custom_api_key_here":
            self.api_key = ""
        self.label = "Custom OpenAI-compatible API"

    async def get_models(self) -> list[str]:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        data = await request_json(
            "GET",
            f"{self.base_url}/models",
            provider_label=self.label,
            headers=headers,
        )
        models = [
            m.get("id")
            for m in data.get("data", [])
            if isinstance(m, dict) and m.get("id")
        ]
        return sorted(models)

    async def test_connection(self) -> dict:
        models = await self.get_models()
        return {
            "status": "connected",
            "message": f"Successfully connected to custom endpoint ({len(models)} models discovered).",
            "models": models,
        }

    async def generate(self, message: str, model: str) -> str:
        if not model:
            raise HTTPException(
                status_code=400,
                detail="Model name is required for custom OpenAI-compatible endpoints.",
            )
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
        }
        data = await request_json(
            "POST",
            f"{self.base_url}/chat/completions",
            provider_label=self.label,
            headers=headers,
            json=payload,
        )
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise HTTPException(
                status_code=502,
                detail="Custom provider returned an unexpected chat response format.",
            )


class OllamaAdapter(ModelProvider):
    def __init__(self):
        self.base_url = OLLAMA_URL
        self.label = "Ollama"

    async def get_models(self) -> list[str]:
        data = await request_json(
            "GET",
            f"{self.base_url}/api/tags",
            provider_label=self.label,
        )
        models = [
            m.get("name")
            for m in data.get("models", [])
            if isinstance(m, dict) and m.get("name")
        ]
        return sorted(models)

    async def test_connection(self) -> dict:
        models = await self.get_models()
        return {
            "status": "connected",
            "message": f"Ollama is reachable at {self.base_url} ({len(models)} installed models found).",
            "models": models,
        }

    async def generate(self, message: str, model: str) -> str:
        installed_models = await self.get_models()
        if not installed_models:
            raise HTTPException(
                status_code=400,
                detail="No models are currently installed in Ollama. Pull a model using `ollama run <model>` first.",
            )
        if model not in installed_models:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{model}' is not installed in Ollama. Available: {', '.join(installed_models[:5])}. The gateway will not automatically download models.",
            )

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        data = await request_json(
            "POST",
            f"{self.base_url}/api/chat",
            provider_label=self.label,
            json=payload,
        )
        try:
            return data["message"]["content"]
        except (KeyError, TypeError):
            raise HTTPException(
                status_code=502,
                detail="Ollama returned an unexpected response format.",
            )


class LlamaCppAdapter(ModelProvider):
    def __init__(self):
        self.base_url = LLAMACPP_URL
        self.label = "llama.cpp Server"

    async def get_models(self) -> list[str]:
        data = await request_json(
            "GET",
            f"{self.base_url}/v1/models",
            provider_label=self.label,
        )
        models = [
            m.get("id")
            for m in data.get("data", [])
            if isinstance(m, dict) and m.get("id")
        ]
        return sorted(models) or ["default"]

    async def test_connection(self) -> dict:
        models = await self.get_models()
        return {
            "status": "connected",
            "message": f"llama.cpp HTTP server is running at {self.base_url}.",
            "models": models,
        }

    async def generate(self, message: str, model: str) -> str:
        payload = {
            "model": model or "default",
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        data = await request_json(
            "POST",
            f"{self.base_url}/v1/chat/completions",
            provider_label=self.label,
            json=payload,
        )
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise HTTPException(
                status_code=502,
                detail="llama.cpp server returned an unexpected response format.",
            )


# -----------------------------------------------------------------------------
# Provider Registry / Factory
# -----------------------------------------------------------------------------
def get_adapter(
    category: str,
    provider: str,
    custom_base_url: str | None = None,
) -> ModelProvider:
    if category == "local":
        if provider == "ollama":
            return OllamaAdapter()
        if provider == "llamacpp":
            return LlamaCppAdapter()
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported local runtime '{provider}'. Choose 'ollama' or 'llamacpp'.",
        )

    if category == "cloud":
        if provider == "openai":
            return OpenAIAdapter()
        if provider == "gemini":
            return GeminiAdapter()
        if provider == "qwen":
            return QwenAPIAdapter()
        if provider == "custom":
            if not custom_base_url:
                raise HTTPException(
                    status_code=400,
                    detail="A valid HTTPS base URL is required for the Custom OpenAI-compatible provider.",
                )
            return CustomOpenAICompatibleAdapter(custom_base_url)
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported cloud provider '{provider}'.",
        )

    raise HTTPException(
        status_code=400,
        detail="Category must be either 'cloud' or 'local'.",
    )


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------
@app.get("/")
async def root_index():
    """Serve the single-page frontend application from index.html."""
    index_file = APP_DIR / "index.html"
    if not index_file.is_file():
        raise HTTPException(
            status_code=500,
            detail="Frontend file index.html is missing. Please ensure index.html exists in the project root.",
        )
    return FileResponse(index_file)


@app.get("/api/health")
async def health_check():
    """Return backend operational status."""
    return {
        "status": "ok",
        "application": "Model Gateway",
        "version": "1.0.0",
    }


@app.get("/api/providers")
async def list_providers():
    """Return supported categories, providers, default models, and configuration status."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_configured = bool(openai_key and openai_key != "your_openai_api_key_here")

    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_configured = bool(gemini_key and gemini_key != "your_gemini_api_key_here")

    dashscope_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    dashscope_configured = bool(
        dashscope_key
        and dashscope_key != "your_dashscope_api_key_here"
        and dashscope_key != "your_qwen_api_key_here"
    )

    custom_key = os.getenv("CUSTOM_API_KEY", "").strip()
    custom_configured = bool(custom_key and custom_key != "your_custom_api_key_here")

    return {
        "categories": [
            {
                "id": "cloud",
                "name": "Cloud AI",
                "providers": [
                    {
                        "id": "openai",
                        "name": "OpenAI",
                        "default_model": "gpt-4o-mini",
                        "configured": openai_configured,
                        "requires_custom_url": False,
                    },
                    {
                        "id": "gemini",
                        "name": "Google Gemini",
                        "default_model": "gemini-1.5-flash",
                        "configured": gemini_configured,
                        "requires_custom_url": False,
                    },
                    {
                        "id": "qwen",
                        "name": "Qwen API",
                        "default_model": "qwen-plus",
                        "configured": dashscope_configured,
                        "requires_custom_url": False,
                    },
                    {
                        "id": "custom",
                        "name": "Custom OpenAI-compatible API",
                        "default_model": "",
                        "configured": custom_configured,
                        "requires_custom_url": True,
                    },
                ],
            },
            {
                "id": "local",
                "name": "Local AI",
                "providers": [
                    {
                        "id": "ollama",
                        "name": "Ollama",
                        "default_model": "",
                        "configured": True,
                        "default_url": OLLAMA_URL,
                        "requires_custom_url": False,
                    },
                    {
                        "id": "llamacpp",
                        "name": "llama.cpp Server",
                        "default_model": "",
                        "configured": True,
                        "default_url": LLAMACPP_URL,
                        "requires_custom_url": False,
                    },
                ],
            },
        ]
    }


@app.get("/api/models")
async def list_models(
    category: str = Query(..., pattern="^(cloud|local)$"),
    provider: str = Query(..., min_length=1, max_length=40),
    custom_base_url: str | None = None,
):
    """Discover installed or accessible models for the specified provider."""
    if category == "cloud" and provider == "custom":
        if not custom_base_url or not custom_base_url.strip():
            return {
                "models": [],
                "source": "manual",
                "notice": "Enter an HTTPS base URL in Settings to discover or query custom models.",
            }
        custom_base_url = validate_custom_url(custom_base_url)

    adapter = get_adapter(category, provider, custom_base_url)

    try:
        models = await adapter.get_models()
        return {
            "models": models,
            "source": "runtime" if category == "local" else "discovered",
            "notice": None,
        }
    except HTTPException as exc:
        # For cloud providers without valid keys, return sensible defaults marked clearly
        if category == "cloud":
            defaults_map = {
                "openai": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                "gemini": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.5-flash"],
                "qwen": ["qwen-plus", "qwen-turbo", "qwen-max", "qwen-long"],
                "custom": [],
            }
            fallback = defaults_map.get(provider, [])
            return {
                "models": fallback,
                "source": "defaults",
                "notice": f"{exc.detail} Showing standard default models (unverified).",
            }
        # For local runtimes, surface the actual connectivity error so users know to start the process
        raise


@app.post("/api/providers/test")
async def test_provider(body: TestRequest):
    """Perform a live connectivity and authentication test for the selected provider."""
    if body.category == "cloud" and body.provider == "custom":
        if not body.custom_base_url or not body.custom_base_url.strip():
            raise HTTPException(
                status_code=400,
                detail="Custom base URL is required to test custom provider.",
            )
        body.custom_base_url = validate_custom_url(body.custom_base_url)

    adapter = get_adapter(body.category, body.provider, body.custom_base_url)
    result = await adapter.test_connection()
    return {
        "status": "connected",
        "provider": body.provider,
        "category": body.category,
        "message": result.get("message", f"Connected to {body.provider}."),
        "models": result.get("models", []),
    }


@app.post("/api/chat")
async def chat(body: ChatRequest):
    """Process a chat completion request through the chosen provider abstraction."""
    if body.category == "cloud" and body.provider == "custom":
        if not body.custom_base_url or not body.custom_base_url.strip():
            raise HTTPException(
                status_code=400,
                detail="Custom base URL is required for custom provider.",
            )
        body.custom_base_url = validate_custom_url(body.custom_base_url)

    adapter = get_adapter(body.category, body.provider, body.custom_base_url)
    user_msg = body.message.strip()
    model_name = body.model.strip()

    if not user_msg:
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")
    if not model_name:
        raise HTTPException(
            status_code=400,
            detail="Model selection is required. Please choose a model from the dropdown.",
        )

    response_text = await adapter.generate(user_msg, model_name)

    return {
        "response": response_text,
        "provider": body.provider,
        "category": body.category,
        "model": model_name,
    }
