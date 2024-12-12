# Lab 6
## 实验介绍
## 实验原理
## 实验步骤
### Lab6实验报告：超声波传感器测距实验

#### 一、实验介绍
本实验旨在通过使用HC-SR04超声波传感器，学习如何在Raspberry Pi上实现非接触式距离测量。HC-SR04模块能够发射和接收超声波信号，并根据回波时间计算目标物体的距离。此实验不仅有助于理解超声波测距的工作原理，还为开发自动化控制系统提供了实际应用案例。最终目标是编写一段Python代码来读取并显示由超声波传感器测得的距离值。

#### 二、实验原理
1. **超声波传感器工作流程**：
   - 超声波传感器包括一个发射器和一个接收器。当触发引脚（Trig）接收到至少10微秒的高电平脉冲时，它会发送8个周期的40kHz超声波脉冲。
   - 接收器监听反射回来的超声波，并将Echo引脚置为高电平直到接收到回波为止。此时，Echo引脚保持高电平的时间长度与超声波往返一次所需的时间成正比。
   - 由于声音传播速度约为343米/秒（在20摄氏度空气中），因此可以通过测量Echo引脚高电平持续的时间来确定目标距离。

2. **关键参数说明**：
   - **VCC**：5V电源供电；
   - **Trig**：触发引脚，用于启动超声波发射；
   - **Echo**：回波引脚，表示是否检测到返回的超声波；
   - **GND**：接地。

3. **注意事项**：
   - 因为树莓派GPIO引脚的最大输入电压为3.3V，而Echo引脚输出的是5V逻辑电平，所以在某些情况下建议使用分压电路来保护树莓派。不过，在这个实验中，考虑到Echo引脚高电平时间非常短，可以不使用分压电路。

#### 三、实验步骤
1. **硬件连接**：
   - 根据提供的表格，确保正确连接Raspberry Pi、T型转接板和超声波传感器之间的VCC、Trig、Echo和GND引脚。
   - 将超声波传感器的Trig引脚连接到Raspberry Pi的GPIO17（BCM编号），Echo引脚连接到GPIO18（BCM编号），同时确保VCC接到5V电源，GND接地。

2. **编写代码**：
   - 使用Python语言编写程序，首先需要安装RPi.GPIO库以控制GPIO引脚。
   - 编写函数`get_distance()`，该函数负责设置Trig引脚输出10微秒的高电平脉冲，然后等待Echo引脚变为高电平，记录开始时间；接着再次等待Echo引脚变为低电平，记录结束时间。最后利用这两个时间点计算出超声波往返一次所花费的时间，并据此换算成实际距离。
   - 下面是一个简单的代码示例：

```python
import RPi.GPIO as GPIO
import time

# Define GPIO pins for the ultrasonic sensor
TRIG = 17  # BCM numbering
ECHO = 18  # BCM numbering

# Setup GPIO mode and pin directions
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Ensure TRIG is low initially
    GPIO.output(TRIG, False)
    time.sleep(0.2)

    # Send a 10us pulse to TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for ECHO to go high
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for ECHO to go low again
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the duration of the pulse
    pulse_duration = pulse_end - pulse_start

    # Convert pulse duration to distance in centimeters
    distance = pulse_duration * 17150  # Speed of sound in cm/s divided by 2 (round trip)
    distance = round(distance, 2)

    return distance

try:
    print("Measuring distance...")
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()  # Clean up GPIO settings before exiting
```

3. **测试与验证**：
   - 运行上述编写的Python脚本，观察输出结果是否合理，确认测量的距离值是否稳定且符合实际情况。
   - 可以尝试改变超声波传感器前方障碍物的位置，检查传感器是否能准确反映距离变化。

4. **清理工作**：
   - 实验结束后，请记得关闭所有运行中的进程，并断开电源以保护设备安全。