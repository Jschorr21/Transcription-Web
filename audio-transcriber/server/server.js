const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const openai = require('openai');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(fileUpload());

// Set your OpenAI API key
openai.apiKey = process.env.OPENAI_API_KEY;

app.post('/transcribe', async (req, res) => {
    if (!req.files || !req.files.audio) {
        return res.status(400).send('No audio file uploaded.');
    }

    const audioFile = req.files.audio;
    const filePath = path.join(__dirname, 'uploads', audioFile.name);
    audioFile.mv(filePath);

    try {
        const transcriptionResponse = await openai.Audio.transcribe({
            model: 'whisper-1',
            file: fs.createReadStream(filePath),
        });
        fs.unlinkSync(filePath); // Delete the file after transcribing
        res.json({ transcription: transcriptionResponse.text });
    } catch (error) {
        res.status(500).send(`Transcription error: ${error.message}`);
    }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
