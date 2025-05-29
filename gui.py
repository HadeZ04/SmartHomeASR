# === gui.py ===
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from .voice import predict, execute_command
from .utils import is_music_playing, speak_text
from .gpio_control import (
    bedroom_light_on, bedroom_light_off,
    bathroom_light_on, bathroom_light_off,
    turn_on_all_lights, turn_off_all_lights,
    bedroom_fan_on, bedroom_fan_off,
    open_door, close_door,
    read_and_display_dht11, start_pir_monitoring
)
from .utils import (
    play_music, pause_music, volume_up, volume_down
)
import time


def on_screen_listen_command():
    from .audio import record_audio, predict_single_wav_tflite
    if is_music_playing():
        pause_music()
        time.sleep(0.3)
    wav_file = record_audio(filename="command.wav", duration=5)
    transcription = predict_single_wav_tflite(wav_file, gain=1.5)
    print(f"Recognized: {transcription}")
    execute_command(transcription)
    time.sleep(0.5)

def toggle_music():
    if is_music_playing():
        pause_music()
    else:
        play_music()

def start_gui_control_panel():
    window = tk.Tk()
    window.title("Smart Home Control Panel")
    window.geometry("820x600")
    window.configure(bg="#f0f2f5")
    default_font = ("Segoe UI", 13, "bold")

    def create_button(master, text, command, bg_color):
        btn = tk.Button(
            master, text=text, command=lambda: [btn_press_effect(btn, bg_color), command()],
            font=default_font, bg=bg_color, fg="white",
            activebackground="#333333", activeforeground="white",
            padx=8, pady=8, bd=0, relief="flat", width=20, height=1
        )
        def on_enter(e): btn.config(bg="#555555")
        def on_leave(e): btn.config(bg=bg_color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        def btn_press_effect(button, original_color):
            button.config(bg="#222222")
            button.after(500, lambda: button.config(bg=original_color))
        return btn

    def create_tooltip(widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        label.pack()
        def enter(event):
            x, y = widget.winfo_pointerxy()
            tooltip.geometry(f"+{x+10}+{y+10}")
            tooltip.deiconify()
        def leave(event): tooltip.withdraw()
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    # Mic icon button
    try:
        mic_img_raw = Image.open("/home/thith/mic.jpeg").resize((64, 64))
        mic_img = ImageTk.PhotoImage(mic_img_raw)
        mic_button = tk.Button(window, image=mic_img, command=on_screen_listen_command,
                               bd=0, bg="#f0f2f5", activebackground="#dcdcdc", cursor="hand2")
        mic_button.image = mic_img
        mic_button.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        mic_button.bind("<Enter>", lambda e: mic_button.config(bg="#dcdcdc"))
        mic_button.bind("<Leave>", lambda e: mic_button.config(bg="#f0f2f5"))
        create_tooltip(mic_button, "Click to speak")
    except Exception as e:
        print("[WARNING] Mic icon not loaded:", e)

    controls = [
        ("Predict Your Voice", predict, "#000c03"),
        ("Play / Pause Music", toggle_music, "#007bff"),
        ("Volume Up", volume_up, "#007bff"),
        ("Volume Down", volume_down, "#007bff"),
        ("Turn On Bedroom Light", bedroom_light_on, "#ff0000"),
        ("Turn Off Bedroom Light", bedroom_light_off, "#ff0000"),
        ("Switch On Bathroom Light", bathroom_light_on, "#ff0000"),
        ("Switch Off Bathroom Light", bathroom_light_off, "#ff0000"),
        ("Turn On All Lights", turn_on_all_lights, "#00ff40"),
        ("Turn Off All Lights", turn_off_all_lights, "#00ff40"),
        ("Turn On Fan", bedroom_fan_on, "#ffcc00"),
        ("Turn Off Fan", bedroom_fan_off, "#ffcc00"),
        ("Open Door", open_door, "#ff5e00"),
        ("Close Door", close_door, "#ff5e00"),
        ("Read Temperature", read_and_display_dht11, "#ff0051"),
        ("Check PIR", start_pir_monitoring, "#ff0051"),
    ]

    for i, (label, cmd, color) in enumerate(controls):
        row = (i // 2) + 1
        col = i % 2
        btn = create_button(window, label, cmd, color)
        btn.grid(row=row, column=col, padx=20, pady=10, sticky="ew")

    for c in range(2):
        window.grid_columnconfigure(c, weight=1)

    window.resizable(False, False)
    window.mainloop()

# Next: requirements.txt and README.md
