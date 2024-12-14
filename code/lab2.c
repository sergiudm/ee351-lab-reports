#include <wiringPi.h>
#include <iostream>

#define RED_PIN 19
#define GREEN_PIN 20

int main()
{
    wiringPiSetupGpio();
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);

    while (true)
    {
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