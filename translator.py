from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Importar CORS
from googletrans import Translator  # Importar Google Translator
from gtts import gTTS  # Import gTTS for Text-to-Speech
import os
from threading import Thread

# Crear la app de Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)  # Esto habilita CORS para todos los orígenes

# Initialize the translator
translator = Translator()

# Directory to save audio files
AUDIO_DIR = "static/audio"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# HTML como un string (lo puedes modificar)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba de Servicio de Traducción</title>
    <script>
        async function sendPrediction() {
            const text = document.getElementById("inputText").value;
            const language = document.getElementById("languageSelect").value;  // Get the selected language
            if (text.trim() === "") return;  // Prevent sending empty input

            const response = await fetch("http://localhost:5555/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text, language: language })  // Send language with the text
            });

            const data = await response.json();
            document.getElementById("predictionResult").innerText = `Translation: ${data.prediction}`;
            document.getElementById("audioButton").style.display = "inline"; // Show audio button
            document.getElementById("audioButton").onclick = () => playAudio(data.audio_url); // Set audio button click
        }

        // Function to play the translated audio
        function playAudio(audioUrl) {
            const audio = new Audio(audioUrl);
            audio.play();
        }

        // Detect Enter key press inside the textarea
        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("inputText").addEventListener("keydown", function (event) {
                if (event.key === "Enter" && !event.shiftKey) { 
                    event.preventDefault();  // Prevents new line in textarea
                    sendPrediction();  // Trigger prediction
                }
            });
        });
    </script>
</head>
<body>
    <div style="max-width: 600px; margin: 0 auto; text-align: center;">
        <h1>Translator</h1>
        
        <!-- Dropdown for selecting language -->
        <label for="languageSelect">Output Language:</label>
        <select id="languageSelect">
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="fr">Français</option>
            <option value="zh-cn">中文 (Chinese)</option>
        </select>
        <br><br>

        <textarea id="inputText" rows="4" cols="50" placeholder="Write something to translate..."></textarea>
        <br><br>
        <button onclick="sendPrediction()">Translate</button>
        <p id="predictionResult" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></p>

        <!-- Audio button -->
        <button id="audioButton" style="display: none;">Play Audio</button>
    </div>
</body>
</html>
"""

# Ruta para servir el HTML
@app.route("/")
def home():
    return html_content

# Ruta para la predicción
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data["text"]
    language = data["language"]

    # Translate the text to the desired language
    translated = translator.translate(text, dest=language)
    translated_text = translated.text  # Extract the translated text

    # Generate audio for the translated text
    tts = gTTS(translated_text, lang=language)
    audio_filename = f"{str(hash(translated_text))}.mp3"  # Use hash to create a unique filename
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    tts.save(audio_path)

    # Return the translated text and the audio URL
    audio_url = f"/static/audio/{audio_filename}"
    
    return jsonify({"prediction": translated_text, "audio_url": audio_url})

# Serve the audio file
@app.route("/static/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

# Ejecutar Flask en un hilo
def run_flask():
    app.run(host="0.0.0.0", port=5555)

# Crear un hilo para ejecutar Flask
if __name__ == '__main__':
    thread = Thread(target=run_flask)
    thread.start()