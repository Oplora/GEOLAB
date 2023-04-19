from random import gauss, randint, uniform, seed
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# from ops import straight_sum, optis

# MACRO-PARAMETERS
FREQUENCY = 4  # improves band pass filter resolution in time domain, but messing up frequency domain.
# Use this parameter only in ploting images for diploma
COUNTS = 600  # Improves frequency domain for each signal
# to increase resolution in frequency domain. Not sure if it worked.
ALL_COUNTS = FREQUENCY * COUNTS
SEED = 1  # parameter to initialize random numbers generator. This controlling random factor is used in constructing
# 'random' geological area reflectivity
EXCEPTION_COLOR = '\033[1;35m'


# SIGNAL COMPONENTS CONSTRUCTORS

def geo_reflect(positions, values):
    """Returns one signal - geological reflectivity
    Geological reflectivity - signal with few pics at given positions.
    Values in those positions should be less then 1 by absolute value"""
    reflectivity = np.zeros(ALL_COUNTS)
    for k, i in enumerate(positions):
        try:
            reflectivity[i] = values[k]
        except IndexError:  # enables shift geo_reflectivity how we want
            print("{0} Some picks of geo_reflectivity wasn't recorded."
                  " Index {1} out of range {2}\033[00m".format(EXCEPTION_COLOR, i, ALL_COUNTS))
            continue
    return reflectivity


def add_noise(ar, math_exp=0, stand_dev=0.1):
    """ Adds gauss noise for given array (signal/trace). """
    for i in range(len(ar)):
        noise = gauss(mu=math_exp, sigma=stand_dev)
        ar[i] = ar[i] + noise
    return None


def band_pass_filter(w_min, w_max, show=False, crop=False):
    """ Band-pass filter in time axis."""
    max_sample = COUNTS
    freq = FREQUENCY
    # counts = range(-int(max_sample / 2), math.ceil(max_sample / 2))
    if show:
        w = np.linspace(w_min, w_max, num=max_sample)
        W_axis = np.linspace(0, w_min, num=max_sample).tolist() + w.tolist() + np.linspace(w_max, np.pi,
                                                                                           num=max_sample).tolist()
        A_axis = [0 for x in range(len(w))] + [1 for x in range(len(w))] + [0 for x in range(len(w))]
        fig = plt.figure()
        fig.set_figheight(13)
        fig.set_figwidth(13)
        ax = fig.add_subplot(111)
        ax.plot(W_axis, A_axis)
        fig.suptitle("Полосовой фильтр", fontsize=20, fontweight='bold')
        ax.set_xlabel('w, Гц', fontsize=13, style="italic")
        ax.set_ylabel('|A(w)|', fontsize=13, style="italic")
        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.88,
                            wspace=0.4,
                            hspace=0.4)
    counts = np.linspace(-int(max_sample / 2), math.ceil(max_sample / 2), num=max_sample * freq)
    hamming_window = []
    if w_min * w_max > 0 and abs(w_max) <= np.pi and abs(w_min) <= np.pi:  # Two rectangles
        for t in counts:
            f_t = np.sign(w_min) * (w_max * np.sinc(w_max * t / np.pi) - w_min * np.sinc(w_min * t / np.pi)) / np.pi
            hamming_window.append(f_t * (0.53836 + 0.46164 * np.cos(2 * np.pi * t / len(counts))))
        norma = max(hamming_window)
        hamming_window = [value / norma for value in hamming_window]
        return hamming_window
    else:
        print("Error!!!")
        return None

def pass_filter(*args):
    result = []
    for bpf in args:
        w1, w2 = zip(bpf)
        result.append(band_pass_filter(w1, w2))
    return result

def wave(band_pass_filter, amplitude=1):
    """Returns one signal - band pass filter in time domain, scaled by variable 'amplitude'"""
    return np.multiply(band_pass_filter, amplitude)


def signal(forming_wave, reflection, noise=None):
    CONV_MODE = 'same'
    out_signal = np.convolve(forming_wave, reflection, mode=CONV_MODE)
    if noise is not None:
        if not (isinstance(noise, float) or isinstance(noise, int)):
            raise ValueError('Standard deviation (noise=) should be numerical')
        add_noise(out_signal, stand_dev=noise)
    return out_signal


# SEISMIC IMAGES CONSTRUCTORS

def layers_dip(traces_amount):
    from random import randint, uniform, choices
    from numpy.polynomial.polynomial import Polynomial

    poly_coef = [uniform(-COUNTS/10, COUNTS/10) for _ in range(randint(2, 6))]
    P = Polynomial(poly_coef)
    dip_trajectory = [P(x) for x in np.linspace(-1, 1, num=1000)]
    registered_values = [round(val) for val in dip_trajectory[0::(round(1000/traces_amount))]]
    return registered_values


def area_reflectivity(geo_layers_amount, traces_amount, shift=0, rand=False):
    """Constructor for geophysical visualization of area. Crucial method for testing.
    :return list of reflectivity traces in each seismic source
    """
    seed(SEED)  # make random generator fixed (stationary)
    areal_reflect = []
    picks_positions = [randint(0, ALL_COUNTS) for _ in range(geo_layers_amount)]
    picks_values = [uniform(-1, 1) for _ in range(geo_layers_amount)]
    height_dif = layers_dip(traces_amount) if rand else [shift * i for i in range(traces_amount)]
    for i in range(traces_amount):
        picks_positions = np.add(picks_positions, height_dif[i])
        recordings = geo_reflect(picks_positions, picks_values)
        areal_reflect.append(recordings)
    seed(datetime.now())  # move random numbers generator back to loose state
    return areal_reflect


def seismic_image(forming_geo_area, forming_wave, stand_div=0):
    """Builds """
    image = []
    for recorded_reflectivity in forming_geo_area:
        pure_signal = signal(forming_wave, recorded_reflectivity, noise=stand_div)
        image.append(pure_signal)
    return image

