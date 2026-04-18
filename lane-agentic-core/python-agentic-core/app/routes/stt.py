from fastapi import APIRouter

from app.models.contracts import VoiceStreamToSttRequest, TranscribedTextPayload

router = APIRouter(tags=["stt"])


@router.post("/v1/stt/transcribe", response_model=TranscribedTextPayload)
def transcribe_voice(request: VoiceStreamToSttRequest):
    """Accept a voice stream payload (or chunk reference) and return a transcribed text payload.

    Lightweight POC: return a simulated transcript so the lane can be exercised
    without instantiating heavy orchestrator dependencies at import time.
    """
    try:
        call_session_id = request.payload.callSessionId
        metadata = request.payload.metadata or {}
        transcript = f"(simulated transcript for session {call_session_id})"
        return TranscribedTextPayload(callSessionId=call_session_id, transcript=transcript, metadata=metadata)
    except Exception as e:
        print(f"Error in STT POC: {e}")
        return TranscribedTextPayload(callSessionId=getattr(request.payload, 'callSessionId', None) or "", transcript="(simulated transcript)", metadata=getattr(request.payload, 'metadata', None) or {})
