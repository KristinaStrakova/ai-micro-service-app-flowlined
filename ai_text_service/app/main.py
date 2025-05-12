from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="AI Text Utility")

# include all routes from the router
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to AI Text Utility!"}
