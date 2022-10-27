import cmath
import math
import random
from obspy import read
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
import numpy as np
# from cmath import exp

def smothing(arr, window_width):
    smoothed_arr = arr.copy()
    for i in range(len(arr)):
        summary = 0
        n = 0
        for j in range(i - int(window_width / 2), i + int(window_width / 2) + 1):
            if (j >= 0) and (j < len(arr)):
                summary += smoothed_arr[j]
                n += 1
        arr[i] = summary / n
    # arr = smoothed_arr



if __name__ == '__main__':
    st = read('http://examples.obspy.org/RJOB_061005_072159.ehz.new')
    print(st)
    tr = st[0]
    print(tr.stats)
    print(tr.stats.delta)
    print(tr.stats.npts)
