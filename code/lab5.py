import smbus
import math
import time

address = 0x48  # 地址
control_bit = 0x40  # 控制字

# 常数
R0 = 10000
B = 3950
T0 = 298.15  # 25°C -> 开氏温度
Vcc = 5.0  # 5V供电

bus = smbus.SMBus(1)


def read_temperature():
    try:
        # 设置PCF8591地址和控制位
        bus.write_byte(address, control_bit)

        analog_value = bus.read_byte(address)

        Vr = (analog_value / 255.0) * Vcc

        # 计算热敏电阻的阻值
        Rt = R0 * Vr / (Vcc - Vr)

        # 计算温度
        temp_kelvin = 1 / (math.log(Rt / R0) / B + 1 / T0)
        temp_celsius = temp_kelvin - 273.15

        return round(temp_celsius, 2)

    except Exception as e:
        print("Error reading temperature:", str(e))
        return None


try:
    while True:
        temperature = read_temperature()
        if temperature is not None:
            print(f"Temperature: {temperature}°C")
        else:
            print("Failed to read temperature.")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting program.")
