import numpy as np
from random import seed, gauss, randint
from scipy.fft import fft
import matplotlib.pyplot as plt


class Receiver:
    def __init__(self):
        self.values = []
        self.boarders = None

    def __add__(self, other):
        """ Define addition in the class. It gives new element of the class """
        sum = Receiver()

        differences = len(self.values) - len(other.values)

        # IF THEY HAVE DIFFERENT AMOUNT OF COUNTS, THEN ADD SOME 0 TO MAKE IT POSSIBLE FOR ADDITION
        if differences < 0:
            self.values = np.append(self.values, [0] * abs(differences))
        else:
            other.values = np.append(other.values, [0] * abs(differences))

        sum.values = np.add(self.values, other.values)

        sum.boarders = [0, max(self.boarders[1], other.boarders[1])]
        return sum

    def seismogram(self, seismote_amount, spacing, mode='left'):
        """ Makes seismogram based on amount of picks, spacing between them and relevant location of source.  Returns
        array of Receiver elements"""
        seismogram = [self]

        for k in range(seismote_amount):  # cycle for making seismotes, based on given one (self)
            next_seismote = Receiver()
            # generating new signal (replaced seismote)
            next_seismote.values = np.append([0] * (k + 1) * spacing,
                                             self.values.tolist()[: (len(self.values) - (k + 1) * spacing)])

            # If source is one right side, then adding seismotes on left side of seismogram, otherwise adding on right
            seismogram = np.append(next_seismote, seismogram) if mode == 'right' else np.append(seismogram,
                                                                                                next_seismote)

        if mode == 'middle':
            # copy, then remove starting seismote (the self) and flip it
            first_part = np.delete(seismogram.copy(), 0)[::-1]
            seismogram = np.append(first_part, seismogram)  # stick up both parts
        return seismogram

    def seismote(self, noise, n, mode='basic', counts=0):  # MAKES SEISMOGRAM. IT'S COMBINING SEISMOTE
        signal = Receiver()

        if mode == 'one':
            signal = self
            mode = 'null'
        else:
            # generate n random "starting" digital counts of given signal (self)
            starts = [randint(0, n * len(self.values)) for _ in range(n)]
            starts.sort()
            for point in starts:
                r = Receiver()  # will contain sum of n-times moved copies of given signal
                r.values = np.flipud(np.append(np.flipud(self.values), [0] * point))  # move given signal (first count
                # of the signal) on previously generated "starting" point; FLIPUD - REVERSING OF ARREY
                signal = signal + r  # save result of preceding lines

        # set new value for class Noise constant "counts"
        Noise.counts = len(signal.values) if len(signal.values) > counts else counts
        noise.paint(mode=mode)  # paint given noise
        signal = noise + signal  # add noise to final signal

        return signal

    @property
    def FFT(self):  # FORWARD FOURIER TRANSFORM
        w = fft(self.values)
        A = [abs(x) for x in w]
        return A

    @staticmethod
    def show(object):  # shows object.values, where object belongs to Receiver class
        plt.style.use('seaborn')

        fig = plt.figure()
        ax = plt.axes()
        A = object.values[::-1]
        B = [x for x in range(object.boarders[0],object.boarders[1])]
        ax.plot(A, B)
        fig.suptitle('Сейсмограмма')
        plt.show()


class Noise(Receiver):
    counts = 200

    def __init__(self, mathematical_expectation, dispersion, convoluting_function):
        super().__init__()
        self.boarders = [0, self.counts]
        self.normal_distribution = [mathematical_expectation, dispersion]
        self.convoluting_function = convoluting_function
        self.values = [gauss(mathematical_expectation, dispersion) for _ in range(self.counts)]

    def paint(self, mode='basic'):  # СОЗДАЕТ И ПОДКРАШИВАЕТ ШУМ, if mode is not 'basic' then there is no noise, just
        # lines of zeroes
        # seed()  # Let us always get random noise
        # values = [gauss(self.normal_distribution[0], self.normal_distribution[1]) for _ in range(self.counts + 1)]
        paint = [self.convoluting_function(x) for x in range(int(self.counts / 10))]  # CONVOLUTING FUNCTION HAS 10
        # LESS VALUES
        self.boarders = [0, self.counts]
        self.values = [1 * elements / 300 for elements in np.convolve(self.values, paint).tolist() if
                       9 < np.convolve(self.values, paint).tolist().index(elements) < (
                               self.counts + self.counts / 10 - 1) - 10] if mode == 'basic' \
            else np.zeros(len(self.values) + len(paint) - 1).tolist()
        # np.convolve(values, paint) выдавал объект типа numpy.ndarray. Я преобразовал его в list и домножил на
        # коэфициент (на глаз подобрал), чтобы макисмальное отклонение не превышало 1/10 от максимального пика фильтра.
        # # 1 / 200 to decrease noise amplitude around 10% of our BP_filter max valu


class Signal(Receiver):
    counts = int((Noise.counts + Noise.counts / 10) - 21)

    def __init__(self, boarders):
        super().__init__()
        self.boarders = boarders  # array type. Example: [1, 3]

    def BP_filter(self):  # our band-press filer in time axis
        w1 = min(self.boarders)
        w2 = max(self.boarders)
        t = np.linspace(-self.counts / 2, self.counts / 2, self.counts).astype(int)  # integer time values array
        if w1 * w2 > 0 and abs(w2) <= np.pi and abs(w1) <= np.pi:  # Two rectangles
            f_t = np.sign(w1) * (w2 * np.sinc(w2 * t / np.pi) - w1 * np.sinc(w1 * t / np.pi)) / np.pi
            hamming_window = f_t * (0.53836 + 0.46164 * np.cos(2 * np.pi * t / self.counts))
            # Division by np.pi because of original definition of sinc(x) in python
            self.values = hamming_window
            self.limiting_frequency = np.pi
        else:
            print('Invalid boarders values!')


n1 = Noise(100, 50)
# n1.paint()
Receiver.show(n1)
