# AntennaPattern.py
# Author: Danny Flynn
# Date Modified: 20210601

from enum import Enum
import numpy as np
import math

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
            self.pattern = np.zeros((len(self.phi_range), len(self.theta_range)))
        elif len(args) == 2: # Cosine antenna with max Gain 
            self.phi_range = np.linspace(0, 360, 361)
            self.theta_range = np.linspace(0, 180, 181)
            order = args[0]
            gain = args[1]
            cos_th1 = np.cos(self.theta_range * (math.pi/180))
            cos_n = np.power(cos_th1, order)
            # For all phi cuts, same deal
            patt = np.zeros((len(self.phi_range), len(self.theta_range)), dtype=float)
            for i in range(0, len(self.phi_range)):
                patt[i, :] = gain * cos_n
            self.pattern = patt

        elif len(args) == 3:
            filepath = args[0]
            self.phi_range = args[1]
            self.theta_range = args[2]
            self.import_antenna_known_angles(filepath)
        elif len(args) == 4:
            self.phi_range = args[0]
            self.theta_range = args[1]
            self.pattern = args[2]

    def import_antenna_known_angles(self, filename):
        self.pattern = np.genfromtxt(filename, delimiter=',')
    
    def get_phi_range(self):
        return self.phi_range

    def get_theta_range(self):
        return self.theta_range

    def get_gain_pattern(self):
        return self.pattern

    def is_whole_sphere(self):
        pass

    def get_polarization(self):
        pass

