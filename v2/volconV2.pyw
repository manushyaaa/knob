import serial
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

# Function to check if a COM port is available
def is_com_port_available(port):
    try:
        ser = serial.Serial(port, 9600)
        ser.close()
        return True
    except serial.SerialException:
        return False
                        
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

    except serial.SerialException as e:
        #print(f"An error occurred while opening the COM port: {e}")
        pass
