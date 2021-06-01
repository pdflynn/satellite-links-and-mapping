from Terminal import Terminal
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pymap3d


# term = Terminal("uplink", 1, 0, 0, 300e3)

# print(term)
# # print(term.latvec)
# # print(term.lonvec)

# latlat,lonlon = np.meshgrid(term.latvec, term.lonvec)

# # print(latlat)
# print(latlat)
# print(np.size(latlat))
# print(np.size(lonlon))
# plt.plot(latlat, lonlon, marker='.')
# plt.show()

lat,lon,alt = 0,0,300e3
lat_vec = np.linspace(-10,10, 21)

[az,el,r] = pymap3d.geodetic2aer(lat,lon,alt,lat_vec,0,0)
print(az)
print(el)
print(r)