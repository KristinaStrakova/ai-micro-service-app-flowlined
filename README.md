
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


```
---

## How to Set Up & Run

### 1. Clone the repository

```bash

TO DO:
```

### 2. Set your environment variables

Create a `.env` file in the root:

```env
COHERE_API_KEY=for_now_there_is_mine
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

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

In this branch I did not include Pytest since I encountered numerous issues with file imports. When running tests locally, pytest consistently responded with errors like `ModuleNotFoundError: No module named 'app'` due to import path conflicts. The only workarounds involved writing complete relative paths in main.py, which then broke the setup when running the service in Docker. Since it was impossible to have a configuration that satisfied both testing and Docker execution simultaneously, I decided to split these efforts into separate branches—demonstrating each skill individually. In this branch I am showcasing my experience with **Docker** to containerize the project, making it easy for anyone to run with `docker compose up`.

**Pytest** are available on the `main` branch.

The service is structured with **async endpoints**, supports structured **JSON logs** using Loguru, and is production-ready for small-scale use.

---

##  Non-Functional Features

-  Docker-first: Just `docker compose up --build`
-  Async endpoints (`async def`)
-  JSON logging with Loguru
-  FastAPI docs auto-rendered at `/docs`
-  Unit tests using Pytest

---

