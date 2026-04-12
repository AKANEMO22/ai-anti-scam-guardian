from fastapi import FastAPI

from app.routes.score import router as score_router

app = FastAPI(title="Anti-Scam Agentic Core", version="0.1.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "lane": "agentic-core"}


app.include_router(score_router)
