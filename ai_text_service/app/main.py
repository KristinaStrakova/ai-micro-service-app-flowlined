from fastapi import FastAPI
from ai_text_service.app.api import endpoints

app = FastAPI(title="AI Text Utility")

# include all routes from the router
app.include_router(endpoints.router)


@app.get("/")
def root():
    return {"message": "Welcome to AI Text Utility!"}

