# WEEK TWO NOTES

# AI APIs & CHATBOT INTEGRATION

## What is an API?

API stands for **Application Programming Interface**.

An API allows two software applications to communicate with each other.

For example, imagine you are building an AI chatbot website. Your frontend is written in HTML, CSS and JavaScript, while your backend is written in Python.

The frontend cannot directly execute your Python backend code. Instead, it sends a request to the backend through an API.

### Example

You type the following message into your chatbot:

"Explain Python in simple words."

Your application follows this process:

User enters a prompt

⬇️

Frontend sends a request to the backend

⬇️

Backend receives the prompt

⬇️

Backend calls the AI API

⬇️

AI generates a response

⬇️

Backend sends the response to the frontend

⬇️

Frontend displays the answer

**Remember: An API acts as a communication bridge between applications.**

---

## What is a REST API?

REST stands for **Representational State Transfer**.

A REST API is a common way for applications to communicate over HTTP using defined URLs and methods.

For example, your chatbot backend might provide these endpoints:

- `GET /` — Check whether the backend is running.
- `POST /api/chat` — Send a prompt and receive an AI response.

An endpoint is a URL where an application can access a particular function or resource.

### Important HTTP methods

**1. GET**

Used to retrieve information.

Example: Checking whether your chatbot backend is running.

**2. POST**

Used to send information to a server.

Example: Sending a prompt to your chatbot backend.

**3. PUT**

Used to replace or update a resource.

**4. DELETE**

Used to delete a resource.

For Week 2, the most important methods are **GET and POST**.

---

## What is JSON?

JSON stands for **JavaScript Object Notation**.

It is a text format used to exchange structured data between applications.

For example, when the frontend sends a message to the backend, it can send the following JSON:

```json
{
  "prompt": "Explain Python in simple words."
}
```

The backend receives the prompt and sends it to the AI provider.

The AI generates a response, and the backend can return JSON like this:

```json
{
  "reply": "Python is a programming language known for its simple syntax."
}
```

### Important points

- JSON stores information as key-value pairs.
- Keys are written as strings.
- Strings use double quotation marks.
- JSON can contain strings, numbers, booleans, arrays, objects and null values.
- JSON is commonly used when frontend and backend applications communicate.

**Remember: JSON is the format used to send and receive data.**

---

## What are HTTP headers?

HTTP headers contain additional information about an HTTP request or response.

They help the server understand how to process the request.

### Example headers

**Content-Type**

Tells the server what type of data is being sent.

For example:

`Content-Type: application/json`

This indicates that the request body contains JSON.

**Authorization**

Used to provide authentication credentials when an API requires them.

For example, an AI provider may require an API key in an authorization header.

### How headers work

Frontend prepares a request

⬇️

Request includes headers and JSON data

⬇️

Backend receives the request

⬇️

Backend processes the information

**Important:** Your browser frontend should not contain the secret AI provider API key. The backend should use that key when communicating with the provider.

---

## What are HTTP status codes?

HTTP status codes tell you whether a request succeeded or encountered a problem.

### 1. Successful responses

**200 — OK**

The request succeeded.

Example: The chatbot successfully returns an AI response.

**201 — Created**

A resource was created successfully.

This is common when creating resources, but it is not normally required for a simple chat response.

### 2. Client errors

**400 — Bad Request**

The request contains invalid information.

**401 — Unauthorized**

Authentication is missing or invalid.

Example: An AI provider rejects an invalid API key.

**403 — Forbidden**

The server understands the request but refuses access.

**404 — Not Found**

The requested resource or endpoint does not exist.

**422 — Unprocessable Content**

The server cannot process the request because its data fails validation. FastAPI commonly returns this status for invalid request bodies.

**429 — Too Many Requests**

The request exceeds a rate limit or usage limit.

### 3. Server errors

**500 — Internal Server Error**

An unexpected error occurs inside the server.

**502 — Bad Gateway**

A gateway or intermediary receives an invalid response from an upstream service.

**504 — Gateway Timeout**

A gateway does not receive a timely response from an upstream service.

### Example

Suppose your chatbot calls an AI provider, but the provider is unavailable.

The backend should handle the failure and return a suitable error response instead of crashing.

**Remember: Status codes help developers understand what happened to a request.**

---

## What is an AI API?

An AI API allows your application to use an existing AI model through requests.

You do not need to train the model yourself.

For example, your chatbot can send a prompt to an AI provider, and the provider returns a generated answer.

### Example workflow

User enters a prompt

⬇️

Frontend sends the prompt to Python

⬇️

Python sends a request to an AI provider

⬇️

AI provider processes the prompt

⬇️

AI provider returns its response

⬇️

Python extracts the answer

⬇️

Frontend displays the answer

### Important terms

**AI provider:** A service that provides access to AI models.

**AI model:** The trained model that generates responses.

**API request:** A message sent to an API to perform an operation.

**API response:** The information returned by the API.

**API key:** A secret credential used to authenticate with an API.

Official documentation: https://platform.openai.com/docs/

---

## What is an API key?

An API key is a secret credential used to authenticate an application with an API provider.

It may also be associated with usage limits, billing and account permissions.

Think of it as a password that allows your backend to access a service.

### Why must an API key be protected?

If you put the key directly inside frontend JavaScript, anyone who visits your website may be able to inspect the code or network requests and obtain it.

Someone could then misuse the key and potentially consume your API credits.

### Correct approach

Frontend

⬇️

Python backend

⬇️

Backend reads the API key from an environment variable

⬇️

Backend authenticates with the AI provider

⬇️

Backend returns the result to the frontend

### Important security rules

- Never place secret API keys in frontend JavaScript.
- Never upload real API keys to GitHub.
- Store secrets in environment variables.
- Keep the local `.env` file out of version control.
- Provide a `.env.example` file containing placeholder values rather than real secrets.
- Never return API keys in responses or error messages.

Official API key safety guidance:

https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

**Remember: The frontend communicates with your backend; your backend communicates with the AI provider using the secret key.**

---

## What are environment variables?

Environment variables are values supplied to an application through its environment rather than being hardcoded into the source code.

They are useful for storing configuration and secrets.

For example, your backend needs to know which API key to use.

Instead of writing the real key directly into Python code, you store it in a local `.env` file and load it into the backend environment.

### Important files

**`.env`**

Contains local configuration and secret values.

This file should not be committed to GitHub.

**`.env.example`**

Shows the configuration variables the application expects, using placeholder values.

For example, it can indicate that an API key must be configured without containing the real key.

**`.gitignore`**

Tells Git which files and folders should not be tracked.

It should exclude your `.env` file and Python virtual environment.

**Remember: Environment variables help separate application configuration from source code, but you must still protect how they are stored and accessed.**

---

## What is a backend API endpoint?

An endpoint is a URL that allows a client to access a particular backend operation.

For your chatbot, you will create:

`POST /api/chat`

This endpoint receives the user's prompt and returns the AI-generated answer.

### What happens inside the endpoint?

1. The frontend sends a prompt.
2. The backend receives the request.
3. The backend validates the prompt.
4. The backend checks its configuration.
5. The backend sends the prompt to the AI provider.
6. The AI provider generates a response.
7. The backend extracts the answer.
8. The backend returns a JSON response.

### Example

Request:

```json
{
  "prompt": "What is an API?"
}
```

Response:

```json
{
  "reply": "An API allows software applications to communicate with each other."
}
```

The exact response structure depends on how you design your backend.

**Remember: Your frontend sends the prompt to your own backend endpoint, not directly to the AI provider using a secret key.**

---

## What is FastAPI?

FastAPI is a Python framework for building APIs.

You can use it to create the backend for your chatbot.

### Why use FastAPI?

- It lets you define API endpoints.
- It supports HTTP methods such as GET and POST.
- It validates request data using Python type declarations and Pydantic models.
- It supports asynchronous operations.
- It provides interactive API documentation.

For example, your backend can expose:

- `GET /` — Check backend availability.
- `POST /api/chat` — Process a chat request.

FastAPI also provides an interactive documentation page that allows you to test endpoints without first creating a frontend.

Official documentation: https://fastapi.tiangolo.com/

---

## What is error handling?

Error handling means detecting problems and responding to them safely rather than allowing the application to crash unexpectedly.

Your chatbot can encounter errors in several places:

- The user submits an empty prompt.
- The request contains invalid data.
- The API key is missing.
- The API key is invalid.
- The selected model is unavailable.
- The provider rate limit is reached.
- The provider request times out.
- The provider returns an unexpected error.

### Example

Suppose the user submits a prompt, but the backend has no API key configured.

The backend should detect the missing configuration and return a clear error.

It should not expose a Python stack trace, the contents of environment variables, or other sensitive information.

### What should the frontend do?

- Display a useful error message.
- Stop showing the loading indicator.
- Allow the user to try again.
- Avoid displaying sensitive technical details.

### Important distinction

A successful HTTP request does not necessarily mean the AI operation succeeded. The application must also handle errors returned by the AI provider.

**Remember: Good error handling makes the application more reliable and easier to debug.**

---

## What is a timeout?

A timeout occurs when an operation takes longer than the allowed waiting period.

For example, your backend sends a prompt to an AI provider, but the provider takes too long to respond.

The backend should stop waiting after the configured timeout and handle the situation appropriately.

### Example workflow

User sends a prompt

⬇️

Backend sends a request to the AI provider

⬇️

Provider does not respond in time

⬇️

Backend handles the timeout

⬇️

Frontend displays a helpful error message

A timeout does not always mean the provider is completely unavailable. The request may simply have taken too long.

---

## What is API testing?

API testing means checking whether an endpoint behaves correctly under different conditions.

You should test your backend before relying on the frontend.

For example, FastAPI's interactive documentation can be used to send requests to your endpoint.

---

## What is CORS?

CORS stands for **Cross-Origin Resource Sharing**.

It is a browser security mechanism that controls whether a web page can make requests to a server on a different origin.

An origin consists of the scheme, host and port.

For example, your frontend might run on one local port while FastAPI runs on another. The browser may block requests unless the backend allows the frontend's origin.

### Example

Frontend: `http://localhost:5500`

Backend: `http://localhost:8000`

These are different origins because their ports differ.

You may need to configure CORS in FastAPI to allow your frontend to communicate with the backend.

For development, allow only the origins you need. Avoid allowing every origin indiscriminately, particularly in production.

**Remember: CORS controls browser cross-origin access; it does not replace authentication or API-key security.**

---

## How do the frontend and backend work together?

Your chatbot has three main parts.

### 1. HTML — Structure

HTML defines the elements of the page.

Examples include:

- Chat container.
- Message area.
- Text input.
- Send button.

### 2. CSS — Appearance

CSS controls the appearance of those elements.

Examples include:

- Colours and backgrounds.
- Spacing and alignment.
- Message bubbles.
- Responsive layouts.
- Loading animations.

### 3. JavaScript — Behaviour

JavaScript makes the frontend interactive.

It handles:

- Reading the user's message.
- Sending HTTP requests to the backend.
- Processing JSON responses.
- Displaying AI messages.
- Showing loading indicators and errors.

### 4. Python — Backend logic

Python receives the requests, validates data, accesses the API key, calls the AI provider and returns the response.

### 5. AI provider — Response generation

The provider runs the model and generates an answer from the submitted prompt.

**Remember: HTML structures the page, CSS styles it, JavaScript handles browser interactions, Python manages backend operations, and the AI provider generates the response.**

---

## Week 2 Mini-Project

### Build an AI Chatbot

The purpose of this mini-project is to combine everything you learned about APIs and backend integration.

### Required features

- A simple chat interface.
- A message input and Send button.
- A Python backend using FastAPI.
- A `POST /api/chat` endpoint.
- Integration with an actual AI provider.
- JSON request and response handling.
- Secure API-key configuration.
- Input validation and error handling.
- Loading indicators and error messages.
- API testing and security documentation.

### Final concept to remember

**Frontend → Backend API → AI Provider → Backend Response → Frontend**
