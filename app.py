from flask import Flask, request, render_template, jsonify
import requests
import os
import wave
import pyaudio

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Your Groq API key (ensure it's securely stored in production)
GROQ_API_KEY = "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"

def save_audio(file):
    """Save uploaded audio file."""
    audio_path = os.path.join(UPLOAD_FOLDER, "realtime_audio.wav")
    file.save(audio_path)
    return audio_path

def process_audio_and_generate_art(audio_path):
    """Process audio using Groq API and generate art (Modify logic as per Groq's requirements)."""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    # Example request (Modify based on Groq’s actual API requirements)
    response = requests.post(
        "https://api.groq.com/v1/generate",
        headers=headers,
        json={"prompt": "Generate art from this audio file."}  # Modify as needed
    )

    if response.status_code == 200:
        return response.json().get("art_url", "Error: No image generated")
    return "Error: API request failed"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    """Receives audio, processes it, and returns generated art URL."""
    audio_file = request.files["audio"]
    audio_path = save_audio(audio_file)
    art_url = process_audio_and_generate_art(audio_path)
    return jsonify({"art_url": art_url})

if __name__ == "__main__":
    app.run(debug=True)
