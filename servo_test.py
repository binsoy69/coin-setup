
import RPi.GPIO as GPIO
import time

# Set the GPIO pin connected to the orange signal wire
SERVO_PIN = 18  # Change this if you connected to another pin

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM to 50Hz (standard for hobby servos)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

def set_angle(angle):
    """Move servo to specified angle (0 to 180 degrees)"""
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)  # Stop signal to avoid jitter

try:
	while True:
		#Ask user for angle and turn servo to it
		angle = float(input('Enter angle between 0 & 180: '))
		set_angle(angle)
		
except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
	servo.stop()
	GPIO.cleanup()
	print("Servo test complete.")
