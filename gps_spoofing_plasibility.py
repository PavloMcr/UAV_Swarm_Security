from pymavlink import mavutil
import serial
import time
import swarm_positions
import swarm_ranging
import math


# Connect to Pixhawk to get GPS 
# Initialize connection to Pixhawk
pixhawk = mavutil.mavlink_connection('/dev/serial', baud=115200)  # serial port & baud rate need to be adjusted

# Request GPS position

def get_own_gps_position():
    # Request GPS_RAW_INT messages
    pixhawk.mav.request_data_stream_send(pixhawk.target_system, pixhawk.target_component, mavutil.mavlink.MAV_DATA_STREAM_POSITION, 1, 1)

    while True:
        # Wait for GPS_RAW_INT message and extract GPS coordinates
        msg = pixhawk.recv_match(type='GPS_RAW_INT', blocking=True)
        if msg:
            latitude = msg.lat / 1e7  # Convert to decimal degrees
            longitude = msg.lon / 1e7  # Convert to decimal degrees
            altitude = msg.alt / 1000.0  # Convert to meters
            print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}m")
            break  # Remove break to continuously print GPS data



class GPS_Coordinates:
    def __init__(self, timestamp: int, latitude: float, longitude: float, altitude: float):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    @staticmethod
    def get_own_gps_coordinates():
        # Placeholder for method to request GPS data from Pixhawk
        # Actual implementation will depend on the communication setup with Pixhawk
        timestamp = int(time.time())
        latitude, longitude, altitude = 0.0, 0.0, 0.0  # Replace with actual request logic
        return GPS_Coordinates(timestamp, latitude, longitude, altitude)

    @staticmethod
    def get_drone_gps_coordinates():
        # Placeholder for method to request GPS data from neighboring drones
        # Implement based on the communication method used with the drones
        timestamp = int(time.time())
        latitude, longitude, altitude = 0.0, 0.0, 0.0  # Replace with actual request logic
        return GPS_Coordinates(timestamp, latitude, longitude, altitude)

    def calc_distance(self, other: 'GPS_Coordinates') -> Dict[str, float]:
        # Conversion from degrees to radians
        rad_lat_self = math.radians(self.latitude)
        rad_lon_self = math.radians(self.longitude)
        rad_lat_other = math.radians(other.latitude)
        rad_lon_other = math.radians(other.longitude)
        rad_delta = rad_lon_other - rad_lon_self
        R = 6371000  # Earth radius in meters

        # Spherical law of Cosines
        d_flat = math.acos(math.sin(rad_lat_self) * math.sin(rad_lat_other) +
                           math.cos(rad_lat_self) * math.cos(rad_lat_other) * math.cos(rad_delta)) * R

        # Euclidean distance with respect to altitude
        euclidean_distance = math.sqrt(d_flat**2 + (self.altitude - other.altitude)**2)

        timestamp = min(self.timestamp, other.timestamp)
        return {"gps_timestamp": timestamp, "gps_dist": euclidean_distance}


class UAVTelemetry:
    def __init__(self):
        self.gps_positions: List[GPS_Coordinates] = []

    def record_own_position(self):
        own_position = GPS_Coordinates.get_own_gps_coordinates()
        self.gps_positions.append(own_position)
        print(f"Recorded own position: {own_position.latitude}, {own_position.longitude}, {own_position.altitude}")

    def record_drone_position(self):
        drone_position = GPS_Coordinates.get_drone_gps_coordinates()
        self.gps_positions.append(drone_position)
        print(f"Recorded drone position: {drone_position.latitude}, {drone_position.longitude}, {drone_position.altitude}")

# Example usage
if __name__ == "__main__":
    uav_telemetry = UAVTelemetry()
    uav_telemetry.record_own_position()  # Record the UAV's own position
    uav_telemetry.record_drone_position()  # Record a neighboring drone's position
