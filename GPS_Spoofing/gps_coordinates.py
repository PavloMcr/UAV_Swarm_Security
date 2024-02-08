from pymavlink import mavutil
import serial
import time
import math

class GPS_Coordinates:
    def __init__(self, timestamp=None, latitude=None, longitude=None, altitude=None):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.own_positions = []  # List to store GPS positions
        self.other_drones_positions = {} # Dictionary to store other drones' positions keyed by drone ID   
    @staticmethod
    def get_own_gps_coordinates(pixhawk):
        # Fetch GPS data and return as a tuple
        # Request GPS position from Pixhawk
        pixhawk.mav.request_data_stream_send(pixhawk.target_system, pixhawk.target_component, mavutil.mavlink.MAV_DATA_STREAM_POSITION, 1, 1)
        while True:
            msg = pixhawk.recv_match(type='GPS_RAW_INT', blocking=True)
            if msg:
                latitude = msg.lat / 1e7  # Convert to decimal degrees
                longitude = msg.lon / 1e7  # Convert to decimal degrees
                altitude = msg.alt / 1000.0  # Convert to meters
                timestamp = int(time.time())
                return latitude, longitude, altitude, timestamp # Returns a tuple                           
    @staticmethod
    def get_other_drone_gps_coordinates():
        # TODO: Implement the logic to listen for and receive GPS data from other drones
        # involves reading from a serial port, or another communication interface
        #        
        # return latitude, longitude, altitude, timestamp
        pass
    def add_own_coordinates(self, position_data):
        # this func should add current position to the list
        # position_data is a tuple: (latitude, longitude, altitude, timestamp)
        latitude, longitude, altitude, timestamp = position_data
        position = {'latitude': latitude, 'longitude': longitude, 'altitude': altitude, 'timestamp': timestamp}
        if len(self.own_positions) >= 5:
            self.own_positions.pop(0)  # Keep the list to a maximum of 5 positions
        self.own_positions.append(position)
        
    def add_other_drone_coordinates(self, drone_id, position_data):
        # Ensure there's a list for a drone with this drone_id
        if drone_id not in self.other_drones_positions:
            self.other_drones_positions[drone_id] = []
        # Add position data for the specified drone ID
        if len(self.other_drones_positions[drone_id]) >= 5:
            self.other_drones_positions[drone_id].pop(0)  # Limit to last 5 positions
        self.other_drones_positions[drone_id].append(position_data)
