from math import ceil, factorial
import numpy as np


def taper(arr):
    """ Smooth edges by converting rectangle to trapeze"""
    length = len(arr)
    delta = ceil(length * 0.1)  # 5-10% of length
    for i in range(delta + 1):
        arr[i] = i * arr[delta] / delta
        arr[length - 1 - i] = i * (-arr[length - 1] + arr[length - 1 - delta]) / delta
    return arr


def smooth(arr, window_width):
    """ Smooth given trace. Used in SNR.
    Reduce fluctuations in given array."""
    smoothed_arr = arr.copy()
    for i in range(len(arr)):
        summary = 0
        n = 0
        for j in range(i - int(window_width / 2), i + int(window_width / 2) + 1):
            if (j >= 0) and (j < len(arr)):
                summary += smoothed_arr[j]
                n += 1
        smoothed_arr[i] = summary / n
    return smoothed_arr

# def savitzky_golay(y, window_size, order, deriv=0, rate=1):
#     try:
#      window_size = np.abs(np.int_(window_size))
#      order = np.abs(np.int_(order))
#     except ValueError as msg:
#         raise ValueError("window_size and order have to be of type int")
#     if window_size % 2 != 1 or window_size < 1:
#      raise TypeError("window_size size must be a positive odd number")
#     if window_size < order + 2:
#      raise TypeError("window_size is too small for the polynomials order")
#     order_range = range(order+1)
#     half_window = (window_size -1) // 2
#     # precompute coefficients
#     b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
#     m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
#     # pad the signal at the extremes with
#     # values taken from the signal itself
#     firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
#     lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
#     y = np.concatenate((firstvals, y, lastvals))
#     return np.convolve(m[::-1], y, mode='valid')

