from source_data import FREQUENCY
import numpy as np
import matplotlib.pyplot as plt
import cmath

fourier_normalization = 'backward'


def fourier_shift(f_t, shift_t=0, domain='t'):
    """ Procedure that convert trace to frequency domain and shift trace by given time.
        Returns trace in time domain if parameter domain='t', otherwise returns in frequency domain."""
    # N = f_t.size
    N = len(f_t)
    fourier_transform = np.fft.rfft(f_t, n=N, norm=fourier_normalization)
    frequency_samples = np.fft.rfftfreq(N)
    S_w = fourier_transform
    if shift_t != 0:
        exponents = np.asarray([cmath.exp(complex(0, -2 * np.pi * w * (-shift_t))) for w in frequency_samples])
        S_w = np.multiply(fourier_transform, exponents)
    f_t = np.fft.irfft(S_w, n=N, norm=fourier_normalization) if domain == 't' else [S_w, N]
    return f_t


def reverse_fourier(f_w, frequency_samples):
    return np.fft.irfft(f_w, n=frequency_samples, norm=fourier_normalization)


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
