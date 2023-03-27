import random
import math
import numpy as np
import matplotlib.pyplot as plt


def add_noise(ar, math_exp=0, stand_dev=0.1):
    """ Adds gauss noise for given array. """
    for i in range(len(ar)):
        noise = random.gauss(mu=math_exp, sigma=stand_dev)
        ar[i] = ar[i] + noise
    return None


def bpf(w1, w2, max_sample, freq=1, show=False, ):
    """ Band-pass filter in time axis."""
    # counts = range(-int(max_sample / 2), math.ceil(max_sample / 2))
    if show:
        w = np.linspace(w1, w2, num=max_sample)
        W_axis = np.linspace(0, w1, num=max_sample).tolist() + w.tolist() + np.linspace(w2, np.pi , num=max_sample).tolist()
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
    counts = np.linspace(-int(max_sample / 2),  math.ceil(max_sample / 2), num=max_sample*freq)
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


def geo_reflect(length, positions, values):
    reflectance = np.zeros(length)
    for k, i in enumerate(positions):
        reflectance[i] = values[k]
    return reflectance


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
