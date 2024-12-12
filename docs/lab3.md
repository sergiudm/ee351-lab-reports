### Lab3实验报告：轻触开关实验

#### 一、实验介绍
本实验旨在通过使用Raspberry Pi控制多个LED以实现流水灯效果，即LED按照一定顺序依次点亮和熄灭，形成流动的光带。这个项目不仅能够加深对GPIO引脚操作的理解，还能练习编程技能，如循环结构的应用。最终目标是编写一段Python代码来驱动8个或更多数量的LED完成流水灯效果。

#### 二、实验原理
1. **Raspberry Pi GPIO接口**：
   - Raspberry Pi提供了多个可编程的通用输入输出（General Purpose Input Output, GPIO）引脚，这些引脚可以被配置为输入或输出模式，并且可以直接与外部电路连接。
   - 在本次实验中，我们将利用BCM编号体系下的若干GPIO引脚作为输出端口来控制LED的状态（亮/灭）。

2. **LED连接方式**：
   - 每个LED都有两个引脚：阳极（较长的那个）和阴极（较短的那个）。当电流从阳极流向阴极时，LED就会发光；反之则不会亮起。
   - 对于多颗LED组成的流水灯，通常会将所有LED的阴极共同接地，而每个LED的阳极分别连接到不同的GPIO引脚上，这样就可以单独控制每个LED的工作状态了。

3. **延时函数**：
   - 在Python中，`time.sleep()`函数可以让程序暂停执行一段时间（秒），这对于创建视觉上的延迟非常有用，比如让LED保持点亮几秒钟后再熄灭。

4. **循环结构**：
   - 使用for循环或者while循环可以轻松地重复执行相同的代码块，从而实现LED按顺序逐个点亮的效果。此外，还可以结合条件语句来改变灯光流动的方向（例如左移或右移）。

#### 三、实验步骤
1. **硬件连接**：
   - 根据提供的表格，确保正确连接Raspberry Pi、T型转接板和8个LED之间的VCC、GND及信号线（SIG）。
   - 将每个LED的阳极（长腿）通过限流电阻连接到指定的GPIO引脚上（如GPIO17, GPIO27, GPIO22等），并将所有LED的阴极（短腿）连接到公共的地线上（GND）。
   - 注意选择合适的限流电阻值，以保证LED正常工作而不至于过载损坏。

2. **编写代码**：
   - 使用Python语言编写程序，首先需要安装RPi.GPIO库以控制GPIO引脚。
   - 导入必要的库后，创建一个包含所有LED对应GPIO引脚编号的列表，并定义一个函数用于设置这些引脚的状态（高电平或低电平）。
   - 编写主逻辑部分，包括初始化GPIO模式、进入无限循环使LED按照预定顺序依次点亮并伴有适当的时间间隔。
   - 下面是一个简单的代码示例：

```python
import RPi.GPIO as GPIO
import time

# Define GPIO pins for the LEDs (BCM numbering)
led_pins = [17, 27, 22, 5, 6, 13, 19, 26]  # Adjust these based on your setup

# Setup GPIO mode and pin directions
GPIO.setmode(GPIO.BCM)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

def set_leds(state):
    """Set all LEDs to the given state (True=ON, False=OFF)."""
    for pin in led_pins:
        GPIO.output(pin, state)

try:
    print("Running LED chaser...")
    
    while True:
        # Turn on each LED one by one
        for i in range(len(led_pins)):
            set_leds(False)  # Turn off all LEDs
            GPIO.output(led_pins[i], True)  # Turn on current LED
            print(f"LED {i+1} is ON")
            time.sleep(0.2)  # Wait for a short period
            
except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    set_leds(False)  # Ensure all LEDs are turned off before exiting
    GPIO.cleanup()  # Clean up GPIO settings
```

这段代码将会按照从第一个到最后一个LED的顺序，依次点亮每一个LED，每次点亮持续0.2秒，然后继续下一个，直到用户按下Ctrl+C停止程序运行。

3. **测试与验证**：
   - 执行上述编写的Python脚本，观察LED是否能按照预期的方式依次点亮。
   - 如果一切正常，尝试调整时间间隔（`time.sleep()`参数）来看看不同速度下的流水灯效果。
   - 另外，也可以修改代码逻辑，例如反转灯光流动方向，或者添加更多的动画效果（如全亮、闪烁等）。

4. **清理工作**：
   - 实验结束后，请记得关闭所有运行中的进程，并断开电源以保护设备安全。