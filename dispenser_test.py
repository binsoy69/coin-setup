import RPi.GPIO as GPIO
import time

# Map denominations to GPIO pins
DISPENSER_SERVOS = {
    "1": 18,
    "5": 17,
    "10": 27,
    "20": 22
}

# Setup GPIO
GPIO.setmode(GPIO.BCM)
servo_pwms = {}

# Setup Angle
BACKWARD = 0
FORWARD = 160

def set_angle(pin, angle):
    duty = 2 + (angle / 18)
    servo_pwms[pin].ChangeDutyCycle(duty)
    time.sleep(0.002)
    servo_pwms[pin].ChangeDutyCycle(0)

def init_servos():
    for denom, pin in DISPENSER_SERVOS.items():
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0)
        servo_pwms[pin] = pwm
        set_angle(pin, BACKWARD)
        print(f"Initialized servo for {denom} on GPIO {pin}")

def cleanup():
    for pwm in servo_pwms.values():
        pwm.stop()
    GPIO.cleanup()

def dispense_coin(denom):
    pin = DISPENSER_SERVOS.get(denom)
    if not pin:
        print("Invalid denomination selected.")
        return
    print(f"Dispensing {denom} coin...")
    # Sweep from 0 to 160 degrees
    for pos in range(0, BACKWARD):  # 0 to 160
        set_angle(pin,pos)
	# Sweep from 160 back to 0 degrees
    for pos in range(FORWARD, -1, -1):  # 160 to 0
        set_angle(pin,pos)
    print("Dispensed.\n")

# MAIN PROGRAM
try:
    init_servos()
    while True:
        choice = input("Enter coin denomination to dispense (1, 5, 10, 20 or q to quit): ").strip()
        if choice.lower() == 'q':
            break
        dispense_coin(choice)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    cleanup()
    print("All servos released. Goodbye.")

