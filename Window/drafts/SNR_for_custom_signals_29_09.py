import sys

from ops import *

def make_seismogramm(signal, trace_amount, noise_mode, stand_dev, relative_shift_range):
    """
    :param noise_mode: same, diff, None
    :return: array
    """
    signal_with_noise = []
    noise = []
    Spec_sig = []
    Spec_noise = []
    for i in range(trace_amount):
        temp = signal.copy()
        if noise_mode == "diff":
            add_noise(temp, stand_dev=stand_dev)

        noise.append(temp-signal)
        Spectrum_signal =[abs(S) for S in fourier_shift(signal, domain='f')]
        Spec_sig.append(Spectrum_signal)
        Spectrum_noise = [abs(S) for S in fourier_shift(temp - signal, domain='f')]
        Spec_noise.append(Spectrum_noise)


        if isinstance(relative_shift_range, list) and len(relative_shift_range) == 2:
            shift = random.uniform(relative_shift_range[0], relative_shift_range[1])
            temp = fourier_shift(temp, shift)

        signal_with_noise.append(temp)
        del temp
    return [signal_with_noise, noise, Spec_sig, Spec_noise]

def show_signal_and_noise(*values, pure_signal, fig_label=None):
    amount_of_plots = len(values)
    # plt.plot(range(len(pure_signal)), pure_signal, label="Сигнал")
    # for i in range(amount_of_plots):
    #     plt.plot(range(len(values[i])), values[i], label=str(i)+" - шум")
    # plt.legend()
    # plt.title('{}'.format(str(fig_label)), fontsize=10)
    # plt.show()
    fig, axes = plt.subplots(nrows=amount_of_plots, ncols=1)
    if amount_of_plots == 1:
        axes.plot(range(len(pure_signal)), pure_signal)
    else:
        for i in range(1, amount_of_plots):
            axes[0].plot(range(len(pure_signal)), pure_signal)
            axes[i].plot(range(len(values[i])), values[i] - pure_signal, label=str(i)+" - шум")
            # axes[i].set(title='Graph {}'.format(str(i)))
    fig.suptitle('{}'.format(str(fig_label)), fontsize=10)
    plt.show()

if __name__ == '__main__':
    counts = 150

    delta = np.zeros(counts)
    delta[74] = 40
    bpf = bpf(0.1, 3, counts)
    signal = np.convolve(delta, bpf, mode='same')

    # # Seismogramm 1
    # ta = 10 # trace amount
    # sd = 1 # standard deviation
    # rrs = [-10,10] # range of relative shift between neighbouring traces
    # DATA = make_seismogramm(signal, ta, 'diff', sd, rrs)
    # akf_vkf_coef = window(*DATA[0])
    # for j in range(len(DATA[0])):
    #     show(signal, DATA[1][j], fig_label="Сигнал и шум")  # signal and noise (1)
    #     show(DATA[0][j], fig_label="Их сумма")  # signal (2)
    #     show(DATA[2][j], DATA[3][j], fig_label="Спектры сигнала и шума")  # spectrums (3)
    #     show(akf_vkf_coef[0][j], akf_vkf_coef[1][j], mode='comb', fig_label="Автокорреляционная и\nвзаимнокорреляционная ф-ии") # AKF VKF (4)
    #     Spectrum_akf = [abs(S) for S in fourier_shift(akf_vkf_coef[0][j], domain='f')]
    #     Spectrum_vkf = [abs(S) for S in fourier_shift(akf_vkf_coef[1][j], domain='f')]
    #     show(Spectrum_akf, Spectrum_vkf, fig_label="Спектры АКФ и ВКФ")  # spectrums (5)
    #
    # # Seismogramm 2
    # ta = 10  # trace amount
    # sd = 0.1  # standard deviation
    # rrs = [-10, 10]  # range of relative shift between neighbouring traces
    # SM_2 = make_seismogramm(signal, ta, 'diff', sd, rrs)

    # bpf = bpf(0.1, 3, counts)  # band-pass filter
    # bpf_s = bpf(0.1, 3, counts)  # band-pass filter with w1=0.5 and w2=1

    signal_10 = np.convolve(delta, bpf, mode='same')
    signal_11 = signal_10.copy()
    signal_20 = np.convolve(delta, bpf, mode='same')
    signal_21 = signal_20.copy()

    s_d = 0
    add_noise(signal_10, stand_dev=s_d)
    add_noise(signal_11, stand_dev=s_d)
    s_d = 5
    add_noise(signal_20, stand_dev=s_d)
    add_noise(signal_21, stand_dev=s_d)

    S_0 = [signal_10, signal_20]
    S_1 = [signal_11, signal_21]

    # Выделение трасс с одинковыми номерами

    T_1 = [signal_10, signal_11]
    T_2 = [signal_20, signal_21]

    # Прямые суммы и их отношение сигнал/шум

    str_s_0 = straight_sum(*S_0)
    str_s_1 = straight_sum(*S_1)
    SNR_of_straight_sum = window(str_s_0, str_s_1)[2]

    # str_t_1 = straight_sum(*T_1)
    # str_t_2 = straight_sum(*T_2)
    # SNR_of_straight_sum = window(str_t_1, str_t_2)[2]

    # Оптимальные суммы и их отношение сигнал/шум

    # os_12_0 = opti_sum(*S_10_20, **(window(*S_10_20)[2]))
    os_0 = optis(S_0) # Оптимальная сумма первого набора
    # os_12_0 = opti_sum(*S_10_20, **(window(*S_10_20)[2]))
    os_1 = optis(S_1) # Оптимальная сумма второго набора
    SNR_of_opti_sum = window(os_0, os_1)[2]

    # os_1 = optis(T_1)  # Оптимальная сумма первого набора
    # os_2 = optis(T_2)  # Оптимальная сумма второго набора
    # SNR_of_opti_sum = window(os_1, os_2)[2]

    # Визуализация полученных отношений сигнал/шум

    label = "Отношение сигнал/шум для \n 0 - оптимальной суммы оптимальных сумм,\n 1 - прямой суммы прямых сумм \n Набор {}"
    color_trace_10, color_trace_20 = '#8C0000', '#00008B'
    color_trace_11, color_trace_21 = '#F00000', '#0343DF'
    color_S_0 = [color_trace_10, color_trace_20]
    color_S_1 = [color_trace_11, color_trace_21]
    color_T_1 = [color_trace_10, color_trace_11]
    color_T_2 = [color_trace_20, color_trace_21]

    show(*S_0, fig_label="Набор 1 исходных сигналов", color=color_S_0)
    show(str_s_0, os_0, fig_label="Прямая и оптимальная суммы трасс\nнабора 1", color=color_S_0)
    show(*S_1, fig_label="Набор 2 исходных сигналов", color=color_S_1)
    show(str_s_1, os_1, fig_label="Прямая и оптимальная суммы трасс\nнабора 2", color=color_S_1)
    # show(*T_1, fig_label="Первые трассы", color=color_T_1)
    show(SNR_of_opti_sum["0"], SNR_of_straight_sum["0"], fig_label=label.format("1"), mode='comb')
    # show(*T_2, fig_label="Вторые трассы", color=color_T_2)
    show(SNR_of_opti_sum["1"], SNR_of_straight_sum["1"], fig_label=label.format("2"), mode='comb')