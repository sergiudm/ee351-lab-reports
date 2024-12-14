import RPi.GPIO as GPIO
import time

BUTTON_PIN = 23
LED_PIN = 18
TRIG = 17
ECHO = 27  # 确保 ECHO 引脚正确

# 设置 GPIO 模式
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 全局变量，用于控制超声波测量
measuring = False
pulse_start = 0
pulse_end = 0


def button_pressed_callback(channel):
    """按键按下回调函数：点亮 LED 并启动测距"""
    global measuring
    GPIO.output(LED_PIN, GPIO.HIGH)
    measuring = True  # 设置为 True 以允许测距
    GPIO.output(TRIG, False)  # 先拉低，再拉高，使得输出一个干净的脉冲
    time.sleep(0.01)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10us 脉冲
    GPIO.output(TRIG, False)


def button_released_callback(channel):
    """按键松开回调函数：熄灭 LED"""
    global measuring
    GPIO.output(LED_PIN, GPIO.LOW)
    measuring = False  # 设置为 False 以停止测距


def echo_callback(channel):
    """ECHO 引脚状态变化回调函数：计算距离"""
    global measuring, pulse_start, pulse_end
    if measuring:  # 只有在测量状态下才进行计算
        if GPIO.input(ECHO) == GPIO.HIGH:
            pulse_start = time.time()
        elif GPIO.input(ECHO) == GPIO.LOW:
            pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 34300 / 2
            print(f"Distance: {distance:.2f} cm")


# 添加按键按下和松开事件检测
GPIO.add_event_detect(
    BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200
)  # 按下
GPIO.add_event_detect(
    BUTTON_PIN, GPIO.RISING, callback=button_released_callback, bouncetime=200
)  # 松开

# 添加 ECHO 引脚状态变化检测
GPIO.add_event_detect(ECHO, GPIO.BOTH, callback=echo_callback)

try:
    print("Press the button...")
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCleaning up...")
    GPIO.cleanup()
