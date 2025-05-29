from .audio import record_audio, predict_single_wav_tflite
from .command_map import command_action_map
from .utils import speak_text, is_music_playing
import time

is_listening = False

def execute_command(text):
    from fuzzywuzzy import process
    text = text.lower().strip()
    best_match, score = process.extractOne(text, command_action_map.keys())
    if score >= 85:
        try:
            print(f"Executing: '{best_match}' (score: {score})")
            speak_text(f"You said: {best_match}")
            command_action_map[best_match]()
        except Exception as e:
            print(f"[ERROR] Cannot execute '{best_match}': {e}")
            speak_text("Sorry, I cannot do that.")
    else:
        print("Unrecognized command:", text)
        speak_text("I don't understand the command.")

def predict(duration=5, gain=1.5, use_file=None):
    global is_listening
    is_listening = True
    try:
        wav_file = use_file if use_file else record_audio("predict_input.wav", duration)
        is_listening = False
        text = predict_single_wav_tflite(wav_file, gain=gain).strip().capitalize()
        print(f"[Predict] Recognized: \"{text}\"")
        speak_text(f"You said: {text}")
        return text
    except Exception as e:
        is_listening = False
        print(f"[ERROR] Predict failed: {e}")
        speak_text("Recognition failed.")
        return ""

def main_loop():
    global is_listening
    speak_text("Voice listening mode activated")
    while True:
        try:
            resume_music = False
            if is_music_playing():
                resume_music = True
                media_player.pause()

            is_listening = True
            wav_file = record_audio("command.wav", duration=5)
            is_listening = False
            transcription = predict_single_wav_tflite(wav_file, gain=1.5)
            print(f"Recognized: {transcription}")
            execute_command(transcription)

            if resume_music:
                time.sleep(0.5)
                media_player.play()
        except Exception as e:
            is_listening = False
            print(f"[ERROR] Voice command error: {e}")
            speak_text("There was a problem recognizing your voice.")
        time.sleep(1)

def test_command_input():
    speak_text("Test mode started. Please enter a command.")
    while True:
        command_text = input(">> ").strip().lower()
        if command_text == "exit":
            speak_text("Exiting test mode.")
            break
        execute_command(command_text)
