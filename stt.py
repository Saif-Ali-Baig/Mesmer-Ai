import os
import torch
import speechbrain as sb
from speechbrain.inference.ASR import EncoderDecoderASR
import wave
import numpy as np

model_path = os.path.join(os.path.dirname(__file__), "speechbrain-model-en")
print(f"Checking model path: {model_path}, exists: {os.path.exists(model_path)}")

if not os.path.exists(model_path):
    raise Exception(f"Model folder {model_path} not found")

# Load the pre-trained ASR model
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-crdnn-rnnlm-librispeech",
    savedir=model_path
)
asr_model.eval()  # Set to evaluation mode

def process_stt(audio_bytes):
    try:
        # Write bytes to a temporary WAV file
        with wave.open('temp.wav', 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            wav_file.writeframes(audio_bytes)

        # Read the WAV file and convert to tensor
        with wave.open('temp.wav', 'rb') as wav_file:
            samples = wav_file.readframes(wav_file.getnframes())
            audio_data = np.frombuffer(samples, dtype=np.int16)
            signal = torch.FloatTensor(audio_data).unsqueeze(0) / 32768.0  # Normalize to [-1, 1]
            wav_lens = torch.tensor([1.0])  # Length of the audio (single sample)

        # Transcribe
        with torch.no_grad():
            prediction = asr_model.transcribe_batch(signal, wav_lens=wav_lens)
            text = prediction[0]  # Assuming batch output
            return text, "en-US"
    except Exception as e:
        # Fallback to transcribe_file if batch fails
        try:
            with wave.open('temp.wav', 'rb') as wav_file:
                prediction = asr_model.transcribe_file(wav_file.name)
                return prediction, "en-US"
        except Exception as e2:
            return f"Error processing speech: {str(e)} or {str(e2)}", None
    finally:
        if os.path.exists('temp.wav'):
            os.remove('temp.wav')

if __name__ == "__main__":
    import sys
    audio_bytes = sys.stdin.buffer.read()
    text, lang = process_stt(audio_bytes)
    print(f"Text: {text}, Language: {lang}")