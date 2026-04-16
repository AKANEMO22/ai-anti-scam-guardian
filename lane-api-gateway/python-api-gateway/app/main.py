# from dotenv import load_dotenv
# load_dotenv()

from fastapi import FastAPI

from app.routes.analyze import router as analyze_router
from app.routes.feedback import router as feedback_router
from app.routes.internal_cache_flow import router as internal_cache_flow_router
from app.routes.internal_cloud_run_update_database_flow import router as internal_cloud_run_update_database_flow_router
from app.routes.internal_cloud_run_cache_miss_flow import router as internal_cloud_run_cache_miss_flow_router
from app.routes.internal_cache_miss_flow import router as internal_cache_miss_flow_router
from app.routes.internal_feedback_flow import router as internal_feedback_flow_router
from app.routes.internal_auth_flow import router as internal_auth_flow_router

app = FastAPI(title="Anti-Scam API Gateway", version="0.1.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "lane": "api-gateway"}


app.include_router(analyze_router)
app.include_router(feedback_router)
app.include_router(internal_auth_flow_router)
app.include_router(internal_cache_flow_router)
app.include_router(internal_cloud_run_update_database_flow_router)
app.include_router(internal_cloud_run_cache_miss_flow_router)
app.include_router(internal_cache_miss_flow_router)
app.include_router(internal_feedback_flow_router)
