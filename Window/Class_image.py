import source_data as sd
from copy_ops import window, alter_image
from numpy import add, int64, mean, pi
from Class_monitor import Monitor
from exceptions import prCyan


class SeisImage(Monitor):

    def __init__(self, traces, counts=sd.ALL_COUNTS):
        self.traces = traces
        self.counts = counts

    def __add__(self, other):
        summed_image = SeisImage(add(self.traces, other.traces))
        return summed_image

    def __truediv__(self, other):
        if isinstance(other, int64):
            scaled_image = SeisImage(self.traces/other)
            return scaled_image
        else:
            raise TypeError(f"{type(other)}")

    @property
    def snrs(self):
        return window(*self.traces)

    def optimal(self):
        return SeisImage(alter_image(*self.traces, coefficients=self.snrs))

    @staticmethod
    def MCOP(images_list):
        """Multi-channel optimal filter"""
        processed_images = []
        for image in images_list:
            if not isinstance(image, SeisImage):
                raise TypeError(f"MCOP can process only SeisImage's list, but found {type(image)}")
            else:
                processed_images.append(image.optimal())
        optimal_image = SeisImage(mean(processed_images, axis=0))
        # return optimal_image
        return mean(processed_images, axis=0)

    def show(self, snr=False, **kwargs):
        if snr is True or snr:
            try:
                title = 'СНР ' + str(kwargs.pop('fig_title')).lower()
            except KeyError:
                title = 'СНР'
            snrs = [snr[:int(sd.COUNTS / 2)] for snr in
                    self.snrs]  # Just to make visualization easier (FREQ increasing)
            abscissa_axis = (0, pi, sd.COUNTS // 2)
            super().show(*snrs, X_axis=abscissa_axis, fig_title=title, **kwargs)
        else:
            super().show(*self.traces, **kwargs)
