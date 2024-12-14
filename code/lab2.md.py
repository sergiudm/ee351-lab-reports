import RPi.GPIO as GPIO
import time

# Define GPIO pins for the LED (BCM numbering)
RED_PIN = 19  # Red part of the dual-color LED
GREEN_PIN = 20  # Green part of the dual-color LED

# Setup GPIO mode and pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

try:
    while True:
        # Turn on red LED
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        print("Red LED is ON")
        time.sleep(1)  # Wait for 1 second
        
        # Turn on green LED
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        print("Green LED is ON")
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()


   #include <wiringPi.h>
   #include <iostream>

   #define RED_PIN 19
   #define GREEN_PIN 20

   int main() {
       wiringPiSetupGpio();
       pinMode(RED_PIN, OUTPUT);
       pinMode(GREEN_PIN, OUTPUT);

       while (true) {
           digitalWrite(RED_PIN, HIGH);
           digitalWrite(GREEN_PIN, LOW);
           std::cout << "Red LED is ON" << std::endl;
           delay(1000);

           digitalWrite(RED_PIN, LOW);
           digitalWrite(GREEN_PIN, HIGH);
           std::cout << "Green LED is ON" << std::endl;
           delay(1000);
       }

       return 0;
   }
