import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sys
import time
import threading

led = 16
button = 36
reader = SimpleMFRC522()
status = 'Alive'

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def on(led):
    global status
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)
    status = 'Dead'

def off(led):
    GPIO.cleanup(led)
    
def get_rfid():
    global status
    id, text = reader.read()
    if status == 'Dead':
        off(led)
        print('Revived!')
        status = 'Alive'
    else:
        print('Player still alive!')
    time.sleep(.1)
    get_rfid()
    
def get_button():
    if not GPIO.input(button):
        print('Player is dead!')
        on(led)
    time.sleep(.1)
    get_button()
    
try:
    t1 = threading.Thread(target=get_button)
    t2 = threading.Thread(target=get_rfid)
    
    
    t1.start()
    t2.start()
            
except KeyboardInterrupt:
    GPIO.cleanup()
    print('exit')
    sys.exit(0)



