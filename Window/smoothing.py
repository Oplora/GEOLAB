import math


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