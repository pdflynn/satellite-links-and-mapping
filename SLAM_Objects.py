import numpy as np
import pymap3d
from scipy import constants


class Project:
    self.link = Link(None, None, None)
    self.satellites = set()
    self.ground_stations = set()
    
    def __init__(self, filepath):
        pass





class Link:
    def __init__(self, region, satellite, ground_station):
        self.region = region
        self.satellite = satellite
        self.ground_station = ground_station

    def evaluate_simple_link(self, freq):
        self.region.compute_fspl(freq)
        CN = self.satellite.get_eirp() - self.region.get_fspl() + self.ground_station.get_gt()
        return CN

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

        elif len(args) == 4:
            self.lat_min = args[0]
            self.lat_max = args[1]
            self.lon_min = args[2]
            self.lon_max = args[3]

        else:
            raise ValueError('Invalid number of arguments passed to LinkRegion. Either specify the region by-satellite with three arguments (lat, lon, alt) or manually with four arguments (min_lat, max_lat, min_lon, max_lon')

        self.lat_vec = np.linspace(self.lat_min, self.lat_max, n)
        self.lon_vec = np.linspace(self.lon_min, self.lon_max, n)

    # TODO: should automatically set up
    def compute_slant_paths(self, sat_lat, sat_lon, sat_alt, datum=pymap3d.utils.Ellipsoid('wgs84')):
        """Gets the slant path length from each coordinate
        in the region to the specified satellite coordinate."""
        self.slant_paths = np.zeros((len(self.lat_vec), len(self.lon_vec)))
        for i in range(0, len(self.lat_vec)):
            for j in range(0, len(self.lon_vec)):
                [az, el, r] = pymap3d.geodetic2aer(sat_lat, sat_lon, sat_alt, self.lat_vec[i], self.lon_vec[j], 0, datum) # TODO: add datum changing
                self.slant_paths[i, j] = r
    
    def get_slant_paths(self):
        if self.slant_paths is None:
            raise ValueError('No slant paths! Compute them.')
        else:
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

    # Gets the Free Space Path Loss along each path within the slant path vector
    def compute_fspl(self, freq):
        if self.slant_paths is not None:
            self.FSPL = 20 * np.log10((4*np.pi*self.slant_paths*freq) / constants.c)
        else:
            raise ValueError("No slant paths! Must compute first.")
    
    def get_fspl(self):
        if self.FSPL is not None:
            return self.FSPL
        else:
            raise ValueError("FSPL Not computed!")


# TODO: Rename "Transmitter?"
class Satellite:
    def __init__(self, *args):
        """Creates a new Satellite. Pass PA output (dB) to argument 0, 
        radiation pattern (int or float or 3d Numpy array) to argument 1.
        Any losses incurred due to cable attenuation or other effects between
        the output of Amplifier and Antenna passed to argument 2 (dB)."""
        if len(args) >= 2:
            if isinstance(args[1], int or float):
                # User has specified boresight gain for satellite
                # Set satellite overall radiation pattern to boresight value
                self.radiation_pattern = np.full((361, 181), args[1])
                # 1 degree increments by default
                self.phi = np.linspace(-180, 180, 361)
                self.theta = np.linspace(-90, 90, 181)
            elif isinstance(args[1], np.ndarray):
                # User has specified 3D antenna pattern for satellite
                # Set satellite overall radiation pattern to passed value
                self.radiation_pattern = args[1]
                # Assume pattern is all-encompassing a far-field sphere
                shape = self.radiation_pattern.shape
                self.phi = np.linspace(-180, 180, shape[0])
                self.theta = np.linspace(-90, 90, shape[1])

        # Account for losses, or set to zero if none specified.
        if len(args) >= 3:
            self.losses = args[2]
        else:
            self.losses = 0
        
        # Assign power output from first argument
        self.power_output = args[0]
    
    # Get the satellite's power output
    def get_power_output(self):
        return self.power_output
    
    # Get the satellite's radiation pattern, phi, and theta vectors.
    def get_radiation_pattern(self):
        return self.radiation_pattern, self.phi, self.theta
    
    # Get the satellite's losses, if any
    def get_losses(self):
        return self.losses

    # Calculates the satellite's EIRP (Equivalent Isotropic Radiated Power)
    # and returns it as the output of the function.
    # EIRP = PA (dB) - Loss (dB) + Gain (dBi)
    def get_eirp(self):
        return self.power_output - self.losses + self.radiation_pattern[0, 0] # TODO: incorporate angles and all that



# TODO: rename "Receiver?"
class GroundStation:
    """ Creates a new Ground Station. A ground station consists of, at minimum,
    a number or array specifying the radiation pattern (Gain) of the receiver
    antenna system at the ground station, and a system noise temperature. If
    no system noise temperature is specified, a value of 750 K is used."""
    def __init__(self, *args):
        if isinstance(args[1], int or float):
            # User has specified boresight gain for ground station
            # Set ground station overall radiation pattern to boresight value
            self.radiation_pattern = np.full((361, 181), args[1])
            # 1 degree increments by default
            self.phi = np.linspace(-180, 180, 361)
            self.theta = np.linspace(-90, 90, 181)

        elif isinstance(args[1], np.ndarray):
            # User has specified 3D antenna pattern for ground station
            # Set ground station overall radiation pattern to passed values
            self.radiation_pattern = args[1]
            # Assume pattern is all-encompassing a far-field sphere
            shape = self.radiation_pattern.shape
            self.phi = np.linspace(-180, 180, shape[0])
            self.theta = np.linspace(-90, 90, shape[1])

        self.system_noise_temperature = args[0]

        # Gets the ground station system noise temperature
    def get_system_noise_temperature(self):
        return self.system_noise_temperature

    # Gets the radiation pattern, and accompanying phi and theta vectors
    def get_radiation_pattern(self):
        return self.radiation_pattern, self.phi, self.theta

    # Gets the G/T (gain to temperature ratio) of the receiver system
    def get_gt(self):
        return self.radiation_pattern[0,0] - 10 * np.log10(self.system_noise_temperature) # TODO: pattern