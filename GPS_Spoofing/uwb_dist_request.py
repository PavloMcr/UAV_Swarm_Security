import serial
import time

def request_uwb_distance(serial_port='/dev/ttyS0', baudrate=115200):
    """
    Requests a UWB distance measurement from a DWM module.
    
    Parameters:
    - serial_port: The serial port to which the DWM module is connected.
    - baudrate: The baud rate for serial communication.
    
    Returns:
    - The measured distance in meters, or None if an error occurred.
    """
    try:
        # Initialize serial connection
        ser = serial.Serial(serial_port, baudrate, timeout=1)
        # Send a command to request a distance measurement
        ser.write(b'REQUEST_DISTANCE\n')
        
        # Wait for the response
        response = ser.readline().decode().strip()
        ser.close()
        
        # Convert the response to a distance value
        # The conversion depends on the response format
        distance = float(response)  # Placeholder conversion
        
        return distance
    except Exception as e:
        print(f"Error requesting UWB distance: {e}")
        return None
