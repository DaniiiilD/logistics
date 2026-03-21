from fastapi import FastAPI
from src.api.views.auth import main_router

app = FastAPI(title="Logistics App")
app.include_router(main_router)
