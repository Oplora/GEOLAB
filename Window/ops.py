""" Библиотека для обработки сигналов с помощью многоканального фильтра, описанного в работе"""

from transforms import *
from smoothing import *


def cross_correlation(first_trace_values: list, second_trace_values: list, center_max=False):
    vkf = np.correlate(first_trace_values, second_trace_values, mode='same')
    # Debug_vkf += vkf  # adds to return from window function
    # np.double(vkf)
    if not center_max:
        return vkf
    else:
        shift = lagrange(vkf)
        # shifted_vkf += np.add(shifted_vkf, fourier_shift(vkf, shift))  # previous vkf, but having real pick in zero
        return fourier_shift(vkf, shift)  # previous vkf, but having real pick in zero


def autocorrelation(trace_values: list):
    return np.correlate(trace_values, trace_values, mode='same')


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
    wei = []  # container for SNRs
    trace_length = len(traces_arr[0])
    taper_ar = taper([1] * window_width)
    All_debug_akfs = []
    All_debug_vkfs = []
    while k < len(traces_arr):
        i = 0
        counts_vkf = trace_length
        Debug_vkf = np.zeros(counts_vkf)
        pair_of_seismotes = traces_arr[(k - 1):(k + 1)]
        shifted_vkf = np.zeros(counts_vkf)
        akf_l = np.zeros(counts_vkf)
        akf_r = np.zeros(counts_vkf)
        # while i < trace_length - window_width + 1:
        for i in range(trace_length - window_width + 1):
            trace_left = np.zeros(trace_length)
            trace_right = np.zeros(trace_length)
            for j in range(window_width):
                trace_left[j + i] = taper_ar[j] * pair_of_seismotes[0][i + j]
                trace_right[j + i] = taper_ar[j] * pair_of_seismotes[1][i + j]
            # vkf = np.correlate(trace_left, trace_right, mode='same')
            # Debug_vkf += vkf  # adds to return from window function
            # np.double(vkf)
            # shift = lagrange(vkf)
            # shifted_vkf += np.add(shifted_vkf, fourier_shift(vkf, shift))  # previous vkf, but having real pick in zero
            Debug_vkf += cross_correlation(trace_left, trace_right)
            print(len(Debug_vkf))
            shifted_vkf += cross_correlation(trace_left, trace_right, center_max=True)

            # akf_l += np.add(akf_l, np.correlate(trace_left, trace_left, mode='same'))
            # akf_r += np.add(akf_r, np.correlate(trace_right, trace_right, mode='same'))
            akf_l += autocorrelation(trace_left)
            akf_r += autocorrelation(trace_right)
            # i += 1  # Counter of windows amount on one seismote
        # av_akf_left = akf_l / (trace_length - window_width + 1)
        # av_akf_right = akf_r / (trace_length - window_width + 1)
        # av_vkf = shifted_vkf / (trace_length - window_width + 1)
        av_akf_left = akf_l
        av_akf_right = akf_r
        av_vkf = shifted_vkf
        All_debug_vkfs.append(Debug_vkf / (trace_length - window_width + 1))
        All_debug_akfs.append(av_akf_left)
        snr_l = weights(av_vkf, av_akf_left)
        snr_r = weights(av_vkf, av_akf_right)
        weights_dict.update({"{}".format(str(k - 1)): snr_l,
                             "{}".format(str(k)): snr_r})  # adds last coefficients counted for given trace
        wei.append(snr_l)
        k += 1
        if k == len(traces_arr):
            wei.append(snr_r)
    return [All_debug_akfs, All_debug_vkfs, weights_dict, wei]


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
