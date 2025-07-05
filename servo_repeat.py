import RPi.GPIO as GPIO
import time

# Constants
SERVO_PIN = 18  # Change this to the correct GPIO pin number
FREQ = 50       # 50Hz for hobby servo

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, FREQ)
servo.start(0)

def set_angle(angle):
    """Convert angle (0-180) to PWM duty cycle and send it to servo."""
    duty = 2 + (angle / 18)  # Map angle to duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.002)         # Short delay for smooth movement
    servo.ChangeDutyCycle(0)  # Stop signal to avoid jitter

try:
    while True:
        # Sweep from 0 to 160 degrees
        for pos in range(0, 180):  # 0 to 160
            set_angle(pos)

        # Sweep from 160 back to 0 degrees
        for pos in range(180, -1, -1):  # 160 to 0
            set_angle(pos)
        time.sleep(3)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    servo.stop()
    GPIO.cleanup()
    print("Servo sweep test complete.")
