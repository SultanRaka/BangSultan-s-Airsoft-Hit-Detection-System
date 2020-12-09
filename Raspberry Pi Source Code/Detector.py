import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sys
import time
import threading


led = 16
button = 36
buzzer = 37
reader = SimpleMFRC522()
status = 'Alive'

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)




def on(led):
    global status
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)
    GPIO.output(buzzer, GPIO.HIGH)
    status = 'Dead'

def off(led):
    GPIO.output(buzzer, GPIO.LOW)
    GPIO.cleanup(led)
    
def get_rfid():
    global status
    id, text = reader.read()
    if status == 'Dead':
        off(led)
        print('Revived!')
        status = 'Alive'
        client.publish("BangSultanSmartVestSystemForTA","Revived!")
        time.sleep(3)
        client.publish("BangSultanSmartVestSystemForTA","Alive")
    else:
        print('Player still alive!')
        client.publish("BangSultanSmartVestSystemForTA","Player still alive!")
        time.sleep(3)
        client.publish("BangSultanSmartVestSystemForTA","Alive")
    time.sleep(.1)
    get_rfid()
    
def get_button():
    if not GPIO.input(button):
        print('Player is dead!')
        on(led)
        client.publish("BangSultanSmartVestSystemForTA","Dead")
    time.sleep(.1)
    get_button()
    
try:
    broker_address="192.168.2.69"
    client = mqtt.Client("P1")
    print('connecting')
    client.connect(broker_address)
    client.publish("BangSultanSmartVestSystemForTA","Alive")
    print('connected!')
    t1 = threading.Thread(target=get_button)
    t2 = threading.Thread(target=get_rfid)
    
    
    t1.start()
    t2.start()
            
except KeyboardInterrupt:
    GPIO.cleanup()
    print('exit')
    sys.exit(0)



