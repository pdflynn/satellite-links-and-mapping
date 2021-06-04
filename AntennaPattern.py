# AntennaPattern.py
# Author: Danny Flynn
# Date Modified: 20210601

from enum import Enum
import numpy as np

class Polarization(Enum):
    LINEAR = 0
    RHCP = 1
    LHCP = 2
    TOTAL_POWER = 3

class AntennaPattern():
    """ AntennaPattern represents a far-field antenna gain
        pattern of a transmitting or receiving antenna. This object
        supports imports from several different far-field antenna data
        formats, including .ffd, HFSS default format, and 2D grid format.
        The AntennaPattern object also includes the associated phi and
        theta angles of the pattern in degrees."""
    def __init__(self, *args, polarization=Polarization.TOTAL_POWER):
        """ Initializes a new AntennaPattern object. There are three ways
            to initialize: with no elements for an isotropic element, with 
            one filepath argument for an externally imported pattern, or 
            with three arguments to specify the phi range, theta range, and
            2D-tabular values with NumPy arrays."""
        if len(args) == 0:
            self.phi_range = np.linspace(0, 360, 361)
            self.theta_range = np.linspace(0, 180, 181)
            self.pattern = np.zeros(len(self.phi_range), len(self.theta_range))
        elif len(args) == 1:
            filepath = args[0]
            self.import_antenna_pattern(filepath)
        elif len(args) == 3:
            self.phi_range = args[0]
            self.theta_range = args[1]
            self.pattern = args[2]

    def import_antenna_pattern(self, filepath):
        pass
    
    def get_phi_range(self):
        pass

    def get_theta_range(self):
        pass

    def get_gain_pattern(self):
        pass

    def is_whole_sphere(self):
        pass

    def get_polarization(self):
        pass

