from ops import *

if __name__ == '__main__':

    counts = int(600 / 4)

    delta_1 = np.zeros(counts)  # δ-impulse with pick at 74
    delta_1[int(296 / 4)] = 40
    # show(delta_1)

    bpf_1 = bpf(0.2, 3, counts)  # band-pass filter with w1=0.2 and w2=3
    bpf_2 = bpf(0.1, 1, counts)  # band-pass filter with w1=0.5 and w2=1

    shift_t = 0

    signal_1 = np.convolve(delta_1, bpf_1, mode='same')
    # signal_11 = fourier_shift(signal_1.copy(), shift_t)
    # signal_1 = delta_1
    signal_11 = signal_1.copy()

    signal_2 = np.convolve(delta_1, bpf_2, mode='same')
    # signal_21 = fourier_shift(signal_2.copy(), shift_t)
    # signal_2 = delta_1.copy()
    signal_21 = signal_2.copy()
    # show(signal_1, signal_2)

    s_d = 1
    # add_noise(signal_1, stand_dev=s_d)
    # add_noise(signal_11, stand_dev=s_d)
    # add_noise(signal_2, stand_dev=s_d)
    # add_noise(signal_21, stand_dev=s_d)
    cross_section1 = [signal_1, signal_2]
    cross_section2 = [signal_11, signal_21]

    # Frequency domain
    w_signal_1 = [abs(v) for v in fourier_shift(signal_1, domain='f')]
    w_signal_2 = [abs(v) for v in fourier_shift(signal_2, domain='f')]
    w_signal_11 = [abs(v) for v in fourier_shift(signal_11, domain='f')]
    w_signal_21 = [abs(v) for v in fourier_shift(signal_21, domain='f')]
    w_cross_section1 = [w_signal_1, w_signal_2]

    MAX1 = (w_signal_1)
    #Shift testing
    signal_1 = fourier_shift(signal_1, shift_t=1.7)
    w_signal_1 = [abs(v) for v in fourier_shift(signal_1, domain='f')]
    MAX2 = (w_signal_1)
    print(MAX1,"\n", MAX2)
    print(len(MAX1), "\n", len(MAX2))
    show(signal_1, signal_11)
    show(w_signal_1, w_signal_11)


    # Without snr
    s1 = straight_sum(*cross_section1)
    s2 = straight_sum(*cross_section2)
    snr_non_opti_sum = window(s1, s2)
    # With snr
    os1 = opti_sum(*cross_section1, **window(*cross_section1))
    # f_os1 = [abs(v) for v in fourier_shift(os1, domain='f')]
    # show(os1, f_os1, fig_label="Opti_sum_1 and it's spectrum")
    os2 = opti_sum(*cross_section2, **window(*cross_section2))
    snr_opti_sum = window(os1, os2)
    # Visualizing
    first_snr = window(*cross_section1)
    show(first_snr["0"], first_snr["1"], fig_label="SNR's of signal_1, signal_2")
    show(*cross_section1, fig_label="Time domain")
    show(*w_cross_section1, fig_label="Frequency domain")
    show(s1, os1, fig_label="Sum's of cross section 1")
    show(s2, os2, fig_label="Sum's of cross section 2")
    show(snr_non_opti_sum["0"], snr_opti_sum["0"], snr_non_opti_sum["1"], snr_opti_sum["1"], fig_label="SNR's")
    # show(*(cross_section1+cross_section2))