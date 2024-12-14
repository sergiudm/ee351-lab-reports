import RPi.GPIO as GPIO
import time

RED_PIN = 19  # 红色LED
GREEN_PIN = 20  # 绿色LED

# 设置GPIO模式
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

try:
    while True:
        # 打开红色LED
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        print("红色LED已打开")
        time.sleep(1)  # 等待1秒钟

        # 打开绿色LED
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        print("绿色LED已打开")
        time.sleep(1)  # 等待1秒

except KeyboardInterrupt:
    print("程序被终止")

finally:
    # 退出前清理GPIO设置
    GPIO.cleanup()
