# Link.py
# Author: Danny Flynn
# Date Modified: 20210603

class LinkHop():
    """ LinkHop represents a single transmit and receive path. For example,
        a LinkHop could be between a ground station and a satellite, between
        a satellite and a satellite, or between a satellite and a ground
        station. LinkHop requires at minimum one TRANSMITTER object and one
        RECEIVER object, as well as information about the channel. """
    def __init__(self, transmitter, channel, receiver):
        """ Initializes a new LinkHop consisting of a transmitter, channel,
            and receiver. """
        self.transmitter = transmitter
        self.channel = channel
        self.receiver = receiver

    def evaluate_hop(self):
        eirp = self.transmitter.get_eirp()
        gt = self.receiver.get_gt()
        tx_losses = self.transmitter.get_losses()
        rx_losses = self.receiver.get_losses()
        
