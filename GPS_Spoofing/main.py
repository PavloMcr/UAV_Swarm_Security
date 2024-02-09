from pymavlink import mavutil
from gps_coordinates import GPS_Coordinates
from calc_gps_distance import calc_distance
import serial
import time
import math


# Execute
def main():
  
    try:
        pixhawk = mavutil.mavlink_connection('/dev/serial', baud=115200)  # serial port & baud rate
        # Wait for the first heartbeat to confirm the connection
        heartbeat = pixhawk.wait_heartbeat(timeout=5)  # Timeout in seconds
        if heartbeat:
            gps_handler = GPS_Coordinates()  # Instantiate your GPS handler class
            own_coords = GPS_Coordinates.get_own_gps_coordinates(pixhawk, timeout=5)
            # TODO: Implement the fetching of other drone coordinates
            # other_coord = GPS_Coordinates.get_other_drone_gps_coordinates("Communication Hub")
            # gps_handler.add_other_drone_coordinates(other_coord) 
            if own_coords:
                gps_handler.add_own_coordinates(own_coords)               
            else:
                print("Failed to retrieve GPS coordinates.")                
        else:
            print("Failed to receive heartbeat from Pixhawk.")            
    except Exception as e:
        print(f"Error during Pixhawk communication: {e}")  
    
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
