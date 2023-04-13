from transforms import *
from smoothing import *
from exceptions import *



# MACRO-PARAMETERS
WEIGHTS = list()


def cross_cor(first_trace_values: list, second_trace_values: list, center_max=False, make_even=False):
    ''' Взаимная корреляция функций. Если последний параметр равен True, то вкф центриеруется'''
    vkf = np.correlate(first_trace_values, second_trace_values, mode='same')
    if center_max:
        shift = lagrange(vkf)
        vkf = fourier_shift(vkf, shift)  # previous vkf, but having real pick in zero
    if make_even:
        vkf_parts = np.split(vkf, 2)
        mean = vkf_parts[0] + np.flip(vkf_parts[1])
        even_vkf = np.concatenate((mean, np.flip(mean)))
        vkf = even_vkf
    return vkf


def auto_cor(trace_values: list):
    return np.correlate(trace_values, trace_values, mode='same')

def process_traces(window_width, trace1, trace2, calculate_both_akf=True) -> tuple:
    """Returns correlation functions: cross- abd auto-correlations - for given traces """
    trace_length = len(trace1)
    vkf = np.zeros(trace_length)
    akf1 = np.zeros(trace_length)
    akf2 = np.zeros(trace_length)
    for count in range(trace_length - window_width + 1):
        vkf += cross_cor(trace1, trace2, center_max=True, make_even=True)
        akf1 += auto_cor(trace1)
        if calculate_both_akf:
            akf2 += auto_cor(trace2)
    akf = [akf1, akf2] if calculate_both_akf else akf1
    return vkf, akf

def window(*image, process_function=process_traces, width=None, result_storage=None):
    """Позволяет работать на некоторой части, а не целой трассе. Применяется выделяет такие подобласти на двух соседних
    трассах."""
    if result_storage is None:
        result_storage = WEIGHTS
    window_width = width if width is not None else len(image[0])
    trace_indices = range(len(image) - 1)
    vkf_list, akf_list = [], []
    for number in trace_indices:
        left_trace = image[number]
        right_trace = image[number+1]
        if number < max(trace_indices):
            correlations = process_function(window_width, left_trace, right_trace, calculate_both_akf=False)
            akf_list.append(correlations[1])
        else:
            correlations = process_traces(window_width, left_trace, right_trace, calculate_both_akf=True)
            akf_list.extend(correlations[1])
        vkf_list.append(correlations[0])
    vkf_mean = np.mean(vkf_list, axis=0)
    VKFs = [vkf_mean for _ in range(len(image))]
    AKFs = akf_list
    result_storage = weights(VKFs, AKFs, dim=2)
    return result_storage



def weights(vkf, akf, dim=1):
    """ Coefficients, showing ratio between signal and noise. """
    from source_data import ALL_COUNTS
    if dim == 1:
        noise_rate = np.asarray([abs(value) for value in np.fft.rfft(akf - vkf, norm=fourier_normalization)])
        signal_rate = np.asarray([abs(value) for value in np.fft.rfft(vkf, norm=fourier_normalization)])
        stabilizing_coef = 0.1 * max(noise_rate)
        snr = smooth(np.divide(signal_rate, (noise_rate + stabilizing_coef)), ALL_COUNTS * 0.005)
        return snr
    elif dim == 2:
        snrs = []
        for i in range(len(vkf)):
            snrs.append(weights(vkf[i], akf[i], dim=1))
        return snrs
    else:
        raise ValueError("dim should be equal 1 or 2")


def alter_image(*image, coefficients):
    from numpy import multiply
    from numpy.fft import rfft, irfft
    processed_image = []
    true_scaling_coef, n, d = 0, 0, 0
    for trace, coefficients in zip(image, coefficients):
        trace_in_freq_domain = rfft(trace, norm=fourier_normalization)
        mul_in_freq_domain = multiply(trace_in_freq_domain, coefficients)
        processed_trace = irfft(mul_in_freq_domain, norm=fourier_normalization)
        d += max(processed_trace)
        n += max(trace)
        processed_image.append(processed_trace)
    true_scaling_coef = float(n / d)
    return [optimal_trace * true_scaling_coef for optimal_trace in processed_image]
