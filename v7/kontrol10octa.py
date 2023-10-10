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

# Load configuration from a JSON file
with open("v6\config.json", "r") as config_file:
    config = json.load(config_file)

MAIN_COUNTER = 0 

BRIG_VAL = config["brightness"]
WLED_CNTR = config["wled_brightness"]
SPOTIFY_VOLUME = config["spotify_volume"]
VID = config["serial_vid"]
PID = config["serial_pid"]

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

# def media_change():
#     pass
# def media_changeR():                                                                                                                                                                                                                                                                                                                                                                                                                               
#     pass

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

#def shutdownR():
#pass

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
    WLED_CNTR += 10
    if WLED_CNTR < 0:
        WLED_CNTR = 0
    if WLED_CNTR > 254:
        WLED_CNTR = 254
    try:
        requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
    except Exception as e:
        print("Error sending request to change light:", e)

def light_down():
    global WLED_CNTR
    WLED_CNTR -= 10
    if WLED_CNTR < 0:
        WLED_CNTR = 0
    if WLED_CNTR > 254:
        WLED_CNTR = 254
    try:
        requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
    except Exception as e:
        print("Error sending request to change light:", e)

def change_mode():
    pass

# def change_modeR():
#     pass
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

def mute():
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)


def previous_track():
    try:
        sp.previous_track()
    except Exception as e:
        print("Spotify API error:", e)

def next_track():
    try:
        sp.next_track()
    except Exception as e:
        print("Spotify API error:", e)

 
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
    # "MediaChange": media_change,
    # "MediaChangeR": media_change,
    "Lock": lock,
    "Shutdown": shutdown,
    # "ChangeMode": change_mode,
    # "ChangeModeR": change_mode,
    "Power": power,
    "Previous": previous_track,
    "Next": next_track,
}

def time_sender_thread(_gateway):
    while True:
        # Get the current time
        while not get_com_port():
            print("COM not found. Waiting...")
            time.sleep(1)

        current_time = datetime.now().strftime("  %H:%M:%S")
        print("Sending time:", current_time)

        # Send the time to the serial port
        try:
            ser.write(current_time.encode())
        except serial.SerialException as e:
            print("Serial communication error:", e)

        time.sleep(1)  # Send time every 1 second

 

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
                action = command_mapping.get(command)

                if action:
                    MAIN_COUNTER = 0
                    action()
                    
                else:
                    print("Unknown command:", command)
                data_per = MAIN_COUNTER
                ser.write((str(data_per)).encode())

        except serial.SerialException as e:
            print("Serial communication error:", e)
         
    ser.close()