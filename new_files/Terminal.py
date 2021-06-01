import numpy as np

class Terminal:

    def __init__(self, type, *args):
        # Uplink definition of a terminal (acting as transmitter)
        if type == "uplink":
            if len(args) == 4:
                self.antenna_pattern = args[0]
                npts = 32
                self.auto_generate_coordinates(npts, args[1], args[2], args[3], None)

            elif len(args) == 5:
                self.antenna_pattern = args[0]
                self.latvec = args[1]
                self.lonvec = args[2]
                self.altvec = args[3]

        # Downlink definition of a terminal (acting as receiver)
        elif type == "downlink":
            if len(args) == 3:
                self.antenna_pattern = args[0]
                self.lat_lon_alt = args[1]
                self.boresight_vector = args[2]

    def auto_generate_coordinates(self, npts, lat0, lon0, alt0, ellipsoid):
        """ auto_generate_coordinates takes an input resolution (npts), and a center
            latitude (deg), longitude (deg), and altitude (m) above MSL and assigns
            NumPy arrays of latitudes, longitudes, and altitudes within the radio
            horizon of the center coordinate to the terminal """
        # Determine the line-of-sight distance 
        # TODO: This needs to be adjusted for all ellipsoids, not just spheres
        R = 6371e3
        dist_los = np.sqrt(2 * R * alt0 + np.power(alt0, 2))
        deg_offset = np.rad2deg(dist_los / R)

        # TODO: circular increment to bounds within geodetic coordinate system
        lat_min = lat0 - deg_offset
        lat_max = lat0 + deg_offset
        lon_min = lon0 - deg_offset
        lon_max = lon0 + deg_offset

        # Assign the latitude and longitude vectors
        self.latvec = np.linspace(lat_min, lat_max, npts)
        self.lonvec = np.linspace(lon_min, lon_max, npts)



            
        