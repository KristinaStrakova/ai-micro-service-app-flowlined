from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import cohere
import numpy as np
from app.app_time.time_state import app_start_time
import time

# Load environment variables from .env file
load_dotenv()

# Initialize Cohere API client
cohere_api_key = os.getenv("COHERE_API_KEY")  
co = cohere.Client(cohere_api_key)

router = APIRouter()

# Summarization Endpoint
# This endpoint takes a text (requires minimum 250 characters) and returns a summary of it
class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(req: SummarizeRequest):
    try:
        response = co.summarize(
            text=req.text,
            length="short",         
            format="paragraph",
            model="command"
        )
        return {"summary": response.summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Text Similarity Endpoint
# This endpoint takes a query and a list of texts, and returns the most similar text to the query
class SimilarityRequest(BaseModel):
    query: str
    texts: list[str]

class SimilarityResponse(BaseModel):
    closest_text: str
    score: float

@router.post("/similarity", response_model=SimilarityResponse)
async def get_most_similar(req: SimilarityRequest):
    try:
        texts_to_embed = [req.query] + req.texts
        embeddings = co.embed(
                            texts=texts_to_embed,
                               model="embed-english-v3.0",
                               input_type="classification"
                               ).embeddings


        query_embedding = embeddings[0]
        text_embeddings = embeddings[1:]

        def cosine_similarity(vec1, vec2):
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        scores = [cosine_similarity(query_embedding, emb) for emb in text_embeddings]
        best_index = int(np.argmax(scores))

        return {
            "closest_text": req.texts[best_index],
            "score": round(float(scores[best_index]), 5)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health Check Endpoint - Bonus
@router.get("/health")
async def health_check():
    uptime_seconds = int(time.time() - app_start_time)
    return {"status": "ok", "uptime": uptime_seconds}

