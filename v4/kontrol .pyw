import serial
import time
from pynput.keyboard import Key, Controller
import screen_brightness_control as sbc
import os
import requests
from win10toast import ToastNotifier  # Import ToastNotifier


try:
    brightness = sbc.get_brightness()
except Exception as e:
    print("Error getting brightness:", e)
    brightness = None

keyboard = Controller()

BRIG_VAL = 50
WLED_CNTR = 150
 

# Function to check if a COM port is available
def is_com_port_available(port):
    try:
        ser = serial.Serial(port, 115200)
        ser.close()
        return True
    except serial.SerialException as e:
        print( "is_com_port_available" , e)
        return False

def main():
    global BRIG_VAL
    global WLED_CNTR
    while True:
        # Wait for COM256 to become available
        while not is_com_port_available('COM256'):
            print( "COM not found -> Line 31"  )
            time.sleep(1)  # Wait for 1 second before checking again

        try:
            ser = serial.Serial('COM256', 115200)

            while True:
                command = ser.readline().strip().decode('utf-8')
                if command == "VolumeUp":
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)

                elif command == "VolumeDown":
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)

                elif command == "PlayPause":
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)

                elif command == "Mute":
                    keyboard.press(Key.media_volume_mute)
                    keyboard.release(Key.media_volume_mute)

                elif command == "BrightnessUp":
                    BRIG_VAL += 10
                    try : 
                        sbc.set_brightness(BRIG_VAL)
                    except Exception as e : 
                        pass
                    

                elif command == "BrightnessDown":
                    BRIG_VAL -= 10 
                    try : 
                        sbc.set_brightness(BRIG_VAL)
                    except Exception as e : 
                        pass
                    
                  

                elif command == "SEEKUp":
                    WLED_CNTR += 10
                    if WLED_CNTR < 0:
                        WLED_CNTR = 0
                    if WLED_CNTR > 254:
                        WLED_CNTR = 254
                    requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
                     
                elif command == "SEEKDown":
                    WLED_CNTR -= 10
                    if WLED_CNTR < 0:
                        WLED_CNTR = 0
                    if WLED_CNTR > 254:
                        WLED_CNTR = 254
                    requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
                    

                elif command == "Lock":
                    
                    os.system('rundll32.exe user32.dll,LockWorkStation')
                     

        except serial.SerialException as e:
            print("main loop Exception", e)
            pass

if __name__ == "__main__":
    main()
