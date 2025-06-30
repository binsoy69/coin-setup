import RPi.GPIO as GPIO
import time
from datetime import datetime

# GPIO Pins
COIN_PIN = 17      # Coin pulse input
SERVO_PIN = 18     # Servo signal output

# Coin pulse denomination mapping
COIN_MAP = {
    1: "1",
    5: "5",
    10: "10",
    20: "20"
}

# Sorting categories
CATEGORY_1 = ["1", "5"]
CATEGORY_2 = ["10", "20"]

# Servo angles
NEUTRAL= 90
LEFT = 45
RIGHT= 135

# Timing control
COIN_TIMEOUT = 0.5  # Max time between pulses in a group
pulse_count = 0
last_pulse_time = time.time()

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Servo PWM setup
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

# Helper: move servo to angle
def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

# Start at neutral
set_angle(NEUTRAL)

# Coin pulse interrupt handler
def coin_pulse_callback(channel):
    global pulse_count, last_pulse_time
    now = time.time()

    if now - last_pulse_time > COIN_TIMEOUT:
        pulse_count = 0  # Reset if time gap is too large

    pulse_count += 1
    last_pulse_time = now

# Register interrupt
GPIO.add_event_detect(COIN_PIN, GPIO.FALLING, callback=coin_pulse_callback, bouncetime=5)

print("Coin sorting system ready. Insert coins...")

try:
    while True:
        now = time.time()
        if pulse_count > 0 and (now - last_pulse_time > COIN_TIMEOUT):
            # Interpret pulses
            coin_value = COIN_MAP.get(pulse_count, None)
            if coin_value:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Coin inserted: {coin_value}")
                
                # Sort based on category
                if coin_value in CATEGORY_1:
                    print("Sorting: CATEGORY 1 (1 or 5) LEFT")
                    set_angle(LEFT_ANGLE)
                elif coin_value in CATEGORY_2:
                    print("Sorting: CATEGORY 2 (10 or 20) RIGHT")
                    set_angle(RIGHT_ANGLE)
                else:
                    print("Coin detected but not in any category.")
                
                # Return to neutral
                time.sleep(0.5)
                set_angle(NEUTRAL_ANGLE)
            else:
                print(f"Unknown coin with {pulse_count} pulses")

            pulse_count = 0  # Reset for next coin

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("System shut down.")

