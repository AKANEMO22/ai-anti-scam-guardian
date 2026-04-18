from fastapi import APIRouter, Depends

from app.clients.agentic_core_client import AgenticCoreClient
from app.dependencies import get_agentic_core_client
# lightweight route - accepts generic JSON body with callSessionId/streamRef

router = APIRouter(tags=["stt"])


@router.post("/v1/stt/stream")
async def stream_voice_chunk(
    body: dict,
    core_client: AgenticCoreClient = Depends(get_agentic_core_client),
):
    """Accept a simple JSON body with `callSessionId` and `chunkBase64` and forward to agentic-core STT.

    Body example: {"callSessionId": "abc", "chunkBase64": "...base64...", "metadata": {}}
    """
    call_session_id = body.get("callSessionId")
    chunk = body.get("chunkBase64") or body.get("streamRef")
    metadata = body.get("metadata") or {}

    if not call_session_id or not chunk:
        return {"error": "missing callSessionId or chunkBase64/streamRef"}

    try:
        result = await core_client.transcribe_stream(call_session_id, chunk, metadata)
        return result
    except Exception as e:
        print(f"Error forwarding voice chunk to agentic-core: {e}")
        return {"error": str(e)}
