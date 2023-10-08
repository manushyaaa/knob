import serial  
import serial.tools.list_ports

import time
from pynput.keyboard import Key, Controller
import screen_brightness_control as sbc
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


client_id = 'ad7d4f3724b6446ebd37af580ca3273e'
client_secret = '0d9d08d329e54bc19abc36751534b8f8'
    
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret, 
                                                       redirect_uri='http://localhost:8888/callback',
                                                       scope='user-modify-playback-state'))
 
try:
    brightness = sbc.get_brightness()
except Exception as e:
    print("Error getting brightness:", e)
    brightness = None


ports = serial.tools.list_ports.comports()
keyboard = Controller()

BRIG_VAL = 50
WLED_CNTR = 150
SPOTIFY_VOLUME = 20
 
VID = 6790
PID = 29987


def get_com_port():
    global VID , PID 
    ports = serial.tools.list_ports.comports()
    if len(ports) == 0:
        print("No serial ports found.")
        return None
    else:
       # print("Available serial ports:")
        for port in ports:
            if port.vid == VID and port.pid == PID:
                print("found your device : " , port.device )
                return str(port.device)


def main():

    global BRIG_VAL
    global WLED_CNTR
    global SPOTIFY_VOLUME
    global port 

    while True:
        # Wait for COM256 to become available
        while not get_com_port():
            print( "COM not found -> Line 31"  )             
            time.sleep(1)

        try:
            ser = serial.Serial( get_com_port(), 115200)

            while True:
                
                command = ser.readline().strip().decode('utf-8')
                print(command)
                if command == "VolumeUp":
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)

                elif command == "VolumeDown":
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)

                elif command == "BrightnessUp":
                    BRIG_VAL += 5
                    try : 
                        sbc.set_brightness(BRIG_VAL)
                    except Exception as e : 
                        pass
                
                elif command == "BrightnessDown":
                    BRIG_VAL -= 5
                    try : 
                        sbc.set_brightness(BRIG_VAL)
                    except Exception as e : 
                        pass
 
                elif command == "MusicSeekUp":
                    SPOTIFY_VOLUME += 10
                    if SPOTIFY_VOLUME  < 0:
                        SPOTIFY_VOLUME  = 0
                    if SPOTIFY_VOLUME > 100:
                        SPOTIFY_VOLUME  = 100
                    try : 
                        sp.volume(SPOTIFY_VOLUME)                      
                    except Exception as e : 
                        pass
                
                elif command == "MusicSeekDown":
                    SPOTIFY_VOLUME -= 10
                    if SPOTIFY_VOLUME  < 0:
                        SPOTIFY_VOLUME  = 0
                    if SPOTIFY_VOLUME > 100:
                        SPOTIFY_VOLUME  = 100
                    try : 
                        sp.volume(SPOTIFY_VOLUME)
                    except Exception as e : 
                        pass
     
                elif command == "LightUp":
                    WLED_CNTR += 10
                    if WLED_CNTR < 0:
                        WLED_CNTR = 0
                    if WLED_CNTR > 254:
                        WLED_CNTR = 254
                    try : 
                        requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
                    except Exception as e : 
                        pass
                    
                elif command == "LightDown":
                    WLED_CNTR -= 10
                    if WLED_CNTR < 0:
                        WLED_CNTR = 0
                    if WLED_CNTR > 254:
                        WLED_CNTR = 254
                    try : 
                        requests.get(f"http://192.168.1.69/win&A={WLED_CNTR}")
                   
                    except Exception as e : 
                        pass



                elif command == "PlayPause":
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)

                elif command == "Mute":
                    keyboard.press(Key.media_volume_mute)
                    keyboard.release(Key.media_volume_mute)


                elif command == "MediaChange":                
                   pass

                elif command == "Lock":                
                    os.system('rundll32.exe user32.dll,LockWorkStation')
                    
                elif command == "Shutdown":                
                    os.system("shutdown /s /t 0")
                
                elif command == "ChangeMode":              
                    pass
                    
                elif command == "Power":                
                    pass

                elif command == "Previous": 

                    try : 
                        sp.previous_track()
                   
                    except Exception as e : 
                        pass               
                


                    

        except serial.SerialException as e:
            print("main loop Exception", e)
            pass

if __name__ == "__main__":
    main()
