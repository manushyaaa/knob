import serial
from pynput.keyboard import Key, Controller

keyboard = Controller()

# Define the COM port used by your Arduino
ser = serial.Serial('COM256', 9600)  # Update with the correct COM port

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

