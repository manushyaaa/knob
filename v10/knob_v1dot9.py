"""
VERSION 1.9 
 
"""
import os
import requests
import serial.tools.list_ports
import screen_brightness_control as sbc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pynput.keyboard import Key, Controller
import json
import time
import threading
from datetime import datetime

config =  {
  "brightness": 50,
  "wled_brightness": 150,
  "spotify_volume": 30, # Initial volume
  "serial_vid": 6790, # REPLACE WITH YOUR DEVICE'S VENDOR ID
  "serial_pid": 29987, # REPLACE WITH YOUR DEVICE'S PRODUCT ID
  "spotify_client_id": "YOUR_SPOTIFY_CLIENT_ID",
  "spotify_client_secret": "YOUR_SPOTIFY_CLIENT_SECRET",
  "wled_url": "YOUR_WLED_IP"
}

color_counter = -1 
wled_ip = config["wled_url"]
WLED_PRESET = 1
BRIG_VAL = config["brightness"]
WLED_CNTR = config["wled_brightness"]
SPOTIFY_VOLUME = config["spotify_volume"]
VID = config["serial_vid"]
PID = config["serial_pid"]
colors = [
    [255, 200, 147],# whitegolden
    [255, 160, 0],  # goldenyellow
    [255, 238, 229],# whiteNatural
    [246, 66, 255], # purple
    [255, 0, 0],    # Red
    [0, 255, 0],    # Green
    [0, 0, 255],    # Blue
]

client_id = config["spotify_client_id"]
client_secret = config["spotify_client_secret"]

keyboard = Controller()

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='http://localhost:8888/callback',
    scope='user-modify-playback-state user-read-playback-state'
))

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

def show_media():
    with keyboard.pressed(Key.cmd):
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        keyboard.release(Key.ctrl)
    keyboard.release(Key.cmd)

def media_change():                                                                                                                                                                                                                                                                                                                                                                                                                               
    os.system("MMSYS.CPL")

def brightness_up():
    global BRIG_VAL
    BRIG_VAL += 5
    try:
        sbc.set_brightness(BRIG_VAL)
    except Exception as e:
        print("Error setting brightness:", e)

def brightness_down():
    global BRIG_VAL
    BRIG_VAL -= 5
    try:
        sbc.set_brightness(BRIG_VAL)
    except Exception as e:
        print("Error setting brightness:", e)

def lock():
    os.system('rundll32.exe user32.dll,LockWorkStation')

def shutdown():
    os.system("shutdown /s /t 0")

def open_tskmgr():
    os.system("taskmgr")
 

def music_seek_up():
    global SPOTIFY_VOLUME
    global MAIN_COUNTER

    SPOTIFY_VOLUME += 5
    if SPOTIFY_VOLUME < 0:
        SPOTIFY_VOLUME = 0
    if SPOTIFY_VOLUME > 100:
        SPOTIFY_VOLUME = 100
    try:
        sp.volume(SPOTIFY_VOLUME)
        MAIN_COUNTER = SPOTIFY_VOLUME
    except Exception as e:
        print("Spotify API error:", e)

def music_seek_down():
    global SPOTIFY_VOLUME
    global MAIN_COUNTER

    SPOTIFY_VOLUME -= 5
    if SPOTIFY_VOLUME < 0:
        SPOTIFY_VOLUME = 0
    if SPOTIFY_VOLUME > 100:
        SPOTIFY_VOLUME = 100
    try:
        sp.volume(SPOTIFY_VOLUME)
        MAIN_COUNTER = SPOTIFY_VOLUME
    except Exception as e:
        print("Spotify API error:", e)

def light_up():
    global WLED_CNTR
    global wled_ip

    WLED_CNTR += 10
    if WLED_CNTR < 0:
        WLED_CNTR = 0
    if WLED_CNTR > 254:
        WLED_CNTR = 254
    try:
        requests.get(f"http://{wled_ip}/win&A={WLED_CNTR}")
    except Exception as e:
        print("Error sending request to change light:", e)

def light_down():
    global WLED_CNTR
    global wled_ip

    WLED_CNTR -= 10
    if WLED_CNTR < 0:
        WLED_CNTR = 0
    if WLED_CNTR > 254:
        WLED_CNTR = 254
    try:
        requests.get(f"http://{wled_ip}/win&A={WLED_CNTR}")
    except Exception as e:
        print("Error sending request to change light:", e)


def change_mode():
    global WLED_PRESET
    global wled_ip
 
    if WLED_PRESET > 5:
        WLED_PRESET = 1
    try :
        url = f"http://{wled_ip}/win&PL={WLED_PRESET}"
        response = requests.post(url)
        
        if response.status_code == 200:
            WLED_PRESET += 1
            print("Preset changed successfully!")
        else:
            print(f"Error changing preset: {response.status_code}")
    except Exception as e:
        pass

def change_color():
    global wled_ip
    global color_counter

    if color_counter > 6:
        color_counter = 1
    try:
        color_payload = {
            "seg": [
                {
                    "col": [colors[color_counter]]
                }
            ]
        }
        url = f"http://{wled_ip}/json/state"
        response = requests.post(url, json=color_payload)
        if response.status_code == 200:
            print(f"Color changed to {colors[color_counter]} successfully!")
            color_counter += 1
        else:
            print(f"Failed to change color. Status code: {response.status_code}")
    except Exception as e:
        print("Error sending request to change light:", e)

def power():  
    try:
        requests.get(f"http://192.168.1.69/win&T=2")
    except Exception as e:
        print("Error sending request to change light:", e)

def play_pause():
    try:
        current_track = sp.current_playback()
        if current_track is not None:
            playback_state = current_track['is_playing']
            if playback_state:
                sp.pause_playback()
                print("Playback paused.")
            else:
                sp.start_playback()
                print("Playback started.")
        else:
            print("No track is currently playing.")
    except Exception as e:
        print("Spotify API error:", e)

# def previous_track():
#     try:
#         sp.previous_track()
#     except Exception as e:
#         print("Spotify API error:", e)

# def next_track():
#     try:
#         sp.next_track()
#     except Exception as e:
#         print("Spotify API error:", e)
 
command_mapping = {
    "VolumeUp": volume_up,
    "VolumeDown": volume_down,
    "BrightnessUp": brightness_up,
    "BrightnessDown": brightness_down,
    "MusicSeekUp": music_seek_up,
    "MusicSeekDown": music_seek_down,
    "LightUp": light_up,
    "LightDown": light_down,
    "PlayPause": play_pause,
    "Mute": mute,
    "MediaChange": media_change,
    "MediaChangeR": show_media,
    "Lock": lock,
    "Shutdown": shutdown,
    "ShutdownR": open_tskmgr,
    "ChangeMode": change_mode,
    "ChangeModeR": change_color,
    "Power": power,
    # "Previous": previous_track,
    # "Next": next_track
}

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
                if command in command_mapping:
                    command_mapping[command]()
                elif command == "GetTime":
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    ser.write((str(current_time)+'\n').encode())

                elif command == "GetDate":
                
                elif command == "GetBrightness":
                else:                    
                    print("Unknown command:", command)
                print( datetime.now().strftime("%H:%M:%S"),"Received command:", command)

        except serial.SerialException as e:
            print("Serial communication error:", e)
         
    ser.close()