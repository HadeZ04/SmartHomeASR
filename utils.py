# === utils.py ===
import subprocess
import time
import vlc

is_listening = False
media_player = vlc.MediaPlayer("/home/thith/videoplayback.mp4")

def speak_text(text):
    global is_listening
    if is_listening:
        print(f"[TTS BLOCKED] {text}")
        return
    print(f"[TTS] {text}")
    subprocess.run(["espeak", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.5)

def is_music_playing():
    return media_player.is_playing()

def play_music():
    media_player.play()
    speak_text("Playing music now")

def pause_music():
    media_player.pause()
    speak_text("Music paused")

def resume_music():
    media_player.play()
    speak_text("Music resumed")

def stop_music():
    media_player.stop()
    speak_text("Music stopped")

def volume_mute():
    media_player.audio_toggle_mute()
    speak_text("Volume muted or unmuted")

def volume_up():
    v = min(media_player.audio_get_volume() + 10, 100)
    media_player.audio_set_volume(v)
    speak_text(f"Volume up to {v} percent")

def volume_down():
    v = max(media_player.audio_get_volume() - 10, 0)
    media_player.audio_set_volume(v)
    speak_text(f"Volume down to {v} percent")
