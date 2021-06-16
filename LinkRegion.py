# LinkRegion.py
# Author: Danny Flynn
# Date Modified: 20210615
from AntennaPattern import *

from astropy import constants as const
import pymap3d as pm
import numpy as np
import matplotlib.pyplot as plt

# Big TODOs
# - Implement support for other celestial bodies besides Earth
# - With this in mind...need to write my own geodetic2aer

class LinkRegion():
    # TODO: Swap lat0, lon0, alt0 to a Satellite object
    def __init__(self, lat0: float, lon0: float, alt0: float, resolution: int):
        """ Initializes a new LinkRegion based on a center point (satellite location) """

        # Suppose a tangent line exists along an Equatorial or Polar spherical Earth
        # Then for Latitude, the latitude angle alpha is between a line along the
        # zenith originating at the center of the Earth and a line originating at
        # the center of the Earth and terminating at the point where the tangent
        # line intersects the Earth. Likewise for longitude but with R_Earth different.
        # TODO: This shouldn't be hard-coded once I add other celestial body support
        x_o_lat = 6357e3 + alt0
        x_o_lon = 6378e3 + alt0

        # Fixed this: re-derived formula and it's arcsin, not sin...
        alpha = np.rad2deg(np.arcsin(np.sqrt(np.power(x_o_lat, 2) - np.power(6357e3, 2)) / x_o_lat))
        beta  = np.rad2deg(np.arcsin(np.sqrt(np.power(x_o_lon, 2) - np.power(6378e3, 2)) / x_o_lon))
        
        print("alpha: " + str(alpha))
        print("beta: " + str(beta))

        self.lat_vec = np.linspace(lat0 - alpha, lat0 + alpha, resolution)
        self.lon_vec = np.linspace(lon0 - beta, lon0 + beta, resolution)

        # Compute satellite observer to deg latitude's look angle to the region
        # Done in O(n) time complexity, better than looping through both latitudes and
        # longitudes as pymap3d doesn't seem to support full vectorization
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
        plot1 = plt.figure(1, dpi=300)
        plt.contourf(self.lat_vec, self.lon_vec, self.el_look_angles, resolution, cmap='RdGy')
        plt.colorbar()
        plt.title("Elevation Angles Seen by Sat")
        plt.ylabel("Latitude (deg)")
        plt.xlabel("Longitude (deg)")

        plot2 = plt.figure(2, dpi=300)
        plt.contourf(self.lat_vec, self.lon_vec, self.az_look_angles, resolution, cmap='GnBu')
        plt.colorbar()
        plt.title("Azimuth Angles Seen by Sat")
        plt.ylabel("Latitude (deg)")
        plt.xlabel("Longitude (deg)")

        plot3 = plt.figure(3, dpi=300)
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