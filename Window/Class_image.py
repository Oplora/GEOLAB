import source_data as sd

from numpy import mean, pi

from exceptions import prCyan


class SeisImage():

    def __init__(self, traces: list, counts=sd.ALL_COUNTS):
        self.traces = traces
        self.counts = counts

    def __add__(self, other):
        from numpy import add
        summed_image = SeisImage(add(self.traces, other.traces))
        return summed_image

    def __truediv__(self, other):
        from numpy import int64
        if isinstance(other, int64):
            scaled_image = SeisImage(self.traces/other)
            return scaled_image
        else:
            raise TypeError(f"{type(other)}")

    @property
    def snrs(self):
        from ops import window
        return window(*self.traces)

    def optimal(self):
        """Transform given image to optimal image.
        Optimal image is the result of scaling image by it's SNR (signal/noise rates) """
        from ops import alter_image
        return SeisImage(alter_image(*self.traces, coefficients=self.snrs))

    @staticmethod
    def MCOP(images_list):
        """Multi-channel optimal filter"""
        from numpy import mean
        processed_images = []
        for image in images_list:
            if not isinstance(image, SeisImage):
                raise TypeError(f"MCOP can process only SeisImage's list, but found {type(image)}")
            else:
                processed_images.append((image.optimal()).traces)
        optimal_image = SeisImage(mean(processed_images, axis=0))
        # optimal_image = optimal_image
        return optimal_image
        # return mean(processed_images, axis=0)

    # @staticmethod
    # def plot(custom_X_axis: tuple, values, axis, color):
    #     from numpy import linspace
    #     if custom_X_axis is not None:
    #         start, stop, num = custom_X_axis
    #         counts = linspace(start, stop, num)
    #     else:
    #         counts = range(len(values))
    #     if color is not None:
    #         axis.plot(counts, values, color=color)
    #     else:
    #         axis.plot(counts, values)

    def show(self, snr=False, **kwargs):
        from Class_monitor import show
        if snr is True or snr == 'both':
            snrs = [snr[:int(sd.COUNTS / 2)] for snr in
                    self.snrs]  # Just to make visualization easier (FREQ increasing)
            abscissa_axis = (0, pi, sd.COUNTS // 2)
            if snr == 'both':
                show(*[self.traces, snrs], mode='sepcomb', X_axis=[None, abscissa_axis], **kwargs)
                return
            try:
                title = 'СНР ' + str(kwargs.pop('fig_title')).lower()
            except KeyError:
                title = 'СНР'
            show(*snrs, X_axis=abscissa_axis, fig_title=title, **kwargs)
        else:
            show(*self.traces, **kwargs)


