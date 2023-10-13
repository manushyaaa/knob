![Knob Controller](https://github.com/manushyaaa/knob/blob/main/knob_banner.png)

## Overview

**Knob** is a versatile rotary encoder-based input device designed for controlling various functions in different contexts. This Arduino-based project utilizes a rotary encoder and push button switches to trigger actions that integrate with various devices and services, including controlling media playback, adjusting system brightness, managing lighting, and more. The system is comprised of both an Arduino-based device and a Python script to control it. The project also includes enhanced rotation sensitivity, different actions, and a time display feature.

### Features:
- Control system volume and media playback.
- Adjust screen brightness.
- Control smart lighting through WLED.
- Interact with Spotify for music playback control.
- Communicate with an Arduino-based device to trigger actions.
- Display the current time on the device.
- Precise rotary encoder for enhanced rotation control.
- OLED screen for displaying current mode and information.

## Components

- Arduino board
- Rotary encoder with push button
- OLED screen (Adafruit SSD1306) (128x32 pixels)
- Push button switches

## Pin Configuration

- CLK (Rotary Encoder): Pin 5
- DATA (Rotary Encoder): Pin 6
- Encoder Switch: Pin 7
- Mode Switch Button: Pin 2
- Left Button: Pin 3
- Right Button: Pin 4
- 
![Knob Circuit](https://github.com/manushyaaa/knob/blob/main/knob_circuit.png)

## Requirements

To use this system, you'll need the following:
```bash
- Python 3.6+
- Arduino board with compatible firmware
- Required Python libraries (install using pip):
  1. requests
  2. serial
  3. spotipy
  4. pynput
  5. screen_brightness_control
```

## Installation

1. Clone the repository:
   
   ```bash   
   git clone https://github.com/manushyaaa/knob.git

   cd knob/v10

   pip install -r requirements.txt or
   python -m pip install -r requirements.txt
   
   ```
2. Make sure to get your Arduino's VID and PID: after plugging in your Arduino board you can use the following script to get the VID and PID of your board.
   ```bash
   python get_device_info.py
   ```
3. Before running the script, you need to configure it by editing the config dictionary in the Python script. Here's what each configuration parameter means:

- `wled_brightness`: Initial WLED brightness.
- `serial_vid`: Vendor ID for your Arduino device.
- `serial_pid`: Product ID for your Arduino device.
- `spotify_client_id`: Your Spotify application client ID.
- `spotify_client_secret`: Your Spotify application client secret.
- `wled_url`: IP address or URL for the WLED controller.

4. Set up your Arduino environment. Install the following dependencies  
  `Adafruit_GFX library`
  `Adafruit_SSD1306 library`

5. Connect the components as per the provided pin configuration.

6. Upload the provided code to your Arduino board.

7. Power on the setup and start using the Knob Controller.

## Usage

1. Connect your device to the computer via a USB serial connection.

2. Run the script:

   ```bash
   python knob_v1dot9.py
   ```

3. The script will continuously listen for commands from your device.

4. You can send commands from the Arduino or modify the `command_mapping` dictionary in the Python script to customize actions.

    ```bash
    Switching Modes
    
    - Press the main button to cycle through different modes. The mode is displayed on the OLED screen.
    
    Rotary Encoder
    
    - Rotate the encoder to perform mode-specific actions. The direction of rotation determines the action.
    
    Button Actions
    
    - Left Button: Execute mode-specific actions when pressed.
    - Right Button: Execute mode-specific actions when pressed.
    
    Encoder Switch
    
    - Press the encoder switch to trigger a mode-specific action.
    
    Time Display
    
    - When in a mode (not 0), the program will periodically query and display time information when connected to a serial device.
    ```
## Modes and Actions

>### Mode 1: Volume Control  
  >- Rotate clockwise: Increase system volume.
  >- Rotate counterclockwise: Decrease system volume.
  >- Encoder switch: Mute system audio.

>### Mode 2: Brightness Control
  >- Rotate clockwise: Increase screen brightness.
  >- Rotate counterclockwise: Decrease screen brightness.
  >- Encoder switch: Lock or unlock the screen.

>### Mode 3: Spotify Control
  >- Rotate clockwise: Navigate to the next track.
  >- Rotate counterclockwise: Navigate to the previous track.
  >- Encoder switch: Play/Pause the current track.

>### Mode 4: WLED Control (ESP2866 Module)
  >- Rotate clockwise: Change WLED mode.
  >- Rotate counterclockwise: Change WLED color.
  >- Encoder switch: Power on/off WLED.

>### OLED Screen
  >- The OLED screen displays the current mode.
  >- It also displays the current time.

## Additional Information 
  >- How to Setup Spotify Web API  : https://developer.spotify.com/documentation/web-api
  >- Installing WS2812FX library (WLED) for your WS2812 LED Strip : https://kno.wled.ge


## Acknowledgments

https://gitlab.com/makeitforless/spotify_controller

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please create a pull request. Please feel free to reach out if you have any questions or encounter issues while using this script.
