### Lab5实验报告：模拟温度传感器实验

#### 一、实验介绍
本实验旨在使用NTC（负温度系数）热敏电阻构建的温度感测模块，通过Raspberry Pi获取当前环境的温度值。该温度传感器能够将温度变化转化为电阻变化，并借助模数转换器PCF8591将这些模拟信号转换为数字信号供Raspberry Pi处理。最终目标是学习如何读取和解析来自温度传感器的数据，以实现对室内/环境温度的有效监测。

#### 二、实验原理
1. **NTC热敏电阻特性**：
   - NTC热敏电阻是一种随温度升高而电阻减小的元件，其阻值与温度之间存在特定关系，这使得它非常适合用来测量温度。
   - 在本实验中，我们将使用Steinhart-Hart方程来计算热敏电阻的精确温度，这是一个用于描述热敏电阻电阻-温度特性的经验公式。

2. **电路设计**：
   - 温度传感器模块由一个NTC热敏电阻和一个固定电阻（例如10kΩ）组成分压电路。当环境温度发生变化时，热敏电阻的阻值也会随之改变，从而影响分压点处的电压输出。
   - 通过连接到PCF8591的模拟输入端口AIN0，我们可以采集这个电压信号，并将其转换为数字形式以便后续分析。

3. **数据处理**：
   - 首先从PCF8591读取经过A/D转换后的数值，然后根据已知条件（如供电电压5V，ADC分辨率为8位即0~255对应0~5V）计算出对应的模拟电压。
   - 接着利用分压比公式计算得到热敏电阻的实际阻值，再代入Steinhart-Hart方程求解温度T。

4. **Steinhart-Hart方程**：
   - Steinhart-Hart方程表达式为 \( \frac{1}{T} = A + B\ln(R) + C(\ln(R))^3 \)，其中\( T \)是以开尔文为单位的绝对温度，\( R \)是热敏电阻在给定温度下的电阻值，而\( A \), \( B \), \( C \)则是取决于具体型号的常数参数。对于本次实验，假设\( R_0 \)为10kΩ，B值为3950K。

#### 三、实验步骤
1. **硬件连接**：
   - 根据提供的表格，确保正确连接Raspberry Pi、T型转接板和PCF8591模块之间的SDA、SCL、VCC和GND引脚。
   - 将模拟温度传感器的AO引脚连接到PCF8591模块的AIN0，DO引脚可以留空或接地，VCC引脚接5V电源，GND引脚接地。

2. **配置I2C总线**：
   - 点击Raspberry Pi桌面环境中的开始菜单，选择Preferences -> Raspberry Pi Configuration。
   - 进入Interfaces标签页，开启I2C选项，点击OK保存更改并重启系统。

3. **编写代码**：
   - 使用Python语言编写程序，首先需要安装`smbus`库，它可以方便地操作I2C设备。
   - 导入必要的库后，创建一个SMBus实例并与PCF8591建立连接，读取AIN0上的模拟值并根据该值计算温度。
   - 下面是一个简单的代码示例：

```python
import smbus
import math
import time

# Define the I2C address of the PCF8591 and control bits
address = 0x48  # Default address for PCF8591
control_bit = 0x40  # Command to start conversion on channel 0 (AIN0)

# Constants for the thermistor calculation
R0 = 10000  # Resistance at 25°C in ohms
B = 3950  # Thermistor constant in Kelvin
T0 = 298.15  # Standard temperature in Kelvin (25°C)
Vcc = 5.0  # Supply voltage in volts

# Initialize the SMBus library
bus = smbus.SMBus(1)  # Use I2C bus 1

def read_temperature():
    try:
        # Write the control byte to initiate an A/D conversion on channel 0
        bus.write_byte(address, control_bit)
        
        # Read back the converted value from the PCF8591
        analog_value = bus.read_byte(address)
        
        # Calculate the analog voltage
        Vr = (analog_value / 255.0) * Vcc
        
        # Calculate the resistance of the thermistor
        Rt = R0 * Vr / (Vcc - Vr)
        
        # Apply the Steinhart-Hart equation to calculate temperature
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
        
        time.sleep(1)  # Small delay between readings

except KeyboardInterrupt:
    pass  # Allow the program to exit cleanly with Ctrl+C
```

4. **测试与验证**：
   - 执行上述编写的Python脚本，观察输出结果是否合理，确认温度读数是否稳定且符合实际环境温度。
   - 如果可能的话，尝试改变周围环境温度（比如靠近热源或冷源），检查传感器是否能准确反映温度变化。

5. **清理工作**：
   - 实验结束后，请记得关闭所有运行中的进程，并断开电源以保护设备安全。