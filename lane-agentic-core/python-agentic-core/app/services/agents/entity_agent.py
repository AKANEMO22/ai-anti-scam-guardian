import re
from app.clients.gemini_client import GeminiClient

ENTITY_SCORE_PROMPT = """
Task: Entity Risk Scoring

Analyze the following text to extract entities (Phone numbers, URLs, Bank Names, Organizations) and evaluate them for phishing or scam risk.

Text to Evaluate:
{input_text}

Threat Indicators:
- Suspicious URLs (e.g. typosquatting, free hosters, unsecure HTTP)
- Request to transfer money to personal bank accounts
- Phone numbers with foreign or premium prefixes masquerading as local

Instructions:
Output an Entity Risk Score from 0.0 (safe) to 1.0 (highest risk).
Provide ONLY a floating point number as output (e.g., 0.87), no text or explanation.
"""

class EntityAgent:
    def __init__(self):
        self.gemini_client = GeminiClient()

    async def analyze_text_metadata_to_signals(self, text: str, metadata: dict[str, str]) -> list[float]:
        """Arrow: Text/Metadata -> Entity Agent, output entity-related risk signals."""
        prompt = ENTITY_SCORE_PROMPT.format(input_text=text)
        response = await self.gemini_client.generate_content(prompt)
        
        try:
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", response)
            if numbers:
                score = float(numbers[0])
                score = max(0.0, min(1.0, score))
                return [score * 100.0]
            return [0.0]
        except ValueError:
            return [0.0]

    def map_entity_signals_to_scores(self, raw_signals: list[float]) -> list[float]:
        """Normalize entity raw signals into consistent score list."""
        return raw_signals

    def emit_entity_signal_scores_for_decision(self, scored_signals: list[float]) -> list[float]:
        """Arrow: Entity Agent -> signal/score payload forwarded to Decision Engine."""
        return scored_signals
