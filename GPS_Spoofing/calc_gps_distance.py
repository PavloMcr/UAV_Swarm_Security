import math

def calc_distance(drone1, drone2):
    """
    Calculate the 3D distance between two sets of GPS coordinates, including altitude.

    Parameters:
    - drone1: Tuple of (latitude, longitude, altitude) for the first point.
    - drone2: Tuple of (latitude, longitude, altitude) for the second point.

    Returns:
    - A dictionary with 'gps_dist' as the calculated distance in meters,
      and 'gps_timestamp' as the current timestamp.
    """
    # Unpack coordinates
    lat1, lon1, alt1 = drone1
    lat2, lon2, alt2 = drone2

    # Convert from degrees to radians
    rad_lat1 = math.radians(lat1)
    rad_lon1 = math.radians(lon1)
    rad_lat2 = math.radians(lat2)
    rad_lon2 = math.radians(lon2)
    rad_delta_lon = rad_lon2 - rad_lon1
    R = 6371000  # Earth radius in meters

    # Spherical law of Cosines
    d_flat = math.acos(math.sin(rad_lat1) * math.sin(rad_lat2) +
                       math.cos(rad_lat1) * math.cos(rad_lat2) * math.cos(rad_delta_lon)) * R

    # Euclidean distance with respect to altitude
    euclidean_distance = math.sqrt(d_flat**2 + (alt1 - alt2)**2)

    # Assuming timestamp handling is done outside or using another utility function
    return {"gps_dist": euclidean_distance}
