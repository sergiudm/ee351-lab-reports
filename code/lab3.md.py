import RPi.GPIO as GPIO
import time

# Define GPIO pins for the LED (BCM numbering)
RED_PIN = 19  # Red part of the dual-color LED
GREEN_PIN = 20  # Green part of the dual-color LED
SWITCH_PIN = 21  # GPIO pin for the tactile switch

# Setup GPIO mode and pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def switch_with_delay(pin, delay=0.1):
    state = GPIO.input(pin)
    time.sleep(delay)
    return state == GPIO.input(pin)

try:
   while True:
      if switch_with_delay(SWITCH_PIN):
            GPIO.output(RED_PIN, GPIO.HIGH)
            GPIO.output(GREEN_PIN, GPIO.LOW)
      else:
            GPIO.output(RED_PIN, GPIO.LOW)
            GPIO.output(GREEN_PIN, GPIO.HIGH)
   
except KeyboardInterrupt:
   print("Exiting...")
finally:
   GPIO.cleanup()

# 3. **实验拓展**
   
#    通过开关和 LED 及相应的编程，实现以下功能：
#    1. 按一下按键，LED 红灯亮起；
#    2. 再次按一下按键，LED 红灯闪烁；
#    3. 再次按一下按键，LED 绿灯亮；
#    4. 再次按一下按键，LED 绿灯闪烁；
# 再次按下按键红灯亮起……如此循环。

#    需要注意消除好按键抖动。

import RPi.GPIO as GPIO
import time

# Define GPIO pins for the LED (BCM numbering)
RED_PIN = 19  # Red part of the dual-color LED
GREEN_PIN = 20  # Green part of the dual-color LED
SWITCH_PIN = 21  # GPIO pin for the tactile switch

# Setup GPIO mode and pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def switch_with_delay(pin, delay=0.1):
    state = GPIO.input(pin)
    time.sleep(delay)
    return state == GPIO.input(pin)

def toggle_led(pin):
    GPIO.output(pin, not GPIO.input(pin))

try:
   while True:
      if switch_with_delay(SWITCH_PIN):
            toggle_led(RED_PIN)
            time.sleep(0.5)
            toggle_led(RED_PIN)
      else:
            toggle_led(GREEN_PIN)
            time.sleep(0.5)
            toggle_led(GREEN_PIN)
   
except KeyboardInterrupt:
   print("Exiting...")
finally:
   GPIO.cleanup()
