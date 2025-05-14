
# AI Micro-Service Coding Challenge

## Introduction

This project is a simple FastAPI-based microservice that exposes two main functionalities:

- **Summarization** of text using Cohere's language model.
- **Semantic similarity matching** between a query and list of texts.

I originally planned to use OpenAI models, it was later changed to Cohere due to API key quota limitations. The service is containerized with Docker and includes automated tests using Pytest.

---

## Project Contents

```bash
.
ai-text_service/
├── .env                            #Cohere with API key
├── .gitignore                      #.gitignore
├── README.md                       #Documentation Overview
├── docker-compose.yml              #Compose set up for local
├── Dockerfile                      #Docker configuration
├── requirements.txt                #Python independencies
├── ai_text_service/                
│   ├── app/
│   │   ├── main.py                 # FastAPI application setup
│   │   ├── api/
│   │   │   ├── endpoints.py        # Cohere - Summarize, Similiarity function (+ health check)
│   │   ├── app_time/
│   │   │   ├── time_state.py       # Time stamp of application
│   │   ├── tests/
│   │   │   └── test_endpoints.py   # Pytests

```
---

## How to Set Up & Run

### 1. Set your environment variables

Create a `.env` file in the root:

```env
COHERE_API_KEY=for_now_there_is_mine
```

### 2. Run Pytests

```bash
pytest /tests
```

---

## Available Endpoints

### `POST /summarize`

Summarizes input text.

```json
{
  "text": "A long article or passage...(has to be at least 250 characters.)"
}
```

### `POST /similarity`

Returns the most similar text to a query from a list.

```json
{
  "query": "What is AI?",
  "texts": ["AI is...", "Cats are cute", "Space is magical place."]
}
```

### `GET /health`
Return time duration of openned application.

---

## The Process

Initially, the project used **OpenAI** as suggested in the coding challenge documentation. However, due to billing and quota limitations, I decided to switch to an alternative.

After researching, I found **Cohere**, which offers a summarization and embedding model quite similar to OpenAI’s. While it allowed more flexibility without requiring a paid tier, it's still not ideal for large-scale production, as it has a 1000-requests-per-month free cap.

I also asked peers for advice and was introduced to **Ollama**, a local generative model, but setting that up would require more time and understanding since I hadn't worked with local LLMs before.

Another new area for me was **Pytest**. The documentation wasn’t always helpful, so I leaned on ChatGPT for examples and guidance. After some iteration and debugging, I wrote tests covering success and error scenarios for both endpoints.

In this branch I did not include **Docker** since I focused on getting **Pytest** to work correctly. While testing locally, I encountered persistent import errors such as `ModuleNotFoundError: No module named 'app'`. To resolve these, I used complete relative paths in main.py, which allowed the tests to pass successfully. However, this approach broke compatibility with Docker, which expected a different project structure. Because it was difficult to find a single setup that satisfied both Docker and testing configurations, I chose to separate them into different branches. This branch showcases working **Pytest coverage** for both successful and error scenarios.

**Docker** setup and containerization can be found in the `cohere-with-docker` branch.

The service is structured with **async endpoints**, supports structured **JSON logs** using Loguru, and is production-ready for small-scale use.

---

##  Non-Functional Features

-  Docker-first: Just `docker compose up --build`
-  Async endpoints (`async def`)
-  JSON logging with Loguru
-  FastAPI docs auto-rendered at `/docs`
-  Unit tests using Pytest

---

