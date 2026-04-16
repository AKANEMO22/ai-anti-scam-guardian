from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload
from app.clients.gemini_client import GeminiClient

REASONING_PROMPT = """
Task: Giải thích lý do cảnh báo lừa đảo & Gợi ý phản hồi nhử mồi (Scam-Baiting).

Phân tích các tín hiệu rủi ro sau đây và thực hiện:
1. Viết lời giải thích BẰNG TIẾNG VIỆT, ngắn gọn, dễ hiểu để cảnh báo người dùng.
2. Nếu rủi ro cao (>50%), hãy gợi ý một câu trả lời "nhử mồi" (baiter response) để lừa lại kẻ lừa đảo hoặc kéo dài thời gian nhằm thu thập bằng chứng/lãng phí thời gian của chúng.

Tín hiệu rủi ro:
- Threat signals (Scam, PII, Engagement): {threat_signals}
- Entity signals: {entity_signals}
- Deepfake signals: {deepfake_signals}

Yêu cầu output JSON:
{{
  "summary": "Tóm tắt ngắn",
  "explanation": "Giải thích chi tiết",
  "baiter_response": "Câu trả lời gợi ý cho người dùng (đóng vai người ngây thơ/hợp tác nhưng không lộ thông tin thật)"
}}

Ví dụ:
{{
  "summary": "Phát hiện giả mạo ngân hàng",
  "explanation": "Link này dẫn tới trang web lừa đảo để chiếm đoạt mã OTP.",
  "baiter_response": "Dạ vâng ạ, tôi đang vào link rồi nhưng mạng hơi lag. Bạn đợi một chút nhé?"
}}
"""

class GeminiApiReasoningEngine:
    def __init__(self):
        self.gemini_client = GeminiClient()

    async def request_reasoning_from_decision_signals(self, bundle: DecisionSignalBundle) -> GeminiReasoningPayload:
        """Arrow: Decision Engine -> Gemini API Reasoning Engine."""
        threats_str = ", ".join([f"{s.score}%" for s in bundle.threat_signals]) or "None"
        entities_str = ", ".join([f"{s.score}%" for s in bundle.entity_signals]) or "None"
        deepfake_str = ", ".join([f"{s.score}%" for s in bundle.deepfake_signals]) or "None"
        
        prompt = REASONING_PROMPT.format(
            threat_signals=threats_str,
            entity_signals=entities_str,
            deepfake_signals=deepfake_str
        )
        
        response_text = await self.gemini_client.generate_content(prompt)
        
        import json
        try:
             # Try to parse JSON from the response text. 
             # Strip out markdown block if the model included it
             clean_text = response_text.replace("```json", "").replace("```", "").strip()
             data = json.loads(clean_text)
             return GeminiReasoningPayload(
                 summary=data.get("summary", ""),
                 explanation=data.get("explanation", ""),
                 baiter_response=data.get("baiter_response")
             )
        except Exception as e:
             print(f"Error parsing Gemini reasoning JSON: {e}")
             return GeminiReasoningPayload(
                 summary="Hệ thống phát hiện dấu hiệu nghi ngờ.",
                 explanation="Chúng tôi khuyên bạn cẩn thận với thông tin này do hệ thống AI phát hiện các rủi ro tiềm ẩn."
             )

    def return_reasoning_to_decision_engine(self, reasoning: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Arrow: Gemini API Reasoning Engine -> Decision Engine."""
        return reasoning
