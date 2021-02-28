import numpy as np
import pymap3d
from scipy import constants


class Link:
    def __init__(self, region, satellite, ground_station):
        self.region = region
        self.satellite = satellite
        self.ground_station = ground_station


class LinkRegion:
    """ LinkRegion is the geographic bounds that a satellite can reach purely
        by line-of-sight."""

    def __init__(self, *args, R=6371e3, n=201):
        """ Constructor for LinkRegion creates a new LinkRegion"""
        if len(args) == 3:
            self.sat_lat = args[0]
            self.sat_lon = args[1]
            self.sat_alt = args[2]
            self.auto_set_boundaries(self.sat_alt, R)

        else if len(args) == 4:
            self.lat_min = args[0]
            self.lat_max = args[1]
            self.lon_min = args[2]
            self.lon_max = args[3]

        else raise ValueError('Invalid number of arguments passed to LinkRegion. Either specify the region by-satellite with three arguments (lat, lon, alt) or manually with four arguments (min_lat, max_lat, min_lon, max_lon')

        self.lat_vec = np.linspace(self.lat_min, self.lat_max, n)
        self.lon_vec = np.linspace(self.lon_min, self.lon_max, n)

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
        # TODO: re-derive this for non-Earth celestial bodies
        self.dist_hoz = 4.12 * np.sqrt(alt) * 1000

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
    def __init__(self, *args):
        """Creates a new Satellite. Pass PA output (dB) to argument 0, 
        radiation pattern (int or float or 3d Numpy array) to argument 1"""

        if len(args) == 2:
            if isinstance(args[1], int or float):
                # User has specified boresight gain for satellite
                # Set satellite overall radiation pattern to boresight value
            elif isinstance(args[1], np.ndarray):
                # User has specified 3D antenna pattern for satellite
                # Set satellite overall radiation pattern to passed value
            self.power_output = args[0]


class GroundStation:
    def __init__(self, *args):
        pass
