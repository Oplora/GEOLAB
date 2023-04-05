import source_data as sd
from copy_ops import window, alter_image


class SeisImage:

    def __init__(self, traces, counts=sd.ALL_COUNTS):
        self.traces = traces
        self.counts = counts

    @property
    def snrs(self):
        return window(*self.traces)

    def optimal(self):
        return SeisImage(alter_image(*self.traces, coefficients=self.snrs))

