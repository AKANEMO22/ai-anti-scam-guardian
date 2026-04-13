import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        # Configure Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model_name = "models/gemini-flash-latest"
        self.model = genai.GenerativeModel(self.model_name)

    async def generate_content(self, prompt: str, system_instruction: str = None) -> str:
        """Thực hiện gọi Gemini để lấy text analysis hoặc reasoning."""
        try:
            # Recreate model locally to avoid caching issues across threads/coroutines
            model_name = "models/gemini-flash-latest"
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
            else:
                model = genai.GenerativeModel(model_name=model_name)
                
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return f"Error: {e}"
