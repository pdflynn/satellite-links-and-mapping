import SLAM_Objects
from time import process_time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

satellite = SLAM_Objects.Satellite(30, 5)
groundstation = SLAM_Objects.GroundStation(315, 8)
region = SLAM_Objects.LinkRegion(0, -80, 600e3)

# print(region.lat_vec)
# print(region.lon_vec)
t1 = process_time()
region.compute_slant_paths(0, -80, 600e3)
a = region.get_slant_paths()
print(a)
t2 = process_time()
print("time elapsed", str(t2-t1))

budget = SLAM_Objects.Link(region, satellite, groundstation)

oversimplified_cn = budget.evaluate_simple_link(300e6)
print(oversimplified_cn)

imgplt = plt.imshow(oversimplified_cn)
plt.show()