import ffmpeg
from flask import Flask, request, send_file
import os

app = Flask(__name__)


@app.route("/", methods=['GET'])
def boot():
    return "booted UP!"


@app.route("/convert", methods=['POST'])
def getdata():
    if os.path.exists("result.wav"):
        os.remove("result.wav ")
    else:
        print("The file does not exist")
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    if file and allowed_file(file.filename):
        file.save('temp.wav')
        ffmpeg.input("temp.wav") \
            .output('result.wav', acodec='pcm_u8', **{'bitexact': None}).run()

        return send_file('result.wav', mimetype='audio/wav')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() == 'wav'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8443)
