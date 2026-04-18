import os
import google.generativeai as genai
import time

class GeminiClient:
    def __init__(self):
        # Configure Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model_name = "models/gemini-1.5-flash-latest" # Using 1.5 for audio support
        self.model = genai.GenerativeModel(self.model_name)

    async def generate_content(self, prompt: str, system_instruction: str = None) -> str:
        """Thực hiện gọi Gemini để lấy text analysis hoặc reasoning."""
        try:
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
            else:
                model = genai.GenerativeModel(model_name=self.model_name)
                
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return f"Error: {e}"

    async def analyze_audio_async(self, audio_path: str, prompt: str) -> str:
        """Upload and analyze audio file for deepfake/heuristic detection."""
        try:
            if not os.path.exists(audio_path):
                return f"Error: Audio file not found at {audio_path}"

            # Upload to Gemini File API
            audio_file = genai.upload_file(path=audio_path)
            
            # Wait for processing if needed (usually instant for small files)
            while audio_file.state.name == "PROCESSING":
                time.sleep(1)
                audio_file = genai.get_file(audio_file.name)

            model = genai.GenerativeModel(model_name=self.model_name)
            response = await model.generate_content_async([prompt, audio_file])
            
            # Clean up: Files automatically expire after 48h, but we can delete manually if desired
            # genai.delete_file(audio_file.name)
            
            return response.text
        except Exception as e:
            print(f"Error analyzing audio with Gemini: {e}")
            return f"Error: {e}"
