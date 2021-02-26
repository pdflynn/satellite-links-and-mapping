import numpy as np
import pymap3d
from scipy import constants

class Link:
    def __init__(self, region, satellite, ground_station):
        self.region = region
        self.satellite = satellite
        self.ground_station = ground_station



# TODO: should LinkRegion remain satellite-agnostic?
class LinkRegion:

    # TODO: cannot have multiple constructors in Python, use *args for Pythonic implement
    # def __init__(self, sat_lat, sat_lon, sat_alt, R=6371e3, n=201):
    #     """Initialize LinkRegion with automatic region generation"""
    #     self.sat_lat = sat_lat
    #     self.sat_lon = sat_lon
    #     self.sat_alt = sat_alt

    # TODO: explicitly define all member variables
    def __init__(self, lat_min, lat_max, lon_min, lon_max, n=201):
        """Initialize LinkRegion with client-specified latitude and longitude region"""
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.lon_min = lon_min
        self.lon_max = lon_max

        # Set up latitude and longitude vectors
        self.lat_vec = np.linspace(self.lat_min, self.lat_max, n)
        self.lon_vec = np.linspace(self.lon_min, self.lon_max, n)

    # TODO: should this be a static function?
    def get_slant_paths(self, sat_lat, sat_lon, sat_alt, datum='wgs84'):
        """Gets the slant path length from each coordinate
        in the region to the specified satellite coordinate."""
        self.slant_paths = np.zeros((len(self.lat_vec), len(self.lon_vec)))
        for i in range(0, len(self.lat_vec)):
            for j in range(0, len(self.lon_vec)):
                self.slant_paths[i, j] = pymap3d.geodetic2aer(sat_lat, sat_lon, sat_alt, 
                                                         self.lat_vec[i], self.lon_vec[j], 0, datum)
        return self.slant_paths

    def get_radio_horizon(self, alt, R=6371e3):
        """Gets the LOS distance and radio horizon of the system given 
        an altitude and celestial body radius"""
        # Using the Pythagorean Theorem, d^2 = 2Rh + h^2, the line of sight distance
        self.dist_los = np.sqrt(2 * R * alt + np.power(alt, 2))
        self.dist_hoz = 4.12 * np.sqrt(alt) * 1000 # TODO: re-derive this for non-Earth celestial bodies

        return self.dist_los, self.dist_hoz

    def auto_set_boundaries(self, alt, R=6371e3):
        """Automatically sets the latitude and longitude boundaries of the
        region based on a satellite altitude"""
        los = self.get_radio_horizon(alt, R)[0]
        deg_offset = np.rad2deg(los / R)

        self.lat_min = self.sat_lat - deg_offset
        self.lat_max = self.sat_lat + deg_offset
        self.lon_min = self.sat_lon - deg_offset
        self.lon_max = self.sat_lon + deg_offset


class Satellite:
    def __init__(self, power_output, antenna_gain):
        pass
    


class GroundStation:
    def __init__(self, noise_temperature, antenna_gain):
        pass
    