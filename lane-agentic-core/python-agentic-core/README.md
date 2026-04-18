# Python Agentic Core Lane

## Vai tro
- Dinh nghia noi bo cac khoi theo so do Agentic AI Core.
- Tach tung chuc nang thanh file/module rieng.
- Cung cap skeleton function (co mo ta muc dich, chua co logic xu ly).

## Duong noi noi bo theo so do
1. `Orchestrator Agent LangGraph Route -> Raw Audio`
2. `Orchestrator Agent LangGraph Route -> Text/Metadata`
3. `Orchestrator Agent LangGraph Route -> Voice Stream`
4. `Raw Audio -> Deepfake Agent`
5. `Voice Stream -> Google STT API`
6. `Google STT API -> Transcribed Text`
7. `Transcribed Text -> Threat Agent`
8. `Text/Metadata -> Entity Agent`
9. `Deepfake Agent -> Decision & Reasoning Engine` (signal/score)
10. `Threat Agent -> Decision & Reasoning Engine` (signal/score)
11. `Entity Agent -> Decision & Reasoning Engine` (signal/score)
12. `Decision & Reasoning Engine -> Gemini API Reasoning Engine`
13. `Gemini API Reasoning Engine -> Decision & Reasoning Engine`
14. `Decision & Reasoning Engine -> JSON score + warning`
15. `JSON score + warning -> Cloud Run API Microservices`
16. `Search Query -> Threat Agent`

## File mapping theo chuc nang
- `app/services/orchestrator.py`: skeleton cho Orchestrator Agent LangGraph Route
- `app/services/channels/deepfake_signal_channel.py`: skeleton cho stage signal/score tu Deepfake Agent
- `app/services/channels/raw_audio_channel.py`: skeleton cho stage Raw Audio
- `app/services/channels/text_metadata_channel.py`: skeleton cho stage Text/Metadata
- `app/services/channels/voice_stream_channel.py`: skeleton cho stage Voice Stream
- `app/services/channels/transcribed_text_channel.py`: skeleton cho stage Transcribed Text (Google STT API -> Transcribed Text -> Threat Agent)
- `app/services/channels/search_query_channel.py`: skeleton cho stage Search Query vao Threat Agent
- `app/services/channels/threat_signal_channel.py`: skeleton cho stage signal/score tu Threat Agent
- `app/services/channels/entity_signal_channel.py`: skeleton cho stage signal/score tu Entity Agent
- `app/services/channels/reasoning_explanation_channel.py`: skeleton cho stage Reasoning/Explanation giua Decision va Gemini
- `app/services/channels/json_score_warning_channel.py`: skeleton cho stage JSON score + warning
- `app/services/agents/deepfake_agent.py`: skeleton Deepfake Agent
- `app/services/agents/stt_agent.py`: skeleton Google STT API
- `app/services/agents/threat_agent.py`: skeleton Threat Agent
- `app/services/agents/entity_agent.py`: skeleton Entity Agent
- `app/services/agents/reasoning_agent.py`: skeleton Gemini API Reasoning Engine
- `app/services/decision_engine.py`: skeleton Decision & Reasoning Engine
- `app/services/internal_link_orchestrator.py`: skeleton dieu phoi cac duong noi noi bo
- `app/services/links/deepfake_decision_link.py`: skeleton link rieng cho Deepfake Agent -> Decision Engine
- `app/services/links/decision_gemini_reasoning_link.py`: skeleton link rieng cho Decision & Reasoning Engine -> Gemini API Reasoning Engine
- `app/services/links/entity_decision_link.py`: skeleton link rieng cho Entity Agent -> Decision Engine
- `app/services/links/gemini_decision_reasoning_link.py`: skeleton link rieng cho Gemini API Reasoning Engine -> Decision & Reasoning Engine
- `app/services/links/google_stt_transcribed_text_link.py`: skeleton link rieng cho Google STT API -> Transcribed Text
- `app/services/links/transcribed_text_threat_agent_link.py`: skeleton link rieng cho Transcribed Text -> Threat Agent
- `app/services/links/google_stt_threat_link.py`: skeleton link back-compat cho handoff Google STT API -> Threat Agent
- `app/services/links/search_query_threat_link.py`: skeleton link rieng cho Search Query -> Threat Agent
- `app/services/links/threat_decision_link.py`: skeleton link rieng cho Threat Agent -> Decision Engine
- `app/services/links/decision_json_score_warning_link.py`: skeleton link rieng cho Decision & Reasoning Engine -> JSON score + warning
- `app/services/links/json_score_warning_cloud_run_link.py`: skeleton link rieng cho JSON score + warning -> Cloud Run API Microservices
- `app/routes/score.py`: endpoint skeleton (gom endpoint noi bo)

## Chay local
```bash
pip install -r requirements.txt
set STORAGE_BASE_URL=http://localhost:8102
uvicorn app.main:app --host 0.0.0.0 --port 8101
```

## API chinh
- `POST /v1/agentic/score`
- `POST /v1/agentic/internal/raw-audio-to-deepfake`
- `POST /v1/agentic/internal/orchestrator-to-raw-audio`
- `POST /v1/agentic/internal/orchestrator-to-text-metadata`
- `POST /v1/agentic/internal/orchestrator-to-voice-stream`
- `POST /v1/agentic/internal/voice-stream-to-google-stt`
- `POST /v1/agentic/internal/google-stt-api-to-transcribed-text`
- `POST /v1/agentic/internal/google-stt-to-threat`
- `POST /v1/agentic/internal/google-stt-api-to-threat-agent`
- `POST /v1/agentic/internal/transcribed-text-to-threat-agent`
- `POST /v1/agentic/internal/search-query-to-threat-agent`
- `POST /v1/agentic/internal/text-metadata-to-entity`
- `POST /v1/agentic/internal/deepfake-to-decision`
- `POST /v1/agentic/internal/deepfake-signal-score-to-decision`
- `POST /v1/agentic/internal/threat-to-decision`
- `POST /v1/agentic/internal/threat-signal-score-to-decision`
- `POST /v1/agentic/internal/entity-to-decision`
- `POST /v1/agentic/internal/entity-signal-score-to-decision`
- `POST /v1/agentic/internal/decision-to-gemini`
- `POST /v1/agentic/internal/decision-reasoning-explanation-to-gemini`
- `POST /v1/agentic/internal/gemini-to-decision`
- `POST /v1/agentic/internal/gemini-reasoning-explanation-to-decision`
- `POST /v1/agentic/internal/decision-and-reasoning-engine-to-json-score-warning`
- `POST /v1/agentic/internal/json-score-warning-to-cloud-run-api-microservices`
- `GET /health`
