---
comments: true
---
### Lab2实验报告：学习知识准备与双色LED实验

#### 一、实验介绍
本实验旨在了解Raspberry Pi的IO接口及其引脚编号方式，并通过实际操作掌握使用wiringPi库和RPi.GPIO库控制硬件的方法，最终目标是实现一个简单的双色LED红绿交替闪烁效果。

#### 二、实验原理
1. **Raspberry Pi IO口**：
   - Raspberry Pi拥有40个GPIO管脚，这些管脚可以通过不同的编号系统来引用，包括物理位置编号、wiringPi指定的编号以及BCM2837 SOC指定的编号。
   - 在本次实验（以及后续实验）中，我们使用BCM编码来连接和编程。

2. **wiringPi库**：
   - wiringPi是一个用于C/C++语言的GPIO控制库，它简化了对Raspberry Pi GPIO的操作。安装此库后，可以方便地在命令行或程序中控制GPIO引脚。

3. **RPi.GPIO库**：
   - RPi.GPIO是一个Python库，允许用户直接从Python代码中控制Raspberry Pi的GPIO。它是Raspbian操作系统的一部分，默认已安装，因此可以直接调用其API进行编程。

4. **Mu编辑器与Geany IDE**：
   - Mu是一款适合初学者使用的Python编辑器，提供了基本的IDE功能如语法检查、运行和调试等。
   - Geany则是一款轻量级的跨平台IDE，支持多种编程语言，对于C/C++项目来说非常适合。
  
!!! tip

      后续经验表明，这两款IDE在树莓派下渲染效果不佳，推荐使用VSCode远程开发插件。

5. **双色LED模块**：
   - 双色LED通常指的是包含两个独立发光单元（红色和绿色）在一个封装内的LED。通过改变输入电压或电流的方向，可以使不同的颜色发光或者两者同时亮起形成黄色。

#### 三、实验步骤
1. **硬件连线**：
   - 将双色LED的S引脚（绿色）、中间引脚（红色）分别连接到Raspberry Pi的GPIO接口上，GND引脚连接到Raspberry Pi的地线。记住使用的GPIO引脚编号（本次实验使用的是BCM编号下的GPIO19, GPIO20, GND）。
   
2. **编写并上传代码**：
   - 使用Mu编辑器创建一个新的Python脚本文件，编写一段代码来控制双色LED的红绿交替闪烁。代码应该设置好相应的GPIO模式（输入/输出），然后按照设定的时间间隔切换LED的状态。
   - 如果使用C/C++，则可以在Geany中新建一个源文件，同样需要配置GPIO模式，并且要记得在编译时链接wiringPi库。

3. **运行测试**：
   - 执行编写的Python脚本或编译后的C/C++程序，观察双色LED是否能够按照预期的顺序红绿交替闪烁。
   - 除了代码逻辑，**一定要检查硬件连接是否正确无误**！！！（比如是否插紧T型板、是否接错了引脚等）

4. **清理工作**：
   - 实验结束后，记得关闭所有运行中的进程，否则LED灯可能会一直亮着。

---

#### 四、编写代码
程序框图：
   
``` mermaid
flowchart TD
      A[开始] --> B[设置GPIO模式]
      B --> C[循环]
      C --> D[点亮红灯]
      D --> E[等待1秒]
      E --> F[点亮绿灯]
      F --> G[等待1秒]
      G --> C
```
Python代码，用于实现双色LED的红绿交替闪烁：

```python
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
```

这段代码将使双色LED按照红-绿-红-绿的顺序交替闪烁，每次持续1秒钟。

C++代码
   ```cpp
   #include <wiringPi.h>
   #include <iostream>

   #define RED_PIN 19
   #define GREEN_PIN 20

   int main() {
       wiringPiSetupGpio();
       pinMode(RED_PIN, OUTPUT);
       pinMode(GREEN_PIN, OUTPUT);

       while (true) {
           digitalWrite(RED_PIN, HIGH);
           digitalWrite(GREEN_PIN, LOW);
           std::cout << "Red LED is ON" << std::endl;
           delay(1000);

           digitalWrite(RED_PIN, LOW);
           digitalWrite(GREEN_PIN, HIGH);
           std::cout << "Green LED is ON" << std::endl;
           delay(1000);
       }

       return 0;
   }
   ```