from google.cloud import speech
from app.models.contracts import TranscribedTextPayload


class SttAgent:
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_voice_stream(self, call_session_id: str | None, stream_ref: str | None) -> str:
        """Link: Voice Stream -> Google STT API, output transcribed text."""
        if not stream_ref:
            return ""

        # For the hackathon, we assume stream_ref is a local path or a URI accessible by the client
        # In a real production system, this would be a byte stream from a socket
        
        try:
            with open(stream_ref, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="vi-VN", # Vietnamese focus for anti-scam
            )

            response = self.client.recognize(config=config, audio=audio)

            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript

            return transcript
        except Exception as e:
            print(f"Error during Google STT transcription: {e}")
            return "Transcription failed"

    def emit_transcribed_text_from_google_stt_api(
        self,
        call_session_id: str | None,
        transcript: str,
        metadata: dict[str, str],
    ) -> TranscribedTextPayload:
        """Arrow: Google STT API -> Transcribed Text stage payload."""
        return TranscribedTextPayload(
            callSessionId=call_session_id,
            transcript=transcript,
            metadata=metadata
        )

    def enrich_transcript_metadata(self, transcript: str) -> dict[str, str]:
        """Prepare transcript metadata that will be forwarded to Threat Agent."""
        # Simple heuristic enrichment: check for volume, length, or just pass through
        return {"transcript_length": str(len(transcript)), "language": "vi-VN"}

    def emit_transcribed_text_for_threat_agent(
        self,
        call_session_id: str | None,
        transcript: str,
        metadata: dict[str, str],
    ) -> TranscribedTextPayload:
        """Arrow: Google STT API -> Threat Agent, package transcript payload for Threat stage."""
        enriched_meta = self.enrich_transcript_metadata(transcript)
        metadata.update(enriched_meta)
        return TranscribedTextPayload(
            callSessionId=call_session_id,
            transcript=transcript,
            metadata=metadata
        )
