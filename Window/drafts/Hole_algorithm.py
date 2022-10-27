from main import *

if __name__ == '__main__':
    # counts = 150
    #
    # delta = np.zeros(counts)
    # delta[74] = 40
    #
    # bpf_w = bpf(0.2, 3, counts)  # band-pass filter with w1=0.2 and w2=3
    # bpf_s = bpf(0.1, 1, counts)  # band-pass filter with w1=0.5 and w2=1
    #
    # signal_1 = np.convolve(delta, bpf_w, mode='same')
    # signal_11 = signal_1.copy()
    # signal_2 = np.convolve(delta, bpf_s, mode='same')
    # signal_21 = signal_2.copy()
    #
    # s_d = 0.1
    # add_noise(signal_1, stand_dev=s_d)
    # add_noise(signal_11, stand_dev=s_d)
    # add_noise(signal_2, stand_dev=s_d)
    # add_noise(signal_21, stand_dev=s_d)
    #
    # snr1 = window(signal_1, signal_11)
    # snr2 = window(signal_2, signal_21)
    #
    # sums = straight_sum(signal_1, signal_2)
    # signal = [signal_1, signal_2]
    # snr = {}
    # snr.update({"0": snr1.get("0"), "1": snr2.get("0")})
    # sum_1 = opti_sum(*signal, **snr)
    #
    # sums_3 = straight_sum(signal_11, signal_21)
    # snr_3 = {}
    # snr_3.update({"0": snr1.get("1"), "1": snr2.get("1")})
    # signal_3 = [signal_11, signal_21]
    # sum_3 = opti_sum(*signal_3, **snr_3)
    #
    # SUMS = straight_sum(sums, sums_3)
    # SNR_SUMS = window(sums, sums_3)
    #
    # SIGNAL = [sum_1, sum_3]
    # SNR = window(*SIGNAL)
    # SUM = opti_sum(*SIGNAL, **SNR)
    # """ Spectrum """
    # ws1 = [abs(v) for v in fourier_shift(signal_1, domain='f')]
    # ws2 = [abs(v) for v in fourier_shift(signal_2, domain='f')]
    # ws11 = [abs(v) for v in fourier_shift(signal_11, domain='f')]
    # ws21 = [abs(v) for v in fourier_shift(signal_21, domain='f')]
    # wss1 = [abs(v) for v in fourier_shift(sum_1, domain='f')]
    # wss2 = [abs(v) for v in fourier_shift(sum_3, domain='f')]
    # wsums = [abs(v) for v in fourier_shift(sums, domain='f')]
    # wsums_3 = [abs(v) for v in fourier_shift(sums_3, domain='f')]
    # WSUMS = [abs(v) for v in fourier_shift(SUMS, domain='f')]
    # m1 = max(wsums)
    # # wsums = [v / m1 for v in wsums]
    # wos = [abs(v) for v in fourier_shift(sum_1, domain='f')]
    # wos_3 = [abs(v) for v in fourier_shift(sum_3, domain='f')]
    # WOS = [abs(v) for v in fourier_shift(SUM, domain='f')]
    # # m1 = max(wos)
    # # wos = [v / m1 for v in wos]
    # """ Monitor """
    # # show(signal_1, ws1, fig_label="Signal 1 and it's spectrum")
    # # show(snr1["0"], ws1, fig_label="SNR 1")
    # # show(snr2["0"], ws2, fig_label="SNR 2")
    # # # show(ws1, ws2)
    # # # show(sums, wsums)
    # # show(sum_1, sums, wos, wsums, fig_label="First pair")
    # #
    # # show(snr_3["0"], ws11, fig_label="SNR 11")
    # # show(snr_3["1"], ws21, fig_label="SNR 21")
    # # show(sum_3, sums_3, wos_3, wsums_3, fig_label="Second pair")
    #
    # show(SNR_SUMS["0"], wsums, fig_label="SNR straight 1 + spectrum")
    # show(SNR_SUMS["1"], wsums_3, fig_label="SNR straight 2 + spectrum")
    #
    # show(SNR["0"], wss1, fig_label="SNR opti 1")
    # show(SNR["1"], wss2, fig_label="SNR opti 2")
    # # show(SUM, SUMS, WOS, WSUMS, fig_label="Opti-opti, straight-straight")
    #

    print(random.uniform(-4,3))
    exit(1)

    counts = int(600 / 4)

    delta_1 = np.zeros(counts)  # δ-impulse with pick at 74
    delta_1[int(296 / 4)] = 40
    # show(delta_1)

    bpf_1 = bpf(0.2, 3, counts)  # band-pass filter with w1=0.2 and w2=3
    bpf_2 = bpf(0.1, 1, counts)  # band-pass filter with w1=0.5 and w2=1

    shift_t = 10

    signal_1 = np.convolve(delta_1, bpf_1)
    signal_11 = fourier_shift(signal_1.copy(), shift_t)

    signal_2 = np.convolve(delta_1, bpf_2)
    signal_21 = fourier_shift(signal_2.copy(), shift_t)
    # show(signal_1, signal_11)

    """Noise"""
    s_d = 10
    # add_noise(signal_1, stand_dev=s_d)
    # add_noise(signal_11, stand_dev=s_d)
    # add_noise(signal_2, stand_dev=s_d)
    # add_noise(signal_21, stand_dev=s_d)

    """ Opti sum checking"""

    # OCCURS TROUBLE WITH SNR AND TRACE LENGTH. SNR LENGTH = WINDOW WIDTH, BUT TRACE LENGTH != WINDOW WIDTH
    # snr1 = window(signal_1, signal_11)
    # # # print(len(snr1["0"]))
    # signals = [signal_1, signal_11]
    # b = opti_sum(*signals, **snr1)
    # show(*signals)
    # show(b)
    # print(len(snr1["0"]))

    snr1 = window(signal_1, signal_11)
    sig1 = [signal_1, signal_2]
    snr2 = window(signal_2, signal_21)
    sig2 = [signal_11, signal_21]

    # snr1.update({"1": snr2.get("0")})
    # snr2.update({"0": snr1.get("0")})

    # show(snr2["1"])
    # show(snr1["0"], snr1["1"], snr2["0"], snr2["1"])
    # show(snr1.values())
    # show(*sig2)
    # for i in ["0", "1"]:
    #     snr1[i] = [value / max(snr1[i]) for value in snr1[i]]
    #     snr2[i] = [value / max(snr2[i]) for value in snr2[i]]
    show(signal_1, signal_11)
    show(snr1["0"], snr1["1"], fig_label="SNR_1")
    for i in ["0", "1"]:
        snr1[i] = [abs(value) for value in fourier_shift(snr1, domain='f')]
        snr2[i] = [abs(value) for value in fourier_shift(snr2, domain='f')]

    os1 = opti_sum(*sig1, **snr1)
    os2 = opti_sum(*sig2, **snr2)

    # show(signal_1, os1, signal_2, os2)
    show(signal_1, os1, bpf_1)
    # show(os2)
    os_snr = window(os1, os2)
    # show(snr1["0"], snr2["1"], os_snr["0"], os_snr["1"])
    # os_sig = [os1, os2]
    # the_os = opti_sum(*os_sig, **os_snr)

    first = [signal_1, signal_11]
    second = [signal_2, signal_21]

    snr1_to_compare = window(*first)
    snr2_to_compare = window(*second)
