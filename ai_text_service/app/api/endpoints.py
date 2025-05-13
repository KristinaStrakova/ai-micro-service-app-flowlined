from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import cohere  

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")  
co = cohere.Client(cohere_api_key)

router = APIRouter()

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


@router.get("/health")
async def health_check():
    return {"status": "ok", "uptime": "123"}
