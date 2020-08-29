from google.cloud import texttospeech as tts
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'visionAPIKey.json'

def list_voices(language_code=None):
    client = tts.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f' Voices: {len(voices)} '.center(60, '-'))
    for voice in voices:
        languages = ', '.join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f'{languages:<8}',
              f'{name:<24}',
              f'{gender:<8}',
              f'{rate:,} Hz',
              sep=' | ')

list_voices('en')