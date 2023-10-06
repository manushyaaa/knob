# import requests

# url = "http://192.168.1.69/win&A=255"

# try:
#     response = requests.get(url)
#     if response.status_code == 200:
#         print("Request successful")
#     else:
#         print(f"Request failed with status code: {response.status_code}")
# except requests.exceptions.RequestException as e:
#     print(f"Request error: {e}")
# import win10toast 
from win10toast import ToastNotifier

# Create a ToastNotifier object
toaster = ToastNotifier()

# Display a simple toast notification
toaster.show_toast("Notification Title", "This is the notification message.", duration=10)
