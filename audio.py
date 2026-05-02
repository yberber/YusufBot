import os
from groq import Groq

STT_MODELS = {
    "whisper-large-v3-turbo": "Whisper Large v3 Turbo (Fast)",
    "whisper-large-v3": "Whisper Large v3",
}

TTS_MODEL = "canopylabs/orpheus-v1-english"
TTS_VOICES = ["tara", "leah", "leo", "dan", "mia", "zac", "zoe"]


def transcribe(audio_bytes: bytes, filename: str, stt_model: str) -> str:
    """Convert recorded audio to text using Groq Whisper. Raises groq.RateLimitError on limit."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    result = client.audio.transcriptions.create(
        model=stt_model,
        file=(filename, audio_bytes),
    )
    return result.text


def synthesize(text: str, voice: str) -> bytes:
    """Convert text to speech using Groq Orpheus. Raises groq.RateLimitError on limit."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=voice,
        input=text,
        response_format="wav",
    )
    return response.read()
