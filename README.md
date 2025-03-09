# Flask Translator API

This project is a simple Flask-based translation service that translates text into different languages using Google Translate (`googletrans`) and also provides a text-to-speech feature (`gTTS`).

It includes a web interface that allows users to enter text, select a language, and get the translated text along with an audio file.

## Features

- Translate text into different languages
- Generate speech audio from translated text
- Simple frontend with an HTML interface
- API that can be used programmatically

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/Pxncho99/Translator.git
cd Translator
```

### 2. Install dependencies

Make sure you have Python installed, then run:

```sh
pip install -r requirements.txt
```

### 3. Run the application

Execute the script with:

```sh
python app.py
```

The server will start at `http://localhost:5555/`.

### 4. Open the web interface

Go to your browser and open:

```
http://localhost:5555/
```

### Usage

  1. Select the language you want to translate your text into (currently available options: English, Spanish, French, and Chinese).
  2. Enter the text you want to translate (it can be in any language).
  3. Press Enter or click the `Translate` button.
  4. Your translation will be displayed, and you can also press the `Play Audio` button to listen to it.

## Dependencies

- Flask
- flask-cors
- googletrans
- gtts (Google Text-to-Speech)

## License

This project is open-source and available under the MIT License.

