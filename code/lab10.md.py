import RPi.GPIO as GPIO
import time

# Define GPIO pins for the button and LED
BUTTON_PIN = 23  # BCM numbering
LED_PIN = 18  # BCM numbering

# Define GPIO pins for the ultrasonic sensor
TRIG = 17  # BCM numbering
ECHO = 18  # BCM numbering

# Setup GPIO mode and pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to toggle LED state
def button_callback(channel):
    if GPIO.input(LED_PIN):
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)

# Function to measure distance with ultrasonic sensor
def ultrasonic_callback(channel):
    # Send a 10us pulse to TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for ECHO to go high
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for ECHO to go low again
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate duration of the pulse
    pulse_duration = pulse_end - pulse_start

    # Calculate distance in cm
    distance = pulse_duration * 34300 / 2
    print(f"Distance: {distance:.2f} cm")

# Add event detection for the button
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    print("Press the button to toggle the LED state.")
    print("Press the button to measure distance with the ultrasonic sensor.")
    while True:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        ultrasonic_callback(BUTTON_PIN)

except KeyboardInterrupt:
    print("\nCleaning up...")
    GPIO.cleanup()
