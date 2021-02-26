# Link_Tools.py
# Last Modified: 21 February 2021
# Description: This file contains several relevant functions for computing link budgets

# TODO: Translate link tools over to objects, should be entirely OOP application


import numpy as np
from scipy import constants
import pymap3d


# calculate_eirp
# This function determines the EIRP (Equivalent Isotropic Radiated Power)
# of a transmitting antenna system based on the transmitter power output,
# cable losses, and antenna boresight gain.
# power_output: The transmitter systems output power (dBW)
# cable_loss: Any cable attenuation from the transmitter system (dB)
# antenna_gain: The boresight (phi=0, theta=0) gain of the transmitter system (dBi)
def calculate_eirp(power_output, cable_loss, antenna_gain):
    # Vectorize
    power_output = np.array(power_output)
    cable_loss = np.array(cable_loss)
    antenna_gain = np.array(antenna_gain)

    eirp = power_output - cable_loss + antenna_gain
    return eirp

# calculate_gt
# This function determines the receiver system G/T (gain over temperature)
# of a receiving antenna system based on the receiver antenna boresight gain,
# and system noise temperature 
# antenna_gain: THe boresight (phi=0, theta=0) gain of the receiver antenna (dBi)
# system_noise_temperature: The noise temperature of the receiver system (K)
def calculate_gt(antenna_gain, system_noise_temperature):
    # Vectorize
    antenna_gain = np.array(antenna_gain)
    system_noise_temperature = np.array(system_noise_temperature)

    gt = antenna_gain - 10 * np.log10(system_noise_temperature)

# calculate_prx
# This function takes an array of "Gains" and "Losses", and, independent of
# whether the values are input as positive or negative, determines the
# power received
# gains: An array containing all gains of the system (power transmitted, antenna gain, etc)
# losses: An array containing all losses of the system (FSPL, gas loss, etc)
def calculate_prx(gains, losses):
    # Do not vectorize
    # Normalize to positive numbers to accept broad input
    for i in range(0, len(gains)):
        gains[i] = np.abs(gains[i])
    for i in range(0, len(losses)):
        losses[i] = np.abs(losses[i])
    # Perform calculations    
    total_gains = np.sum(gains)
    total_losses = np.sum(losses)
    prx = total_gains - total_losses
    return prx

# calculate_fspl
# This function determines the Free Space Path Loss, derived from the Friis transmission
# equation, based on frequency and distance.
# dist: The distance between elements in the link, in meters
# freq: The frequency of the carrier wave of the signal, in Hz
def calculate_fpsl(dist, freq):
    # Vectorize
    dist = np.array(dist)
    freq = np.array(freq)
    FSPL = 20 * np.log10((4*np.pi*dist*freq) / constants.c)
    return FSPL
