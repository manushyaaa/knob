from pynput import keyboard

def get_pressed_key():
    def on_key_press(key):
        try:
            # Check if the pressed key is alphanumeric or a special key
            if key.char:
                print(f'Key pressed: {key.char}')
        except AttributeError:
            # The key pressed is a special key (e.g., Shift, Ctrl, F1, etc.)
            print(f'Special key pressed: {key}')

    # Create a listener that calls on_key_press when a key is pressed
    listener = keyboard.Listener(on_press=on_key_press)

    # Start the listener
    listener.start()

    # Keep the listener running until you manually stop it
    listener.join()

# Usage example:
if __name__ == "__main__":
    get_pressed_key()
