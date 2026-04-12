from fastapi import FastAPI

from app.routes.storage import router as storage_router

app = FastAPI(title="Anti-Scam Storage Lane", version="0.1.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "lane": "storage"}


app.include_router(storage_router)
