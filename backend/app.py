from flask import Flask, request, jsonify, render_template_string
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        # Use the new method for transcription
        response = openai.Audio.create(
            file=file,
            model="whisper-1"
        )
        transcription = response['text']
        return jsonify({'transcription': transcription}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
