import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

def find_com_port():

    global ports

    if len(ports) == 0:
        return None    
    else:       
        for port in ports:
            if port.vid == 6790 and port.pid == 29987:
                print("Success")
                return str(port.device)

def is_com_port_available(port):
    
    if len(ports) == 0:
        return False   
    else:       
        for port in ports:
            if port.vid == 6790 and port.pid == 29987:
 
                print("Success")
                return True


def get_com_port():
    ports = serial.tools.list_ports.comports()
    if len(ports) == 0:
        print("No serial ports found.")
        return None
    else:
        print("Available serial ports:")
        for port in ports:
            if port.vid == 6790 and port.pid == 29987:
                print("found your device : " , port.device )
                return str(port.device)