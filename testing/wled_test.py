import requests
import time

# Define the WLED device IP address
wled_ip = "192.168.1.69"

# List of colors to cycle through (RGB format)
colors = [
    [255, 0, 0],  # Red
    [0, 255, 0],  # Green
    [0, 0, 255],  # Blue
]

# Delay between color changes (in seconds)
delay = 5  # Change color every 5 seconds

while True:
    for color in colors:
        # Construct the JSON payload with the current color
        color_payload = {
            "seg": [
                {
                    "col": [color]
                }
            ]
        }

        # Send an HTTP POST request to change the color
        url = f"http://{wled_ip}/json/state"
        response = requests.post(url, json=color_payload)

        if response.status_code == 200:
            print(f"Color changed to {color} successfully!")
        else:
            print(f"Failed to change color. Status code: {response.status_code}")

        time.sleep(delay)
