# API Test Results

## Test environment
- Backend: FastAPI running locally at `http://127.0.0.1:8000`
- API endpoint: `POST /api/chat`
- API testing: FastAPI `/docs`
- Frontend: local `index.html` served with Live Server

## Backend tests

| # | Test case | Expected result | Actual result | Status |
|---|---|---|---|---|
| 1 | Valid prompt with OpenAI | HTTP 200 with an AI reply | HTTP 502: `The OpenAI provider request failed.` | Failed / unresolved |
| 2 | Valid prompt with Gemini | HTTP 200 with an AI reply | HTTP 200; Gemini returned a reply | Passed |
| 3 | Missing OpenAI API key | HTTP 503 with a configuration error | HTTP 503: `OpenAI API key is not configured.` | Passed |
| 4 | Missing Gemini API key | HTTP 503 with a configuration error | HTTP 503: `Gemini API key is not configured.` | Passed |
| 5 | Invalid Gemini API key | Provider error handled by backend | HTTP 502: `The Gemini provider request failed.` | Passed, assuming the test used the temporary invalid key |
| 6 | Invalid Gemini model | Provider error handled by backend | HTTP 502: `The Gemini provider request failed.` | Passed |
| 7 | Empty message | HTTP 422 validation error | HTTP 422; message must contain at least one character | Passed |

The missing `message` field and whitespace-only message cases were skipped.

## Frontend tests

| # | Test case | Expected result | Actual result | Status |
|---|---|---|---|---|
| 1 | Send a prompt using OpenAI | AI reply appears | Frontend displayed `The OpenAI provider request failed. (HTTP 502)` | Failed / unresolved |
| 2 | Send a prompt using Gemini | AI reply appears | Gemini reply displayed correctly | Passed |
| 3 | Backend unavailable | Clear error appears without crashing | Frontend displayed: `Cannot reach the backend. Make sure FastAPI is running at 127.0.0.1:8000.` | Passed |
| 4 | Backend restarted | Chat works again | Gemini returned a reply after FastAPI restarted | Passed |

## Summary
- Gemini chat works through both the backend API and frontend.
- Missing API keys and invalid Gemini model/key errors were handled with controlled HTTP errors.
- Empty messages are rejected by request validation.
- The frontend shows a clear message when the backend is unavailable and works again after the backend restarts.
- OpenAI requests returned HTTP 502 during testing. The cause was not confirmed, so OpenAI success is not marked as passed.

## Notes
- Never commit real API keys. Keep `.env` out of Git and use `.env.example` with placeholder values if needed.
- Restore the real Gemini API key and normal model setting in `.env` after testing.
- Do not include real API keys in this report.
