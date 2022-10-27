import unittest
import numpy as np
from Signal_class import Receiver, Signal, Noise


class Test(unittest.TestCase):

    def setUp(self):
        self.signal_1 = Signal([np.pi / 10, np.pi / 2])
        self.signal_1.BP_filter()
        self.noise_1 = Noise(1, np.cos)
        self.noise_1.paint()

        self.signal_2 = Signal([np.pi / 20, np.pi / 3])
        self.signal_2.BP_filter()
        self.noise_2 = Noise(1, np.sin)
        self.noise_2.paint()



