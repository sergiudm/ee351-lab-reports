### Lab10实验报告：中断实验

#### 一、实验介绍
本实验旨在通过使用外部中断机制，学习如何在Raspberry Pi上实现对不同外接设备（如按键开关）的及时响应。外部中断允许系统暂停当前任务以优先处理紧急事件，例如硬件设备输入或定时器到期等。本次实验的任务是设置树莓派能够监听特定GPIO引脚上的状态变化，并在检测到有效边沿时触发预定义的动作，如点亮LED灯。

#### 二、实验原理
1. **树莓派中断函数**：
   - 使用`GPIO.add_event_detect()`方法来监控指定GPIO引脚的状态改变。此方法接受四个参数：
     - `channel`：需要监测的GPIO引脚编号。
     - `edge`：指定要监测的边沿类型，可以是上升沿（`GPIO.RISING`）、下降沿（`GPIO.FALLING`）或者两者皆可（`GPIO.BOTH`）。
     - `callback`：当检测到状态变化时调用的回调函数（可选）。
     - `bouncetime`：用于消除机械按键抖动的时间间隔（毫秒单位），即两次有效状态变化之间所需的最小时间差（可选）。

2. **阻塞式等待边缘触发**：
   - 另一种方式是使用`GPIO.wait_for_edge()`函数，在检测到指定边沿之前阻止程序继续执行。这种方法占用较少CPU资源，但会使主程序处于等待状态直到条件满足。

3. **按键去抖动**：
   - 由于物理按键按下时可能会产生短暂的电压波动（即“抖动”），因此在实际应用中通常会加入软件延时或者硬件滤波来确保每个按键动作只被记录一次。

#### 三、实验步骤
1. **建立电路**：
   - 根据提供的表格，确保正确连接Raspberry Pi、T型转接板和轻触按键模块之间的SIG(S)、VCC和GND引脚。
   - 将轻触按键模块的SIG(S)引脚连接到Raspberry Pi的GPIO23（BCM编号），VCC引脚接5V电源，GND引脚接地。
   - 同样地，准备一个或多个LED用于指示按键状态的变化。例如，红色LED的阳极通过限流电阻连接到GPIO17，阴极接地；绿色LED则连接到GPIO27。

2. **编写代码**：
   - 使用Python语言编写程序，首先需要安装RPi.GPIO库以控制GPIO引脚。
   - 编写函数`setup_gpio()`初始化GPIO模式和方向，以及配置按键引脚为输入并启用内部上拉电阻。
   - 定义回调函数`button_pressed_callback()`，该函数将在每次按键按下时被调用，并负责切换LED的颜色。
   - 下面是一个简单的代码示例：

```python
import RPi.GPIO as GPIO
import time

# Define GPIO pins for the LED and button (BCM numbering)
RED_LED_PIN = 17  # BCM 17, physical pin 11
GREEN_LED_PIN = 27  # BCM 27, physical pin 13
BUTTON_PIN = 23  # BCM 23, physical pin 16

def setup_gpio():
    """Setup GPIO mode and pin directions."""
    GPIO.setmode(GPIO.BCM)
    
    # Setup LEDs as output
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    
    # Setup button as input with pull-up resistor
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed_callback(channel):
    """Callback function called when the button is pressed."""
    if channel == BUTTON_PIN:
        print("Button pressed!")
        
        # Toggle between red and green LED
        if GPIO.input(RED_LED_PIN):
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(RED_LED_PIN, GPIO.HIGH)
            GPIO.output(GREEN_LED_PIN, GPIO.LOW)

try:
    setup_gpio()
    
    # Add event detection on the button pin with debouncing
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)
    
    print("Waiting for button press...")
    while True:
        time.sleep(1)  # Keep script running to allow callbacks to work

except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    GPIO.cleanup()  # Clean up GPIO settings before exiting
```

3. **测试与验证**：
   - 执行上述编写的Python脚本，尝试按下轻触按键，观察LED是否能够在红绿之间交替亮起。
   - 检查输出结果是否符合预期，并根据实际情况微调代码逻辑，比如调整按键去抖时间（`bouncetime`参数）。

4. **功能扩展**：
   - 在基础版本的基础上，可以进一步开发更复杂的交互逻辑，例如实现多模式切换（按一下红灯亮，再按一下红灯闪烁，接着绿灯亮，再次按一下绿灯闪烁...如此循环）。
   - 注意保存最终版本的代码及视频记录，以便提交作业。

5. **清理工作**：
   - 实验结束后，请记得关闭所有运行中的进程，并断开电源以保护设备安全。