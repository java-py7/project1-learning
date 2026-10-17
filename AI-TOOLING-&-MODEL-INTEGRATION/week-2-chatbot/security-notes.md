## 1. API Key Protection
- OpenAI and Google Gemini API keys are stored in the backend `.env` file.
- The backend loads environment variables using `python-dotenv`.
- API keys must never be placed in `index.html`, frontend JavaScript, or other files served to the browser.
- The `.env` file should be listed in `.gitignore` so it is not committed to GitHub.
- The `.env.example` file may contain variable names and placeholder values only, never real API keys.

## 2. Backend Request Handling
- The frontend sends the user's message and selected provider to the FastAPI endpoint `POST /api/chat`.
- The backend validates the request using Pydantic.
- The message length is limited to 4,000 characters.
- Only the supported provider values `openai` and `gemini` are accepted.
- Empty or whitespace-only messages are rejected.
- The backend returns JSON responses and uses HTTP status codes to indicate success or failure.

## 3. Error Handling
- Missing provider API keys are handled by returning an error instead of making a provider request.
- Provider API errors are caught and returned as a generic backend error.
- The frontend displays an error message if the backend cannot be reached or the request fails.
- Error responses should not contain API keys, secrets, stack traces, or other sensitive information.
- Provider failures and timeouts should be tested and recorded in `api-tests.md`.

## 4. CORS and Local Development
- During local development, the backend allows browser requests from `http://localhost:5500` and `http://127.0.0.1:5500`.
- The allowed origins should be restricted to the actual frontend origin when deployed.
- CORS is not authentication; it does not replace API access controls.

## 5. Browser Storage and Privacy
- Conversation history and the theme preference are stored in the browser using `localStorage`.
- This means chat history remains on that browser/device and is not protected by a user login.
- Anyone with access to the same browser profile may be able to view the saved conversations.
- Avoid entering passwords, API keys, or other sensitive personal information into the chatbot.
- Provide a way to clear saved conversations if the app is used by others on the same device.

## 6. Git and Repository Safety
- Before committing, check `git status` and verify that `.env` is not staged.
- Do not commit API keys, access tokens, passwords, or other secrets.
- If a real API key is accidentally committed, revoke it and create a replacement; deleting it in a later commit does not remove it from Git history.
- Keep dependencies listed in `requirements.txt`.

## 7. Current Limitations
- The app has no login or user accounts.
- Local browser storage is not encrypted by the app.
- The backend endpoint does not currently implement user authentication or rate limiting.
- CORS alone does not prevent non-browser clients from calling the API.

## 8. Security Checklist
- [✔] `.env` contains real keys only locally and is ignored by Git.
- [✔] `.env.example` contains placeholders only.
- [✔] No API keys are present in frontend code or Git history.
- [✔] Missing-key and provider-error cases have been tested.
- [✔] CORS allows only the intended frontend origin.
- [✔] API keys are configured securely if deployed.


