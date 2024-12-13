import smbus
import time

# Define the I2C address of the PCF8591 and control bits
address = 0x48  # Default address for PCF8591
control_bit = 0x40  # Command to start conversion on channel 0 (AIN0)

bus = smbus.SMBus(1)

try:
    while True:
        # Write the control byte to initiate an A/D conversion on channel 0
        bus.write_byte(address, control_bit)
        
        analog_value = bus.read_byte(address)
        
        print("Analog Value:", analog_value)
        
        # Map the analog value to a range suitable for controlling LED brightness
        led_brightness = int((analog_value / 255.0) * 100)
        
        print("LED Brightness (%):", led_brightness)
        
        time.sleep(0.1)

except KeyboardInterrupt:
   print("Exiting...")
