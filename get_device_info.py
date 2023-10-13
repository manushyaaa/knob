import serial.tools.list_ports

def main():
    while True:
        available_ports = list(serial.tools.list_ports.comports())
        
        if available_ports:
            print("Available USB devices:")
            for port_info in available_ports:
                print(f"  Port: {port_info.device}, Description: {port_info.description} , HWID: {port_info.hwid}, VID: {port_info.vid}, PID: {port_info.pid}, Name: {port_info.name}")

        else:
            print("No USB devices connected.")

        try:
            input("Press Enter to refresh...")   
        except KeyboardInterrupt:
            print("Exiting.")
            break

if __name__ == "__main__":
    main()

 