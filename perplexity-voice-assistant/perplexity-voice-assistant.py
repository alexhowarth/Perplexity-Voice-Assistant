import os
import speech_recognition as sr
from pydub.playback import play
from dotenv import load_dotenv
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from openai import OpenAI

load_dotenv()

def check_envs():
    required_vars = ["PERPLEXITY_API_KEY", "ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID", "MODEL_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")


client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)


def get_audio_data():
    """Opens the microphone and returns the audio data"""
    recognizer = sr.Recognizer()
    # will probably need to use this on raspberry pi sr.Microphone.list_microphone_names()
    # mic = sr.Microphone(device_index=3)
    with sr.Microphone() as source:
        print("Listening...")
        # TODO: still returns nonesense if you don't say anything
        #recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source)
            return audio.get_wav_data()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None


def speech_to_text(audio_bytes):
    """Makes and api request to elevenlabs to convert audio to text"""
    transcription = client.speech_to_text.convert(
        file=audio_bytes,
        model_id="scribe_v1",
    )
    return transcription.text


def query_perplexity(prompt):
    """Sends the text query to perplexity api and returns the result as text"""
    messages = [
        {
            "role": "system",
            "content": (
                "Respond with only one fascinating fact, with no citations or markdown characters, kept under 50 words."
            ),
        },
        {
            "role": "user",
            "content": (
                prompt
            ),
        },
    ]

    perplexity_client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

    response = perplexity_client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    return response.choices[0].message.content


def text_to_speech(text):
    """Makes an api request to elevenlabs to convert text to speech"""
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)

def main():

    # check for required environment variables
    check_envs()

    # get audio from user
    data = get_audio_data()
    if not data:
        return

    # convert audio to text via elevenlabs
    input = speech_to_text(data)
    print(f"Input: {input}")

    # send text to perplexity for response
    perplexity_response = query_perplexity(input)
    print(f"Perplexity Response: {perplexity_response}")

    # play the response
    text_to_speech(perplexity_response)


if __name__ == "__main__":
    main()
