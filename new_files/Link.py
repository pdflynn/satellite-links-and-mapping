class Link:
    """ Link defines a generic Link with no specified type.
        A Link has several types, including an Uplink, which usually
        consists of a ground station and satellite, an Interlink, or 
        Inter-Satellite Link (ISL), which consists of two satellites,
        and a Downlink, which also consists of a satellite and a receiving
        ground station."""
    def __init__(self):
        self.type = "Generic"

    def evaluate_EsNo:
        pass

    


class Uplink(Link):

    def __init__(self, terminal, satellite):
        self.type = "Uplink"
        self.terminal = terminal
        self.satellite = satellite



class Interlink(Link):

    def __init__(self, tx_satellite, rx_satellite):
        self.type = "Interlink"
        self.tx_satellite = tx_satellite
        self.rx_satellite = rx_satellite

class Downlink(Link):
    
    def __init__(self, ground_station, satellite):
        self.type = "Downlink"
        self.ground_station = ground_station
        self.satellite = satellite