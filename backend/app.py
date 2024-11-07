from flask import Flask, request, jsonify, redirect
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/transcribe', code=302)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        file = request.files['file']
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=file
        )
        transcription = response['text']
        return jsonify({'transcription': transcription}), 200
    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
