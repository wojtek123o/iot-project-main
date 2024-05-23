#!/usr/bin/env python3

from config import *
import RPi.GPIO as GPIO
import time
import board
import neopixel

def buzzer(state):
    GPIO.output(buzzerPin, not state)     

def access_granted():
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)
    pixels.fill((0, 255, 0))
    pixels.show()
    
    buzzer(True)
    time.sleep(1)
    buzzer(False)
    time.sleep(1)

    pixels.fill((0, 0, 0))
    pixels.show()
    

def access_denied():
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)
    pixels.fill((255, 0, 0))
    pixels.show()
    
    for _ in range(3): 
            buzzer(True) 
            time.sleep(0.25)  
            buzzer(False) 
            time.sleep(0.25) 

    time.sleep(0.5);

    pixels.fill((0, 0, 0))
    pixels.show()

     
if __name__ == "__main__":
    access_granted()
    time.sleep(2)
    access_denied()
    GPIO.cleanup()  # pylint: disable=no-member
