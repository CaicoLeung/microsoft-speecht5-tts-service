from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
import soundfile as sf
from datasets import load_dataset
from flask import Flask, request
from playsound3 import playsound

app = Flask(__name__)

# Initialize models
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# Load speaker embeddings once
embeddings_dataset = load_dataset(
    "Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(
    embeddings_dataset[7306]["xvector"]).unsqueeze(0)


@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        # Get text from request
        data = request.get_json()
        if not data or 'text' not in data:
            return {'error': 'No text provided'}, 400

        text = data['text']

        # Process text to speech
        inputs = processor(text=text, return_tensors="pt")
        speech = model.generate_speech(
            inputs["input_ids"], speaker_embeddings, vocoder=vocoder
        )

        # Save to file and play the audio
        sf.write("speech.wav", speech.numpy(), samplerate=16000)
        playsound("speech.wav")
        return {'success': True}, 200

    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
