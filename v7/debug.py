import serial
import serial.tools.list_ports
import json
from pynput.keyboard import Key, Controller
from datetime import datetime


keyboard = Controller()

# Load configuration from a JSON file
with open("v6\config.json", "r") as config_file:
    config = json.load(config_file)

VID = config["serial_vid"]
PID = config["serial_pid"]

def get_com_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == VID and port.pid == PID:
            print("Found your device:", port.device)
            return str(port.device)
    print("Device not found.")
    return None


def volume_up():
    keyboard.press(Key.media_volume_up)
    keyboard.release(Key.media_volume_up)

def volume_down():
    keyboard.press(Key.media_volume_down)
    keyboard.release(Key.media_volume_down)

def mute():
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)




if __name__ == "__main__": 

    while True:    

        # Wait for the COM port to become available
        while not get_com_port():
            print("COM not found. Waiting...")
            time.sleep(1)

        try : 
            ser = serial.Serial(get_com_port(), 115200)
        except serial.SerialException as e:
            print("Serial communication error:", e)
     
        try:     
            while True:
                command = ser.readline().strip().decode('utf-8')
                print("Received command:", command)
                if command == "VolumeUp":
                    volume_up()
                elif command == "VolumeDown":
                    volume_down()
                elif command == "Mute":
                    mute()
                elif command == "GetTime":
                    
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    # Send the current time over serial port
                    #print("Sending time:", current_time)
                    ser.write((str(current_time)+'\n').encode())

       
        

        except serial.SerialException as e:
            print("Serial communication error:", e)
         
    ser.close()