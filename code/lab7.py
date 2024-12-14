import RPi.GPIO as GPIO
import pigpio
import time

BUZZER_PIN = 18

pi = pigpio.pi()

# 音符及其对应频率（Hz）
NOTES = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
    "G5": 784,
    "A5": 880,
    "B5": 988,
}

MELODY = [
    "C4",
    "D4",
    "E4",
    "C4",
    "E4",
    "D4",
    "C4",
    "C4",
    "D4",
    "D4",
    "E4",
    "E4",
    "C4",
    "D4",
    "E4",
]


def set_frequency(freq):
    """通过PWM设置蜂鸣器的频率"""
    pi.hardware_PWM(BUZZER_PIN, freq, 500000)


def play_music(melody):
    try:
        for note in melody:
            if note in NOTES:
                set_frequency(NOTES[note])
                time.sleep(0.5)  # 每个音符持续0.5秒
                set_frequency(0)  # 停止发声
                time.sleep(0.1)  # 间隔0.1秒

    except KeyboardInterrupt:
        print("Music stopped by user")

    finally:
        pi.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    print("Playing music...")
    play_music(MELODY)
