from flask import Flask, request, jsonify, redirect, render_template_string
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Root route with an HTML form for file upload
@app.route('/', methods=['GET'])
def home():
    return render_template_string('''
        <!doctype html>
        <title>Upload Audio for Transcription</title>
        <h1>Upload Audio for Transcription</h1>
        <form action="/transcribe" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload and Transcribe">
        </form>
    ''')

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
