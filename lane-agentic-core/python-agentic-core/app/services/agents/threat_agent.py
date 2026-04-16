import re
from app.models.contracts import AgentSignalScore, SearchQueryPayload, TranscribedTextPayload
from app.clients.gemini_client import GeminiClient

SCAM_SCORE_PROMPT = """
Task: Multi-task Scam & Safety Evaluation

You are an expert evaluator analyzing a conversation to estimate risks.
You will evaluate the input based on three metrics:
1. Scam Risk: Likelihood that the sender is a scammer (0.0 to 1.0).
2. PII Risk: Likelihood that the user's response or context contains personally identifiable information (0.0 to 1.0).
3. Engagement: How "hooked" or cooperative the user seems (0.0 to 1.0).

Context (Similar Known Scam Patterns):
{context}

User Input to Evaluate:
{input_text}

Instructions:
- Return the evaluation in exactly the following JSON format:
{{
  "scam_risk": 0.85,
  "pii_risk": 0.1,
  "engagement": 0.5,
  "pii_types": ["phone_number", "none"],
  "reasoning": "Brief explanation"
}}
- If no PII is found, return ["none"] for pii_types.
- Output ONLY the JSON string.
"""

class ThreatAgent:
    def __init__(self):
        self.gemini_client = GeminiClient()

    def ingest_google_stt_transcribed_text(self, payload: TranscribedTextPayload) -> str:
        """Arrow: Google STT API -> Threat Agent, ingest transcript payload from STT stage."""
        return payload.transcript

    def extract_threat_features_from_transcript_payload(self, payload: TranscribedTextPayload) -> list[float]:
        """Extract raw threat features from transcribed-text payload before scoring."""
        return []

    async def analyze_transcribed_text_to_signals(self, transcript: str, pattern_ids: list[str]) -> list[AgentSignalScore]:
        """Arrow: Transcribed Text -> Threat Agent, output risk signals for decision stage."""
        return await self._get_gemini_score(transcript, []) # RAG matches not passed here directly yet

    def ingest_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Arrow: Search Query -> Threat Agent, ingest query payload from LangChain RAG stage."""
        return payload

    async def analyze_search_query_to_signals(self, payload: SearchQueryPayload, patterns: list[dict]) -> list[AgentSignalScore]:
        """Analyze Search Query payload and matched patterns into threat-agent raw signals."""
        return await self._get_gemini_score(payload.query, patterns)

    async def _get_gemini_score(self, text: str, patterns: list[dict]) -> list[AgentSignalScore]:
        import json
        context_str = "None"
        if patterns:
            context_str = "\n".join([f"- {p.get('pattern_text', '')}" for p in patterns])
            
        prompt = SCAM_SCORE_PROMPT.format(context=context_str, input_text=text)
        
        response_text = await self.gemini_client.generate_content(prompt)
        
        try:
            # Clean possible markdown formatting
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            scam_score = data.get("scam_risk", 0.0) * 100.0
            pii_score = data.get("pii_risk", 0.0) * 100.0
            engagement_score = data.get("engagement", 0.0) * 100.0
            pii_types = ",".join(data.get("pii_types", ["none"]))
            
            return [
                AgentSignalScore(signal_name="scam_risk", score=scam_score, reason=data.get("reasoning")),
                AgentSignalScore(signal_name="pii_risk", score=pii_score, reason=pii_types),
                AgentSignalScore(signal_name="engagement", score=engagement_score)
            ]
        except Exception as e:
            print(f"Error parsing Gemini multi-task scoring JSON: {e}")
            return [AgentSignalScore(signal_name="scam_risk", score=0.0)]

    def map_threat_signals_to_scores(self, raw_signals: list[AgentSignalScore]) -> list[AgentSignalScore]:
        """Normalize threat raw signals into consistent score list."""
        return raw_signals

    def emit_threat_signal_scores_for_decision(self, scored_signals: list[AgentSignalScore]) -> list[AgentSignalScore]:
        """Arrow: Threat Agent -> signal/score payload forwarded to Decision Engine."""
        return scored_signals
