import paho.mqtt.client as mqtt
import time
from tkinter import *
from tkinter import ttk

broker ="192.168.2.123" # Laptop IP
msg = "Nothing Connected Yet!"

def updateMsg():
    global msg
    label3.config(text=msg)

def on_log(client, userdata, level, buf):
    print("Log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("konek!")
    else:
        print("gagal konek!")
        
def on_message(client, userdata, message):
    global msg
    msg = str(message.payload.decode("utf-8"))
    updateMsg()
    print(msg)
    
client = mqtt.Client("PythonIdle")
client.on_connect=on_connect
client.on_message=on_message #attach function to callback
#client.on_log=on_log
print("Connecting to broker ", broker)
client.connect(broker)
client.loop_start()
client.subscribe("BangSultanSmartVestSystemForTA")
#client.publish("test","Ini dari file Python yak")

root = Tk()
label = Label(root, text="BangSultan's Smart Vest System",
              font=(None, 25), width=35, height=2)
label.pack()
separator = ttk.Separator(root, orient='horizontal')
separator.pack(side='top', fill='x')
label2 = Label(root, text="Player Status:",font=(None, 15), width=50, height=2)
label2.pack()
label3 = Label(root, text=msg,font=(None, 15), width=50)
label3.pack()
label4 = Label(root, text="",font=(None, 15), width=50, height=2)
label4.pack()
root.mainloop()

#time.sleep(4)
#client.loop_stop()
#client.disconnect()
#print("Done!")
