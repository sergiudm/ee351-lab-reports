### Lab5实验报告：PCF8591模数转换器实验

#### 一、实验介绍
PCF8591 是一款单芯片，单电源，低功耗 8 位 CMOS 数据采集设备，具有
四个模拟输入，一个模拟输出和一个串行 $I^
2C$ 总线接口。三个地址引脚 $A_0，A_1
和 A_2$ 用于对硬件地址进行编程，从而允许使用多达 8 个连接到 $I
^2C$ 总线的设备，
而无需额外的硬件。通过两行双向 $I^
2C$ 总线串行传输与设备之间的地址，控制和
数据。
该设备的功能包括模拟输入多路复用，片上跟踪和保持功能，8 位模数转换
和 8 位数模转换。最大转换率由 $I^
2C$ 总线的最大速度决定。
本次实验目标为：通过控制 PCF8591，将 LED 灯点亮。


#### 二、实验原理
1. **PCF8591特性**：
   - PCF8591是一款单芯片、低功耗的CMOS数据采集设备，它包含模拟输入多路复用、片上跟踪保持功能、8位A/D转换和8位D/A转换。
   - 设备通过I2C总线接口与主控制器通信，默认地址为0x48，但可以通过设置地址引脚A0, A1, 和A2改变其硬件地址，最多允许连接8个相同类型的从设备到同一I2C总线上。

2. **I2C总线通信**：
   - I2C是一种简单的两线式串行通信标准，由SDA（数据线）和SCL（时钟线）组成。在本实验中，Raspberry Pi作为主设备，负责发送命令给PCF8591并接收来自它的响应。

3. **模拟信号采集与处理**：
   - 在这个实验里，AIN0端口被用来接收来自电位计模块的模拟信号，而AOUT端口则输出模拟电压以驱动双色LED模块，从而改变LED的亮度。
   - 当外部条件发生变化时（例如光照强度或温度变化），相应的传感器（如光电二极管或NTC热敏电阻）的阻值也会随之变化，通过测量这些元件两端的电压，我们可以得知环境的变化情况。

#### 三、实验步骤
1. **硬件连接**：
   - 根据提供的表格，确保正确连接Raspberry Pi、T型转接板和PCF8591模块之间的SDA、SCL、VCC和GND引脚。
   - 将双色LED的中间引脚（红色）连接到PCF8591的AOUT引脚，GND引脚接地；如果使用单独的绿色LED，则将其阴极连接到GND，阳极通过限流电阻连接到任意GPIO引脚（如GPIO17）。

2. **配置I2C总线**：
   - 点击Raspberry Pi桌面环境中的开始菜单，选择Preferences -> Raspberry Pi Configuration。
   - 进入Interfaces标签页，开启I2C选项，点击OK保存更改并重启系统。
  
3. **查看设备地址**：
   - 在终端中输入`sudo i2cdetect -y 0`命令，查看I2C总线上所有设备的地址。
   - 如果一切正常，应该能看到PCF8591的地址（默认为0x48）显示在对应的位置上。 

4. **编写代码**：
   - 使用Python语言编写程序，首先需要安装`smbus`库，它可以方便地操作I2C设备。
   - 导入必要的库后，创建一个SMBus实例并与PCF8591建立连接，读取AIN0上的模拟值并根据该值调整AOUT输出，进而控制LED亮度。

```python
import smbus
import time

# Define the I2C address of the PCF8591 and control bits
address = 0x48  # Default address for PCF8591
control_bit = 0x40  # Command to start conversion on channel 0 (AIN0)

# Initialize the SMBus library
bus = smbus.SMBus(1)  # Use I2C bus 1

try:
    while True:
        # Write the control byte to initiate an A/D conversion on channel 0
        bus.write_byte(address, control_bit)
        
        # Read back the converted value from the PCF8591
        analog_value = bus.read_byte(address)
        
        # Print out the raw analog value
        print("Analog Value:", analog_value)
        
        # Map the analog value to a range suitable for controlling LED brightness
        led_brightness = int((analog_value / 255.0) * 100)
        
        print("LED Brightness (%):", led_brightness)
        
        time.sleep(0.1)  # Small delay between readings

except KeyboardInterrupt:
   print("Exiting...")
```

4. **测试与验证**：
   - 执行上述编写的Python脚本，观察LED亮度是否随电位计位置的变化而相应改变。
   - 检查输出结果是否符合预期，并根据实际情况微调代码逻辑。

5. **清理工作**：
   - 实验结束后，请记得关闭所有运行中的进程，并断开电源以保护设备安全。