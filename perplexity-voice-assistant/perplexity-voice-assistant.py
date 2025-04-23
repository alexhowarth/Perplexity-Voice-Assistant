import os
import speech_recognition as sr
from pydub.playback import play
from dotenv import load_dotenv
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from openai import OpenAI

load_dotenv()


def validate_environment_variables():
    """Ensure all required environment variables are set."""
    required_vars = ["PERPLEXITY_API_KEY", "ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID", "MODEL_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")


def initialize_elevenlabs_client():
    """Initialize and return the ElevenLabs client."""
    return ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def capture_audio():
    """Capture audio from the microphone and return it as WAV data."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            return audio.get_wav_data()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return None


def transcribe_audio_to_text(client, audio_bytes):
    """Convert audio bytes to text using ElevenLabs."""
    return client.speech_to_text.convert(
        file=audio_bytes,
        model_id="scribe_v1",
    ).text

def get_system_prompt():
    """Retrieve the system prompt from the environment or use a default value."""
    return os.getenv("PERPLEXITY_SYSTEM_PROMPT", "Respond with only one fascinating fact, with no citations or markdown characters, kept under 50 words.")

def query_perplexity_api(prompt):
    """Send a text query to the Perplexity API and return the response."""

    messages = [
        {
            "role": "system",
            "content": (
                get_system_prompt()
            ),
        },
        {"role": "user", "content": prompt},
    ]

    perplexity_client = OpenAI(
        api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai"
    )

    response = perplexity_client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    return response.choices[0].message.content


def synthesize_text_to_speech(client, text):
    """Convert text to speech using ElevenLabs and play the audio."""
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)


def main():
    """Main function to orchestrate the voice assistant workflow."""
    try:
        validate_environment_variables()
        elevenlabs_client = initialize_elevenlabs_client()

        synthesize_text_to_speech(elevenlabs_client,"How can I help you?")

        audio_data = capture_audio()
        if not audio_data:
            return

        user_input = transcribe_audio_to_text(elevenlabs_client, audio_data)
        print(f"Input: {user_input}")

        response = query_perplexity_api(user_input)
        print(f"Perplexity Response: {response}")

        synthesize_text_to_speech(elevenlabs_client, response)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
