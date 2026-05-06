from fastapi import FastAPI
from src.api.views import api_router

app = FastAPI(title="Logistics App")
app.include_router(api_router)
