# LinkRegion.py
# Author: Danny Flynn
# Date Modified: 20210611
from AntennaPattern import *

from astropy import constants as const
import pymap3d as pm
import numpy as np
import matplotlib.pyplot as plt


class LinkRegion():
    # TODO: Swap lat0, lon0, alt0 to a Satellite object
    def __init__(self, lat0: float, lon0: float, alt0: float, resolution: int):
        """ Initializes a new LinkRegion based on a center point (satellite location) """
        # Compute approximate line of sight distance (update in future versions)
        d_los = np.sqrt(2 * const.R_earth.value * alt0)
        theta_los = d_los / const.R_earth.value
        self.lat_vec = np.linspace(lat0 - theta_los, lat0 + theta_los, resolution)
        self.lon_vec = np.linspace(lon0 - theta_los, lon0 + theta_los, resolution)

        # Compute satellite observer's look angle to the region
        # Done in O(n) time complexity, better than looping through both latitudes and
        # longitudes as pymap3d doesn't seem to support that
        self.az_look_angles = np.zeros((len(self.lat_vec), len(self.lon_vec)), dtype=float)
        self.el_look_angles = np.zeros((len(self.lat_vec), len(self.lon_vec)), dtype=float)
        self.slant_path_lengths = np.zeros((len(self.lat_vec), len(self.lon_vec)), dtype=float)
        for i in range(0, len(self.lat_vec)):
            # for j in range(0, len(lon_vec)):
            az, el, distance = pm.geodetic2aer(self.lat_vec[i], self.lon_vec, 0, lat0, lon0, alt0)
            self.az_look_angles[i,:] = az
            self.el_look_angles[i,:] = 90 + el
            self.slant_path_lengths[i,:] = distance

    def plot_region(self, resolution: int):
        """ Creates plots showing the elevation angles, azimuth angles, and slant path
            lengths seen by the observing satellite of the link region """
        plot1 = plt.figure(1)
        plt.contourf(self.lat_vec, self.lon_vec, self.el_look_angles, resolution, cmap='RdGy')
        plt.colorbar()
        plt.title("Elevation Angles Seen by Sat")
        plt.ylabel("Latitude (deg)")
        plt.xlabel("Longitude (deg)")

        plot2 = plt.figure(2)
        plt.contourf(self.lat_vec, self.lon_vec, self.az_look_angles, resolution, cmap='GnBu')
        plt.colorbar()
        plt.title("Azimuth Angles Seen by Sat")
        plt.ylabel("Latitude (deg)")
        plt.xlabel("Longitude (deg)")

        plot3 = plt.figure(3)
        plt.contourf(self.lat_vec, self.lon_vec, self.slant_path_lengths, resolution, cmap='Greens')
        plt.colorbar()
        plt.title("Slant Path Ranges")
        plt.ylabel("Latitude (deg)")
        plt.xlabel("Longitude (deg)")

        plt.show()

    def project_antenna_pattern(self, antenna: AntennaPattern) -> np.array:
        phi = antenna.get_phi_range()
        the = antenna.get_theta_range()
        gain = antenna.get_gain_pattern()

        self.projected_gain = np.zeros((len(self.lat_vec), len(self.lon_vec)), dtype=float)
        # TODO: can this be done with matrix operations?
        for i in range(0, len(self.lat_vec)):
            for j in range(0, len(self.lon_vec)):
                closest_phi_indx = np.argmin(abs(self.az_look_angles[i,j] - phi))
                closest_the_indx = np.argmin(abs(self.el_look_angles[i,j] - the))
                self.projected_gain[i,j] = gain[closest_phi_indx, closest_the_indx]

        return self.projected_gain