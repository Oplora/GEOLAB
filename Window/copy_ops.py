from transforms import *
from smoothing import *
from exceptions import *
from monitor import show

# MACRO-PARAMETERS
WEIGHTS = list()



def cross_cor(first_trace_values: list, second_trace_values: list, center_max=False):
    ''' Взаимная корреляция функций. Если последний параметр равен True, то вкф центриеруется'''
    vkf = np.correlate(first_trace_values, second_trace_values, mode='same')
    if not center_max:
        return vkf
    else:
        shift = lagrange(vkf)
        return fourier_shift(vkf, shift)  # previous vkf, but having real pick in zero


def auto_cor(trace_values: list):
    return np.correlate(trace_values, trace_values, mode='same')

def process_traces(window_width, trace1, trace2, calculate_both_akf=True) -> tuple:
    """Returns correlation functions: cross- abd auto-correlations - for given traces """
    trace_length = len(trace1)
    vkf = np.zeros(trace_length)
    akf1 = np.zeros(trace_length)
    akf2 = np.zeros(trace_length)
    for count in range(trace_length - window_width + 1):
        vkf += cross_cor(trace1, trace2)
        akf1 += auto_cor(trace1)
        if calculate_both_akf:
            akf2 += auto_cor(trace2)
    akf = [akf1, akf2] if calculate_both_akf else akf1
    return vkf, akf



def window(*image, width=None, result_storage=None):
    """Позволяет работать на некоторой части, а не целой трассе. Применяется выделяет такие подобласти на двух соседних
    трассах."""
    if result_storage is None:
        result_storage = WEIGHTS
    window_width = width if width is not None else len(image[0])
    trace_indices = range(len(image) - 1)
    trace_length = len(image[0])
    taper_ar = taper([1] * window_width)  # Не понимаю зачем это нужно. Построить графики для разных параметров taper
    vkf_list, akf_list = [], []
    for number in trace_indices:
        left_trace = image[number]
        right_trace = image[number+1]
        if number < max(trace_indices):
            correlations = process_traces(window_width, left_trace, right_trace, calculate_both_akf=False)
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
    if dim == 1:
        noise_rate = np.asarray([abs(value) for value in np.fft.rfft(akf - vkf, norm=fourier_normalization)])
        signal_rate = np.asarray([abs(value) for value in np.fft.rfft(vkf, norm=fourier_normalization)])
        stabilizing_coef = 0.1 * max(noise_rate)
        noisy_data = noise_presence_check(noise_rate) # (УДАЛИТЬ В КОНЦЕ ОТЛАДКИ)
        if noisy_data:
            snr = smooth(np.divide(signal_rate, (noise_rate + stabilizing_coef)), 7)
            # snr = np.divide(signal_rate, (noise_rate + stabilizing_coef))
        else:
            # Эта часть кода исключительно для этапа отладки (УДАЛИТЬ В КОНЦЕ ОТЛАДКИ).
            # Если мы подаем незашумленные данные, то отношение сигнал/
            # будет колосально большим. А чтобы моя процедура обработки на чистых данных работала корректно, нужно
            # все урезать
            # snr = smooth(signal_rate, 7)
            signal_rate = [1 if rate > 50 else 0 for rate in signal_rate]
            snr = signal_rate
        # snr = np.divide(snr, max(snr)) #normalization for right scale
        # show(snr, color=(0.25,0.25,0.25), fig_title='SNR')
        return snr
    elif dim == 2:
        snrs = []
        for i in range(len(vkf)):
            snrs.append(weights(vkf[i], akf[i], dim=1))
        return snrs
    else:
        raise ValueError("dim should be equal 1 or 2")


def alter_image(*image, coefficients):
    processed_image = []
    for i, trace in enumerate(image):
        # trace_in_freq_domain = fourier_shift(trace, domain='f')
        # mul_in_freq_domain = np.multiply(trace_in_freq_domain[0], coefficients[i])
        # processed_image.append(reverse_fourier(mul_in_freq_domain, trace_in_freq_domain[1]))
        trace_in_freq_domain = np.fft.rfft(trace, norm=fourier_normalization)
        mul_in_freq_domain = np.multiply(trace_in_freq_domain, coefficients[i])
        processed_image.append(np.fft.irfft(mul_in_freq_domain, norm=fourier_normalization))
    return processed_image

# def optimal_filter(*image):
#     """Действует лишь на одно изображение, а не на набор"""
#     snrs = window(*image) # Signal noise rates for every trace and each frequency
#     processed_image = alter_image(*image, coefficients=snrs)
#     return processed_image

# Дописать, но сначала наладить оптимальный фильтр (снр чистого сигнала)
# def optimal_image(*images):
#     processed_images = list()
#     for image in images:
#         processed_images.append(optimal_filter(image))
#     return np.mean(processed_images, axis=0)


# def normalized_coefficients(**SNR):
#     """ Function that returns specific normalizing coefficients for each coordinate SNR value. """
#     sum = 0
#     trace_amount = len(SNR.keys())
#     trace_length = len(SNR.get("0"))
#     norm_coef_dict = {}
#     norm_coef_ar = np.zeros((trace_amount, trace_length), dtype=np.double)
#     for j in range(trace_length):
#         for i in range(trace_amount):  # sum of every i-coordinate value
#             sum += SNR.get("{}".format(i))[j]
#         for i in range(trace_amount):
#             norm_coef_ar[i][j] = (SNR["{}".format(i)][j]) / sum
#             norm_coef_dict.update({"{}".format(i): norm_coef_ar[i]})
#         sum = 0
#     return norm_coef_dict
#
#
# def opti_sum(*image, **signal_noise_rates):
#     """ Main algorithm. Returns best SNR for given image. """
#     traces_amount = len(image)
#     trace_sum = 0
#     norm_coef = normalized_coefficients(**signal_noise_rates)
#     for i in range(traces_amount):
#         trace_sum += np.multiply(np.fft.rfft(image[i], norm=fourier_normalization), norm_coef["{}".format(i)])
#     processed_summed_trace = np.float32(np.fft.irfft(trace_sum))
#     return processed_summed_trace
#
#
# def optis(signal):
#     return opti_sum(*signal, **window(*signal)[2])
#
#
# def straight_sum(*image):
#     """ Basic sum of image, normalized by theirs amount. """
#     traces_amount = len(image)
#     trace_sum = 0
#     for i in range(traces_amount):
#         trace_sum += image[i]
#     processed_summed_trace = trace_sum / traces_amount
#     return processed_summed_trace
