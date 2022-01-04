# PicoLAN
This is a LAN system library using UART on Raspberry Pi Pico.

## Description
You can build a LAN system by converting the UART of Raspberry Pi Pico to RS485 and connecting them in parallel.

## Demo
This is a program that reads received data.   
format: `STX` `ADDRESS(00~10)` `DATA_LEN` `DATA(10Byte)` `ETX`
```python:demo.py
from machine import UART, Pin
import PicoLAN

def print_func(arg):
    print(arg)

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
plan = PicoLAN.PicoLAN(uart, 10, print_func, 10, 10, PicoLAN.DATA_LEN_FIXED)

while True:
    plan.read()
```
