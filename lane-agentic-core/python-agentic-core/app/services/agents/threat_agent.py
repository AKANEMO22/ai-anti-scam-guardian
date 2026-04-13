import re
from app.models.contracts import SearchQueryPayload, TranscribedTextPayload
from app.clients.gemini_client import GeminiClient

SCAM_SCORE_PROMPT = """
Task: Scam Risk Scoring

You are an expert evaluator analyzing a text or conversation to estimate the likelihood that it is a scam.
You will be provided with the user's input AND a list of similar known scam patterns from our database.

Context (Similar Known Scam Patterns):
{context}

User Input to Evaluate:
{input_text}

Instructions:
- Analyze the user input, comparing it with the known scam patterns to see if it shares threat vectors.
- Estimate the threat risk.
- Output a scam risk score from 0.0 (safe) to 1.0 (highest risk scam).
- Provide ONLY a floating point number as output (e.g., 0.87), no text or explanation.
"""

class ThreatAgent:
    def __init__(self):
        self.gemini_client = GeminiClient()

    def ingest_google_stt_transcribed_text(self, payload: TranscribedTextPayload) -> str:
        """Arrow: Google STT API -> Threat Agent, ingest transcript payload from STT stage."""
        return payload.transcript

    def extract_threat_features_from_transcript_payload(self, payload: TranscribedTextPayload) -> list[float]:
        """Extract raw threat features from transcribed-text payload before scoring."""
        pass  # Not used in this simplified flow

    async def analyze_transcribed_text_to_signals(self, transcript: str, pattern_ids: list[str]) -> list[float]:
        """Arrow: Transcribed Text -> Threat Agent, output risk signals for decision stage."""
        return await self._get_gemini_score(transcript, []) # RAG matches not passed here directly yet

    def ingest_search_query_payload(self, payload: SearchQueryPayload) -> SearchQueryPayload:
        """Arrow: Search Query -> Threat Agent, ingest query payload from LangChain RAG stage."""
        return payload

    async def analyze_search_query_to_signals(self, payload: SearchQueryPayload, patterns: list[dict]) -> list[float]:
        """Analyze Search Query payload and matched patterns into threat-agent raw signals."""
        return await self._get_gemini_score(payload.query, patterns)

    async def _get_gemini_score(self, text: str, patterns: list[dict]) -> list[float]:
        context_str = "None"
        if patterns:
            context_str = "\n".join([f"- {p.get('pattern_text', '')}" for p in patterns])
            
        prompt = SCAM_SCORE_PROMPT.format(context=context_str, input_text=text)
        
        response = await self.gemini_client.generate_content(prompt)
        
        # Parse output for float
        try:
            # Find all numbers in the response
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", response)
            if numbers:
                score = float(numbers[0])
                score = max(0.0, min(1.0, score))  # clamp to 0-1
                return [score * 100.0] # Scale to 0-100 for Decision Engine
            return [0.0]
        except ValueError:
            return [0.0]

    def map_threat_signals_to_scores(self, raw_signals: list[float]) -> list[float]:
        """Normalize threat raw signals into consistent score list."""
        return raw_signals

    def emit_threat_signal_scores_for_decision(self, scored_signals: list[float]) -> list[float]:
        """Arrow: Threat Agent -> signal/score payload forwarded to Decision Engine."""
        return scored_signals
