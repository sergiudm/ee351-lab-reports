import smbus
import RPi.GPIO as GPIO
import time

# I2C 地址
PCF8591_ADDRESS = 0x48

# GPIO 引脚
RED_LED_PIN = 27
GREEN_LED_PIN = 22
BUTTON_PIN = 17

# 初始化
bus = smbus.SMBus(1)  # 使用 I2C 总线 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def read_adc(channel):
    bus.write_byte(PCF8591_ADDRESS, 0x40 | channel)  # 选择通道
    bus.read_byte(PCF8591_ADDRESS)  # 丢弃第一次读取
    return bus.read_byte(PCF8591_ADDRESS)


try:
    while True:
        x_value = read_adc(0)  # 读取 X 轴
        y_value = read_adc(1)  # 读取 Y 轴

        # 将 ADC 值 (0-255) 映射到 PWM 值 (0-100)
        red_brightness = int(x_value / 255 * 100)
        green_brightness = int(y_value / 255 * 100)

        # 使用 PWM 控制 LED 亮度（你需要设置 GPIO 为 PWM 输出）
        red_pwm = GPIO.PWM(RED_LED_PIN, 100)  # 100Hz 频率
        green_pwm = GPIO.PWM(GREEN_LED_PIN, 100)
        red_pwm.start(red_brightness)
        green_pwm.start(green_brightness)

        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # 按键按下
            red_pwm.stop()
            green_pwm.stop()
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            GPIO.output(GREEN_LED_PIN, GPIO.LOW)
            time.sleep(0.5)  # 延时防止抖动
        else:
            red_pwm.ChangeDutyCycle(red_brightness)
            green_pwm.ChangeDutyCycle(green_brightness)

except KeyboardInterrupt:
    red_pwm.stop()
    green_pwm.stop()
    GPIO.cleanup()
