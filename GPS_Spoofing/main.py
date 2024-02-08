from pymavlink import mavutil
from gps_coordinates import GPS_Coordinates
from calc_gps_distance import calc_distance
import serial
import time
import math


# Execute
def main():
    
    pixhawk = mavutil.mavlink_connection('/dev/serial', baud=115200)  # Needs to be adjusted
    # Create the GPS_Coordinates class instance
    gps_handler = GPS_Coordinates()
    # Fetch own drone's GPS coordinates
    own_coords = GPS_Coordinates.get_own_gps_coordinates(pixhawk)
    # Add own drone's GPS coordinates to the list
    gps_handler.add_own_coordinates(own_coords)
    
    # TODO: Implement the fetching of other drone coordinates
    other_coord = GPS_Coordinates.get_other_drone_gps_coordinates("Communication Hub") # Need to implement
    gps_handler.add_other_drone_coordinates(other_coord) 
    
  # Now calculate the distance between your own drone and the other drone
    if gps_handler.own_positions and drone_id in gps_handler.other_drones_positions:
        own_latest_position = gps_handler.own_positions[-1]
        other_drone_latest_position = gps_handler.other_drones_positions[drone_id][-1]

        # Unpack the positions into tuples
        own_position_tuple = (own_latest_position['latitude'], own_latest_position['longitude'], own_latest_position['altitude'])
        other_position_tuple = (other_drone_latest_position['latitude'], other_drone_latest_position['longitude'], other_drone_latest_position['altitude'])

        # Calculate the distance
        distance_info = calc_distance(own_position_tuple, other_position_tuple)
        print(f"Distance to drone {drone_id}: {distance_info['gps_dist']} meters")    

    
if __name__ == "__main__":
    main()
