import datetime
import math
import random
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
import cmath
from scipy.signal import fftconvolve

fourier_normalization = 'backward'


def show(*values, fig_label=None, mode='sep', color=None):
    """ Make graphs for given arrays. """
    amount_of_plots = len(values)
    if mode == 'sep':
        fig, axes = plt.subplots(nrows=amount_of_plots, ncols=1)
        if amount_of_plots == 1:
            counts = [k for k in range(len(values[0]))]
            axes.plot(counts, values[0])
        else:
            for i in range(amount_of_plots):
                counts = [k for k in range(len(values[i]))]
                if color is not None:
                    axes[i].plot(counts, values[i], color=color[i])
                else:
                    axes[i].plot(counts, values[i])
        fig.suptitle('{}'.format(str(fig_label)), fontsize=10)
    elif mode == 'comb':
        for i in range(amount_of_plots):
            plt.plot(range(len(values[i])), values[i], label=str(i))
        plt.legend()
        plt.title('{}'.format(str(fig_label)), fontsize=10)
    plt.show()


def add_noise(ar, math_exp=0, stand_dev=0.1):
    """ Adds gauss noise for given array. """
    for i in range(len(ar)):
        noise = random.gauss(mu=math_exp, sigma=stand_dev)
        ar[i] = ar[i] + noise
    return None


def bpf(w1, w2, max_sample):
    """ Band-pass filter in time axis."""
    counts = range(-int(max_sample / 2), math.ceil(max_sample / 2))
    hamming_window = []
    if w1 * w2 > 0 and abs(w2) <= np.pi and abs(w1) <= np.pi:  # Two rectangles
        for t in counts:
            f_t = np.sign(w1) * (w2 * np.sinc(w2 * t / np.pi) - w1 * np.sinc(w1 * t / np.pi)) / np.pi
            hamming_window.append(f_t * (0.53836 + 0.46164 * np.cos(2 * np.pi * t / len(counts))))
        norma = max(hamming_window)
        hamming_window = [value / norma for value in hamming_window]
        return hamming_window
    else:
        print("Error!!!")
        return None


def add_bpf(to_signal, this_signal, sample):
    """ Adds band-pass filter to given array, it's pick locates in given sample. """
    bp = this_signal.copy()
    pick_of_bp = int(np.argwhere(bp == max(bp)))
    shift_pick_by = pick_of_bp - (sample + 1)
    del bp[0:shift_pick_by + 1]
    for i in range(shift_pick_by + 1):
        bp.append(0)
    processed_signal = np.add(to_signal, bp)
    return processed_signal


def taper(arr):
    """ Smooth edges by converting rectangle to trapeze"""
    length = len(arr)
    delta = math.ceil(length * 0.1)  # 5-10% of length
    for i in range(delta + 1):
        arr[i] = i * arr[delta] / delta
        arr[length - 1 - i] = i * (-arr[length - 1] + arr[length - 1 - delta]) / delta
    return arr


def smooth(arr, window_width):
    """ Smooth given trace. Used in SNR"""
    smoothed_arr = arr.copy()
    for i in range(len(arr)):
        summary = 0
        n = 0
        for j in range(i - int(window_width / 2), i + int(window_width / 2) + 1):
            if (j >= 0) and (j < len(arr)):
                summary += smoothed_arr[j]
                n += 1
        arr[i] = summary / n
    return arr


def fourier_shift(f_t, shift_t=0, domain='t'):
    """ Procedure that convert trace to frequency domain and shift trace by given time.
        Returns trace in time domain if parameter domain='t', otherwise returns in frequency domain."""
    N = f_t.size
    fourier_transform = np.fft.rfft(f_t, n=N, norm=fourier_normalization)
    frequency_samples = np.fft.rfftfreq(N)
    S_w = fourier_transform
    if shift_t != 0:
        exponents = np.asarray([cmath.exp(complex(0, -2 * np.pi * w * (-shift_t))) for w in frequency_samples])
        S_w = np.multiply(fourier_transform, exponents)
    f_t = np.fft.irfft(S_w, n=N, norm=fourier_normalization) if domain == 't' else S_w
    return f_t


def lagrange(cross_correlation, points_frequency=100, polynomial_power=4, show='no'):
    """ Interpolation with Lagrange polynomials. """
    x_max = int(np.argwhere(cross_correlation == max(cross_correlation))[0])
    x_axis = np.array([i for i in range(len(cross_correlation))])
    x = x_axis[(x_axis >= x_max - (polynomial_power / 2)) & (x_axis <= x_max + (polynomial_power / 2))]
    y = cross_correlation[min(x):max(x) + 1]
    y_poly = np.array([], np.double)
    x_poly = np.linspace(x[0], x[-1], num=points_frequency)
    for xp in x_poly:
        yp = 0
        for xi, yi in zip(x, y):
            yp += yi * np.prod((xp - x[x != xi]) / (xi - x[x != xi]))
        y_poly = np.append(y_poly, yp)
    y_poly_max = max(y_poly)
    x_poly_max = x_poly[int(np.argwhere(y_poly == y_poly_max)[0])]

    if show == 'yes':
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
        ax1.plot(x_axis, cross_correlation, 'k', x, y, 'ro', x_poly, y_poly, 'b', x_poly_max, y_poly_max, 'go')
        ax2.plot(x, y, 'ro', x_poly, y_poly, 'b', x_poly_max, y_poly_max, 'go')
        plt.show()
    return x_poly_max - int(len(cross_correlation) / 2)


def weights(vkf, akf):
    """ Coefficients, showing ratio between signal and noise. """
    rakf = np.asarray([abs(value) for value in fourier_shift(akf - vkf, domain='f')])
    vkf = np.asarray([abs(value) for value in fourier_shift(vkf, domain='f')])
    w_akf = np.asarray([abs(value) for value in fourier_shift(akf, domain='f')])
    gamma = max(abs(w_akf))
    snr = smooth(np.divide(vkf, (rakf + 0.1 * gamma)), 7)
    return snr


def window(*traces_arr, width=None):
    """ Main processing function. It's purpuse is
    1: Splinter given arrays on sub-arrays.
    2: Find ratio signal/noise for neighbouring arrays (for every frequency).
    3: Return array of weight sets (adds last counted coefficients for given trace)
    """
    k = 1  # k = 1, because I want to start convolution from pair (traces[0], traces[1])
    window_width = width if width is not None else len(traces_arr[0])
    weights_dict = {}  # container for SNRs
    trace_length = len(traces_arr[0])
    taper_ar = taper([1] * window_width)
    AKF = []
    VKF = []
    while k < len(traces_arr):
        i = 0
        pair_of_seismotes = traces_arr[(k - 1):(k + 1)]
        counts_vkf = trace_length
        vkf_to_return = np.zeros(counts_vkf)
        shifted_vkf = np.zeros(counts_vkf)
        akf_l = np.zeros(counts_vkf)
        akf_r = np.zeros(counts_vkf)
        while i < trace_length - window_width + 1:
            trace_left = np.zeros(trace_length)
            trace_right = np.zeros(trace_length)
            for j in range(window_width):
                trace_left[j + i] = taper_ar[j] * pair_of_seismotes[0][i + j]
                trace_right[j + i] = taper_ar[j] * pair_of_seismotes[1][i + j]
            vkf = np.correlate(trace_left, trace_right, mode='same')
            vkf_to_return += vkf  # adds to return from window function
            np.double(vkf)
            shift = lagrange(vkf)
            shifted_vkf += np.add(shifted_vkf, fourier_shift(vkf, shift))  # previous vkf, but having real pick in zero
            akf_l += np.add(akf_l, np.correlate(trace_left, trace_left, mode='same'))
            akf_r += np.add(akf_r, np.correlate(trace_right, trace_right, mode='same'))
            i += 1  # Counter of windows amount on one seismote
        av_akf_left = akf_l / (trace_length - window_width + 1)
        av_akf_right = akf_r / (trace_length - window_width + 1)
        av_vkf = shifted_vkf / (trace_length - window_width + 1)
        VKF.append(vkf_to_return / (trace_length - window_width + 1))
        AKF.append(av_akf_left)
        snr_l = weights(av_vkf, av_akf_left)
        snr_r = weights(av_vkf, av_akf_right)
        weights_dict.update({"{}".format(str(k - 1)): snr_l,
                             "{}".format(str(k)): snr_r})  # adds last coefficients counted for given trace
        k += 1
    return [AKF, VKF, weights_dict]


def normalized_coefficients(**SNR):
    """ Function that returns specific normalizing coefficients for each coordinate SNR value. """
    sum = 0
    trace_amount = len(SNR.keys())
    trace_length = len(SNR.get("0"))
    norm_coef_dict = {}
    norm_coef_ar = np.zeros((trace_amount, trace_length), dtype=np.double)
    for j in range(trace_length):
        for i in range(trace_amount):  # sum of every i-coordinate value
            sum += SNR.get("{}".format(i))[j]
        for i in range(trace_amount):
            norm_coef_ar[i][j] = (SNR["{}".format(i)][j]) / sum
            norm_coef_dict.update({"{}".format(i): norm_coef_ar[i]})
        sum = 0
    return norm_coef_dict


def opti_sum(*traces, **signal_noise_rates):
    """ Main algorithm. Returns best SNR for given traces. """
    traces_amount = len(traces)
    trace_sum = 0
    norm_coef = normalized_coefficients(**signal_noise_rates)
    for i in range(traces_amount):
        trace_sum += np.multiply(np.fft.rfft(traces[i], norm=fourier_normalization), norm_coef["{}".format(i)])
    processed_summed_trace = np.float32(np.fft.irfft(trace_sum))
    return processed_summed_trace


def optis(signal):
    return opti_sum(*signal, **window(*signal)[2])


def straight_sum(*traces):
    """ Basic sum of traces, normalized by theirs amount. """
    traces_amount = len(traces)
    trace_sum = 0
    for i in range(traces_amount):
        trace_sum += traces[i]
    processed_summed_trace = trace_sum / traces_amount
    return processed_summed_trace

