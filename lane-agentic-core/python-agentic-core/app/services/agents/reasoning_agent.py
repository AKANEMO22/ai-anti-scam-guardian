from app.models.contracts import DecisionSignalBundle, GeminiReasoningPayload
from app.clients.gemini_client import GeminiClient

REASONING_PROMPT = """
Task: Giải thích lý do cảnh báo lừa đảo (Scam Explanation).

Phân tích các tín hiệu rủi ro sau đây và viết một lời giải thích BẰNG TIẾNG VIỆT, ngắn gọn, dễ hiểu để cảnh báo người dùng.

Tín hiệu đe dọa (Threat Signals):
{threat_signals}

Tín hiệu thực thể (Entity Signals - URL, SDT, Bank):
{entity_signals}

Tín hiệu Deepfake Voice (nếu có):
{deepfake_signals}

Yêu cầu:
1. Trả về đúng định dạng JSON có 2 trường: "summary" (1 câu tóm tắt ngắn) và "explanation" (1-2 câu giải thích chi tiết).
2. Viết bằng tiếng Việt, giọng điệu cảnh báo nhưng điềm tĩnh.
3. KHÔNG output gì khác ngoài chuỗi JSON hợp lệ.

Ví dụ Output:
{{"summary": "Phát hiện liên kết giả mạo ngân hàng", "explanation": "Đường dẫn trong tin nhắn nghi ngờ là giả mạo để chiếm đoạt tài khoản. Tuyệt đối không bấm vào link này."}}
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
             return GeminiReasoningPayload(summary=data.get("summary", ""), explanation=data.get("explanation", ""))
        except Exception as e:
             print(f"Error parsing Gemini reasoning JSON: {e}")
             return GeminiReasoningPayload(
                 summary="Hệ thống phát hiện dấu hiệu nghi ngờ.",
                 explanation="Chúng tôi khuyên bạn cẩn thận với thông tin này do hệ thống AI phát hiện các rủi ro tiềm ẩn."
             )

    def return_reasoning_to_decision_engine(self, reasoning: GeminiReasoningPayload) -> GeminiReasoningPayload:
        """Arrow: Gemini API Reasoning Engine -> Decision Engine."""
        return reasoning
