import serial
import time
from pynput.keyboard import Key, Controller
import screen_brightness_control as sbc
import os
import requests 
from win10toast import ToastNotifier

brightness = sbc.get_brightness()

keyboard = Controller()
BRIG_VAL = 50  # Initialize BRIG_VAL as a global variable
WLED_CNTR = 150 
# Function to check if a COM port is available
def is_com_port_available(port):
    try:
        ser = serial.Serial(port, 9600)
        ser.close()
        return True
    except serial.SerialException:
        return False

def main():
    global BRIG_VAL  # Declare BRIG_VAL as a global variable
    global WLED_CNTR
    while True:
       
        # Wait for COM256 to become available
        while not is_com_port_available('COM256'):
            #print("COM256 not available, waiting...")
            time.sleep(1)  # Wait for 1 second before checking again

        #print("COM256 is available, starting the program.")

        try:
            ser = serial.Serial('COM256', 9600)  # Open the COM port

            while True:
                command = ser.readline().strip().decode('utf-8')
                #print(command)
                if command == "VolumeUp":
                    # Simulate a volume up key press
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)

                elif command == "VolumeDown":
                    # Simulate a volume down key press
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)

                elif command == "PlayPause":
                    # Simulate a play/pause key press
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)

                elif command == "Mute":
                    # Simulate a play/pause key press
                    keyboard.press(Key.media_volume_mute)
                    keyboard.release(Key.media_volume_mute)

                elif command == "BrightnessUp":
                    BRIG_VAL += 10
                    sbc.set_brightness(BRIG_VAL)

                elif command == "BrightnessDown":
                    BRIG_VAL -= 10
                    sbc.set_brightness(BRIG_VAL)

                elif command == "SEEKUp":
                    WLED_CNTR += 10  

                    if WLED_CNTR < 0 :
                        WLED_CNTR = 0 

                    if WLED_CNTR > 254 :
                        WLED_CNTR = 254 
                    #print(WLED_CNTR)
                    requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")


                    # keyboard.press(Key.right)
                    # keyboard.release(Key.right)

                elif command == "SEEKDown":
                    WLED_CNTR -= 10  
                    #print(WLED_CNTR)
                    if WLED_CNTR < 0 :
                        WLED_CNTR = 0 
                        
                    if WLED_CNTR > 254 :
                        WLED_CNTR = 254 
                    
                    requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
                    # keyboard.press(Key.left)
                    # keyboard.release(Key.left)

                elif command == "Lock":
                    os.system('rundll32.exe user32.dll,LockWorkStation')

        except serial.SerialException as e:
            # print(f"An error occurred while opening the COM port: {e}")
            pass

if __name__ == "__main__":
    # call your code here
    main()


# import requests

# url = "http://192.128.1.69/win&A=255"

# try:
#     response = requests.get(url)
#     if response.status_code == 200:
#         print("Request successful")
#     else:
#         print(f"Request failed with status code: {response.status_code}")
# except requests.exceptions.RequestException as e:
#     print(f"Request error: {e}")
