# === gpio_control.py ===
from gpiozero import LED, OutputDevice, AngularServo, MotionSensor
import board
import adafruit_dht
import threading
from time import sleep
from .utils import speak_text

# Devices
bedroom_light = LED(26)
bathroom_light = LED(19)
relay_fan = OutputDevice(21, active_high=True, initial_value=False)
pir_sensor = MotionSensor(18)
dht_device = adafruit_dht.DHT11(board.D4)
servo1 = None
servo2 = None

# Lights

def turn_on_all_lights():
    bedroom_light.on()
    bathroom_light.on()
    speak_text("Turned on all lights")

def turn_off_all_lights():
    bedroom_light.off()
    bathroom_light.off()
    speak_text("Turned off all lights")

def bedroom_light_on(): bedroom_light.on(); speak_text("Bedroom light on")
def bedroom_light_off(): bedroom_light.off(); speak_text("Bedroom light off")
def bathroom_light_on(): bathroom_light.on(); speak_text("Bathroom light on")
def bathroom_light_off(): bathroom_light.off(); speak_text("Bathroom light off")

# Fan

def bedroom_fan_on(): relay_fan.on(); speak_text("Fan on")
def bedroom_fan_off(): relay_fan.off(); speak_text("Fan off")

# Temperature and Humidity

def read_and_display_dht11():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if humidity is not None and temperature is not None:
            speak_text(f"Temperature is {temperature:.1f}C, humidity {humidity:.1f}%")
        else:
            speak_text("Sensor error.")
    except RuntimeError as e:
        speak_text("Sensor read error.")
    sleep(2)

# Servo/Door

def get_servo(pin, servo_id):
    global servo1, servo2
    if servo_id == 1 and servo1 is None:
        servo1 = AngularServo(pin, min_angle=0, max_angle=180,
                              min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    if servo_id == 2 and servo2 is None:
        servo2 = AngularServo(pin, min_angle=0, max_angle=180,
                              min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    return servo1 if servo_id == 1 else servo2

def smooth_move(servo, start_angle, end_angle, step=1, delay=0.05):
    step = abs(step) if start_angle < end_angle else -abs(step)
    for angle in range(start_angle, end_angle + step, step):
        servo.angle = max(0, min(180, angle))
        sleep(delay)

def move_door(servo_id, target_angle, text):
    pin = 17 if servo_id == 1 else 16
    servo = get_servo(pin, servo_id)
    current_angle = int(servo.angle) if servo.angle is not None else (0 if target_angle > 0 else 90)
    threading.Thread(target=lambda: smooth_move(servo, current_angle, target_angle)).start()
    speak_text(text)

def open_door():
    move_door(1, 90, "Door 1 opened")
    move_door(2, 90, "Door 2 opened")

def close_door():
    move_door(1, 0, "Door 1 closed")
    move_door(2, 0, "Door 2 closed")

# PIR motion
pir_monitoring = False
pir_thread = None

def pir_monitor_loop():
    global pir_monitoring
    speak_text("Motion detection activated")
    while pir_monitoring:
        if pir_sensor.is_active:
            speak_text("Motion detected")
        else:
            speak_text("No motion")
        sleep(0.5)

def start_pir_monitoring():
    global pir_monitoring, pir_thread
    if not pir_monitoring:
        pir_monitoring = True
        pir_thread = threading.Thread(target=pir_monitor_loop, daemon=True)
        pir_thread.start()
    else:
        speak_text("Motion detection already active")

def stop_pir_monitoring():
    global pir_monitoring
    pir_monitoring = False
    speak_text("Motion detection stopped")

