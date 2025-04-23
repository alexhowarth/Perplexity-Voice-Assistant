# Perplexity Voice Assistant #

Create a .env file and populate it with your API keys:

```
# Perplexity API settings
PERPLEXITY_API_KEY=<key>

# Eleven Labs settings
ELEVENLABS_API_KEY=<key>
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
MODEL_ID=scribe_v1
```

Optionally you can override the default system prompt by setting `PERPLEXITY_SYSTEM_PROMPT` in the `.env` file.

On Raspberry Pi you might need to install the portaudio dev files:

```$ sudo apt install portaudio19-dev```

To get up and running:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ python perplexity-voice-assistant/perplexity-voice-assistant.py
```