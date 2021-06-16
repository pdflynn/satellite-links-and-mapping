# Channel.py
# Author: Danny Flynn
# Date Modified: 20210615

class Channel():
    def __init__(self, use_region=False, use_atm_attn=False, use_rain_fade=False):
        self.use_region = use_region
        self.use_atm_attn = use_atm_attn
        self.use_rain_fade = use_rain_fade

    def evaluate_fspl(self):
        pass

    def evaluate_atm_attn(self):
        pass