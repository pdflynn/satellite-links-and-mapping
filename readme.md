# Satellite Links And Mapping (SLAM)
# Version Alpha 0.1

SLAM is an application I am working on in my free time that can help a satellite systems engineer design a constellation, visualize its coverage area, and determine
throughput and SNR at various points.

SLAM is open-source for personal and educational use. Please contact me if you would like to use this commercially.

# Latest Release: Alpha 0.1
The application is currently in pre-release Alpha. Use at your own risk - as of writing, there are essentially no features implemented yet (just a GUI shell), but
more will be added as I get to them.

# Upcoming Features:
- Single-satellite geographic link budget accounting for basic parameters (FSPL, EIRP, G/T)
- Single-satellite geographic link budget with more advanced parameters (Atmospheric loss, rain fade, cloud fade)
- Satellite orbit propagation using SGP4/SDP4 and time-based coverage
- GUI-based satellite and ground station configuration editor
- Map overlays including received power, SNR, throughput, BER, etc...
- Multi-satellite static geographic link budgets
- Multi-satellite dynamic (propagated) geographic link budgets
- Satellite constellation visualization
- Exporting link maps to shapefile and exporting to pretty static maps

# Features for Way Later:
These would be cool, but I don't yet have the knowledge to implement:
- Satellite constellation optimization for coverage area

