# === main.py ===
import threading
from smart_home.gui import start_gui_control_panel
from smart_home.voice import main_loop, test_command_input
from smart_home.utils import speak_text

if __name__ == "__main__":
    threading.Thread(target=start_gui_control_panel, daemon=True).start()

    while True:
        mode = input("Enter mode (main/test): ").strip().lower()
        if mode == "test":
            test_command_input()
            break
        elif mode == "main":
            main_loop()
            break
        else:
            print("Invalid mode. Please type 'main' or 'test'.")
            speak_text("Please type main or test")
