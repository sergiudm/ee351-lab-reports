import smbus
import time

address = 0x48  # 地址
control_bit = 0x40  # 控制字

bus = smbus.SMBus(1)

try:
    while True:
        # 向PCF8591写入控制字节
        bus.write_byte(address, control_bit)

        analog_value = bus.read_byte(address)

        print("Analog Value:", analog_value)

        # 把模拟值映射到LED亮度范围
        led_brightness = int((analog_value / 255.0) * 100)

        print("LED Brightness (%):", led_brightness)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
