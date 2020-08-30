import io, os
import argparse
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
import pandas as pd
import vlc
import base64

from flask import Flask, request, make_response, Response
from flask_cors import CORS

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

import io
from PIL import Image

from functions import analysis

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'visionAPIKey.json'

speechClient = texttospeech.TextToSpeechClient()
client = vision.ImageAnnotatorClient()
translateClient = translate.Client()

FILENAME = 'workers.png'
FOLDER_PATH = r'/mnt/c/Users/Peter/Documents/PythonVenv/SyncHack/image'


# Returns language and related code for function translateText
def getLanguageCode(code):
    result = translateClient.get_languages()
    languageList = pd.DataFrame(result)

    print(languageList)


# Translates language
def translateText(text, target):
    output = translateClient.translate(text, target)

    return output


def text_to_wav(voice_name, text):
    language_code = '-'.join(voice_name.split('-')[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config)

    filename = f'{language_code}.wav'
    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')
    return filename


def imageToSpeech(imageBase64):
    # print(imageBase64)
    content = base64.b64decode(imageBase64)
    # with io.open(os.path.join(FOLDER_PATH, filename), 'rb') as imageFile:
    # content = imageFile.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )

    textOutput = ""
    try:
        textOutput = df['description'][0]
        # Translate other languages into english
        # textOutput = translateText(textOutput, "en")
        print(textOutput)
    except:
        print("No text found")

    wavFilePath = text_to_wav('en-US-Wavenet-F', textOutput)
    wavAbsFilePath = os.path.abspath(wavFilePath)
    return wavAbsFilePath


app = Flask(__name__)
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"*": {"origins": "*"}}
CORS(app)

@app.route("/", methods=['GET', 'POST'])
def hello():
    # request.get_data()
    imageBase64 = request.data.decode("utf-8")
    print(type(imageBase64))
    print(type(request.data))

    decoded = base64.decodebytes(request.data)

    fd = os.open("file.jpg", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

    os.write(fd, decoded)

    os.close(fd)

    analysis("file.jpg")


    wavAbsFilePath = imageToSpeech(imageBase64)
    with io.open(wavAbsFilePath, 'rb') as wavFile:
        resp = Response(base64.b64encode(wavFile.read()))
    return resp


if __name__ == "__main__":
    app.run(debug=True)