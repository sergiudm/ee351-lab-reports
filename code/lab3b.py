import RPi.GPIO as GPIO
import time

RED_PIN = 19
GREEN_PIN = 20
SWITCH_PIN = 21  # 开关引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def switch_with_delay(pin, delay=0.1):
    """检测开关状态"""
    state = GPIO.input(pin)
    time.sleep(delay)
    return state == GPIO.input(pin)


def toggle_led(pin):
    """切换LED状态"""
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
