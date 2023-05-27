from flask import Flask, request, make_response
from flask_cors import CORS
import ttsmms
import soundfile as sf
import numpy as np
from datetime import datetime
import urllib.parse
import tarfile
import requests
import os

app = Flask(__name__)
CORS(app)


def download_model():
    model_url = "https://dl.fbaipublicfiles.com/mms/tts/shn.tar.gz"
    model_path = "./model"

    os.makedirs(model_path, exist_ok=True)
    if (
        os.path.exists(os.path.join(model_path, "shn/G_100000.pth"))
        and os.path.exists(os.path.join(model_path, "shn/config.json"))
        and os.path.exists(os.path.join(model_path, "shn/vocab.txt"))
    ):
        return True

    response = requests.get(model_url, stream=True)
    file_name = model_url.split("/")[-1]
    file_path = os.path.join(model_path, file_name)

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    tar = tarfile.open(file_path, "r:gz")
    tar.extractall(model_path)
    tar.close()

    return True


@app.route("/")
def home_front():
    return "<div style='display: flex; flex-direction: column; height: 100vh; justify-content: center; align-items: center'><h2>A quick playground for Shan TTSMMS</h2><h4>api usage: /api/&lt;text&gt;</h4></div>"


@app.route("/api", methods=["GET"])
def home_route():
    response = make_response()
    response.headers["Content-type"] = "text/plain"
    response.data = "Usage: /api/<text>"

    return response


@app.route("/api/<path:text>", methods=["GET"])
def api_route(text):
    response = make_response()
    if request.method == "GET":
        response.headers["Access-Control-Allow-Origin"] = "*"
        decoded_text = urllib.parse.unquote(text)

        if download_model():
            audio_data = generate_wav_file(text=decoded_text)
            response.data = audio_data
            response.headers["Content-type"] = "audio/wav"
        else:
            response.headers["Content-type"] = "text/plain"
            response.data = "Something Wrong, please try again."

        return response
    else:
        return make_response("Not Found", 404)


def generate_wav_file(text):
    tts = ttsmms.TTS("./model/shn")

    output = tts.synthesis(text)
    wav_array = output["x"]
    sampling_rate = output["sampling_rate"]

    wav_array = (wav_array * 32767).astype(np.int16)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"temp/temp_{timestamp}.wav"

    with sf.SoundFile(
        filename, "w", samplerate=sampling_rate, channels=1, format="WAV"
    ) as f:
        f.write(wav_array)

    with open(filename, "rb") as f:
        audio_data = f.read()

    return audio_data


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
