import pytest
from httpx import AsyncClient, ASGITransport
from ai_text_service.app.main import app


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

# Test for Summarization Endpoint - success case
@pytest.mark.asyncio
async def test_summarize_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "text": "Artificial intelligence (AI) is rapidly transforming our world, impacting industries from healthcare to finance, education to entertainment. As AI technologies like natural language processing and computer vision become more advanced, they enable machines to perform tasks that once required human intelligence. While AI offers tremendous benefits in terms of efficiency, innovation, and discovery, it also raises important ethical questions. Concerns around job displacement, data privacy, algorithmic bias, and accountability continue to grow. As society embraces the power of AI, it’s crucial to establish frameworks and regulations that ensure these tools are used responsibly and equitably for all."
        }
        response = await client.post("/summarize", json=payload)
        assert response.status_code == 200
        assert "summary" in response.json()
        assert isinstance(response.json()["summary"], str)
        assert len(response.json()["summary"]) > 0


# Test for Summarization Endpoint - error case
@pytest.mark.asyncio
async def test_summarize_empty_input():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "text": ""  # Invalid input: empty string
        }
        # Send an empty JSON body
        response = await client.post("/summarize", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "The 'text' field must not be empty."


# Test for Similarity Endpoint - success case
@pytest.mark.asyncio
async def test_similarity_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "query": "What is AI?",
            "texts": [
                "AI stands for Artificial Intelligence.",
                "Bananas are yellow.",
                "The sky is blue."
            ]
        }
        response = await client.post("/similarity", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "closest_text" in data
        assert "score" in data

        assert data["closest_text"] in payload["texts"]
        assert isinstance(data["score"], float)
        assert 0.0 <= data["score"] <= 1.0


# Test for Similarity Endpoint - error case
@pytest.mark.asyncio
async def test_similarity_with_empty_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "query": "What is AI?",
            "texts": []  # Invalid input: empty list
        }
        response = await client.post("/similarity", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "The 'texts' field must not be empty."

