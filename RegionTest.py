from LinkRegion import *
import matplotlib.pyplot as plt
import numpy as np

reg = LinkRegion(0, 0, 100e3, 250)
# reg.plot_region(100)

isotropic = AntennaPattern()

ext_phi = np.linspace(-180, 180, 361)
ext_the = np.linspace(-90, 90, 181)
helix = AntennaPattern('helix_phi0_360_the_n180_180.csv', ext_phi, ext_the)

cosine = AntennaPattern(4, 40)



proj_pattern = reg.project_antenna_pattern(cosine)

reg.plot_region(128)

plt.figure(dpi=300)
plt.contourf(reg.lat_vec, reg.lon_vec, proj_pattern, 128, cmap='jet')
plt.colorbar()
plt.show()