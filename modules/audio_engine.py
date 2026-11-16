import openai

def transcribe_audio_with_whisper(client, audio_file):
    """
    Takes an audio file uploaded/recorded in Streamlit and sends it to OpenAI Whisper 
    to convert speech to accurate text.
    """
    try:
        # Call OpenAI Whisper API
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ar"  # تدعم اللغة العربية والإنجليزية بمرونة
        )
        return transcript.text
    except Exception as e:
        return f"Error in Whisper transcription: {str.error if hasattr(e, 'error') else str(e)}"
