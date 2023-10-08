# import serial.tools.list_ports

# def main():
#     while True:
#         # Get a list of available serial ports
#         available_ports = list(serial.tools.list_ports.comports())
        
#         if available_ports:
#             print("Available USB devices:")
#             for port_info in available_ports:
#                 print(f"  Port: {port_info.device}, Description: {port_info.description}")

#         else:
#             print("No USB devices connected.")

#         try:
#             input("Press Enter to refresh...")  # Wait for user input to refresh
#         except KeyboardInterrupt:
#             print("Exiting.")
#             break

# if __name__ == "__main__":
#     main()

import serial.tools.list_ports

# def check_for_ch340_device():
#     ports = serial.tools.list_ports.comports()
    
#     for port in ports:
#         if "CH340" in port.description:
#             return True

#     return False

# if __name__ == "__main__":
#     while True:
#         if check_for_ch340_device():
#             print("USB-SERIAL CH340 device plugged in.")
#         else:
#             print("USB-SERIAL CH340 device not found.")
        
#         # You can adjust the polling interval as needed
#         import time
#         time.sleep(1)

for port in serial.tools.list_ports.comports():
    print(port.device)
    print(port.desc)
    print(port.hwid)
    print(port.vid)
    print(port.pid)
    print(port.name)
 
