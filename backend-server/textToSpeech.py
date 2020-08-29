from google.cloud import texttospeech as tts
from playsound import playsound
import os
from pydub import AudioSegment
from pydub.playback import play
import subprocess
import vlc

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'visionAPIKey.json'

def text_to_wav(voice_name, text):
    language_code = '-'.join(voice_name.split('-')[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name)
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config)

    filename = f'{language_code}.wav'
    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')
    return filename

wavFile = text_to_wav('en-US-Wavenet-A', "ni hao monkey kim")
absFile = os.path.abspath(wavFile)
print(absFile)
subprocess.call(['vlc', absFile])
