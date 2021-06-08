from LinkNode import *
from AntennaPattern import *

# Create an isotropic antenna source
isotropic = AntennaPattern()
print("--- Antenna Pattern Information ---")
print("\phi: " + str(isotropic.get_phi_range()))
print("\theta: " + str(isotropic.get_theta_range()))

# Create a transmitting ground station
tx_gnd = TransmitTerminal(isotropic, 30) # 30 dBm = 1 Watt
print(" --- Transmitting Terminal Information ---")
print("TX antenna pattern: ", str(isotropic))
print("TX EIRP (dBm): " + str(tx_gnd.get_eirp()))