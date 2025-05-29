# === audio.py ===
import wave
import pyaudio
import tensorflow as tf
import numpy as np
import librosa
from .config import AUDIO_SAMPLE_RATE, MODEL_PATH, VOCAB_PATH
from tensorflow import keras

with open(VOCAB_PATH, "r", encoding="utf-8") as f:
    vocabulary = [line.rstrip("\n") for line in f]

char_to_num = keras.layers.StringLookup(vocabulary=vocabulary, oov_token="", mask_token=None)
num_to_char = keras.layers.StringLookup(vocabulary=vocabulary, oov_token="", mask_token=None, invert=True)

frame_length = 100
frame_step = 50
fft_length = 256

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def decode_batch_predictions_tflite(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    results = tf.keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]
    output_text = []
    for result in results:
        text = tf.strings.reduce_join(num_to_char(result)).numpy().decode("utf-8")
        output_text.append(text)
    return output_text

def record_audio(filename="recorded.wav", duration=5, fs=AUDIO_SAMPLE_RATE):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    device_index = 0
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels, rate=fs,
                        input=True, input_device_index=device_index, frames_per_buffer=chunk)
    frames = [stream.read(chunk, exception_on_overflow=False) for _ in range(0, int(fs / chunk * duration))]
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return filename

def predict_single_wav_tflite(file_path, gain=1.5):
    audio, sr = librosa.load(file_path, sr=AUDIO_SAMPLE_RATE)
    audio *= gain
    audio = tf.clip_by_value(audio, -1.0, 1.0)
    audio = tf.convert_to_tensor(audio, dtype=tf.float32)
    stft = tf.signal.stft(audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length)
    spectrogram = tf.abs(stft)
    spectrogram = tf.pow(spectrogram, 0.5)
    means = tf.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)
    spectrogram = tf.expand_dims(spectrogram, axis=0)
    interpreter.resize_tensor_input(input_details[0]['index'], spectrogram.shape)
    interpreter.allocate_tensors()
    interpreter.set_tensor(input_details[0]['index'], spectrogram.numpy())
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    decoded = decode_batch_predictions_tflite(output)
    return decoded[0]
