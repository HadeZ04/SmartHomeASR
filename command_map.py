from .gpio_control import (
    turn_on_all_lights, turn_off_all_lights,
    bedroom_light_on, bedroom_light_off,
    bathroom_light_on, bathroom_light_off,
    bedroom_fan_on, bedroom_fan_off,
    read_and_display_dht11,
    open_door, close_door,
    start_pir_monitoring, stop_pir_monitoring
)

from .utils import (
    play_music, pause_music, resume_music, stop_music,
    volume_up, volume_down, volume_mute
)

command_action_map = {
  // Can add more command 
    # === Lights ===
    "lights on": turn_on_all_lights,
    "lights off": turn_off_all_lights,
    "turn on the lights in the bedroom": bedroom_light_on,
    "bedroom lights on": bedroom_light_on,
    "turn off the lights in the bedroom": bedroom_light_off,
    "bedroom lights off": bedroom_light_off,
    "turn on the washroom lights": bathroom_light_on,
    "bathroom lights on": bathroom_light_on,
    "turn the washroom lights off": bathroom_light_off,

    # === Fan ===
    "make it cooler": bedroom_fan_on,
    "make it hotter": bedroom_fan_off,

    # === Temperature Sensor ===
    "increase the temperature": read_and_display_dht11,
    "decrease the temperature": read_and_display_dht11,

    # === Music ===
    "start the music": play_music,
    "play music": play_music,
    "pause music": pause_music,
    "resume music": resume_music,
    "stop": stop_music,

    # === Volume ===
    "volume mute": volume_mute,
    "turn the sound up": volume_up,
    "too quiet": volume_up,
    "turn volume down": volume_down,

    # === PIR motion detection ===
    "resume": start_pir_monitoring,
    "quieter": stop_pir_monitoring,

    # === Door ===
    "fetch my shoes": close_door,
    "go get me my shoes": open_door,
}
