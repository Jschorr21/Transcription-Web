from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={
    r"/transcribe": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5000",
            "https://transcription-web-app-c2a72a351913.herokuapp.com"
        ]
    }
})

# Root route with an HTML form for file upload
@app.route('/', methods=['GET'])
def home():
    return render_template_string('''
        <!doctype html>
        <title>Upload Audio for Transcription</title>
        <h1>Upload Audio for Transcription</h1>
        <form action="/transcribe" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload and Transcribe">
        </form>
    ''')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # Step 1: Retrieve the uploaded file from the form
        file = request.files['file']
        
        # Step 2: Open and process the file for transcription
        with file.stream as audio_file:  # Use `file.stream` for reading directly
            transcription_response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        
        # Step 3: Extract transcription text
        transcription = transcription_response['text']

        # Step 4: Display the transcription on the web page
        return render_template_string('''
            <!doctype html>
            <title>Transcription Result</title>
            <h1>Transcription</h1>
            <p>{{ transcription }}</p>
            <a href="/">Upload Another File</a>
        ''', transcription=transcription)
    
    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
