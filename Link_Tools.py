# Link_Tools.py
# Last Modified: 21 February 2021
# Description: This file contains several relevant functions for computing link budgets
import numpy as np


# calculate_eirp
# This function determines the EIRP (Equivalent Isotropic Radiated Power)
# of a transmitting antenna system based on the transmitter power output,
# cable losses, and antenna boresight gain.
# power_output: The transmitter systems output power (dBW)
# cable_loss: Any cable attenuation from the transmitter system (dB)
# antenna_gain: The boresight (phi=0, theta=0) gain of the transmitter system (dBi)
def calculate_eirp(power_output, cable_loss, antenna_gain):
    eirp = power_output - cable_loss + antenna_gain
    return eirp

# calculate_gt
# This function determines the receiver system G/T (gain over temperature)
# of a receiving antenna system based on the receiver antenna boresight gain,
# and system noise temperature 
# antenna_gain: THe boresight (phi=0, theta=0) gain of the receiver antenna (dBi)
# system_noise_temperature: The noise temperature of the receiver system (K)
def calculate_gt(antenna_gain, system_noise_temperature):
    gt = antenna_gain - 10 * np.log10(system_noise_temperature)

