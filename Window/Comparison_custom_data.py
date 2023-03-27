from ops import *


def clone(signal, n_times, signal_list):
    for i in range(n_times):
        signal_list.append(signal.copy())
    return None


def messup(signal_list, stand_div):

    for sig in signal_list:
        add_noise(sig, stand_dev=stand_div)
    return None


def sort(*seismogramms):
    sorted_list = []
    traces_same_position = []
    for i in range(len(seismogramms[0])):
        for ogt in seismogramms:
            traces_same_position.append(ogt[i])
        sorted_list.append(traces_same_position)
        traces_same_position = []
    return sorted_list


def seism_rand_noise(signals_amount=1, signal_to_clone=None, dist_range=None, seism_len=1):
    if dist_range is None:
        dist_range = [0, 1]
    res_seism = []
    temp_seism = []
    for _ in range(signals_amount):
        # temp_seism.append(signal_to_clone.copy())
        clone(signal_to_clone.copy(), n_times=seism_len, signal_list=temp_seism)
        s_d = random.uniform(dist_range[0], dist_range[1])
        messup(temp_seism, s_d)
        res_seism.append(temp_seism)
        temp_seism = []
    return res_seism


def OPS(*seismogramms):
    """Makes optimal OGT"""
    sorted_traces = sort(*seismogramms)
    optimal_OGT = []
    for traces in sorted_traces:
        optimal_trace = optis(traces)
        optimal_OGT.append(optimal_trace)
    return optimal_OGT


def SS(*seismogramms):
    """Just straight sum"""
    sorted_traces = sort(*seismogramms)
    straight_OGT = []
    for traces in sorted_traces:
        straight_trace = straight_sum(*traces)
        straight_OGT.append(straight_trace)
    return straight_OGT


if __name__ == '__main__':
    frequency = 3
    counts = 200
    all_counts = frequency * counts
    pi = np.pi
    # Signal component parameters

    bpf_1 = bpf(pi/7, 1*pi/3, counts, freq=frequency, show=False)
    # bpf_1 = bpf(0.1, 3, counts, freq=frequency)
    bpf_2 = bpf(pi/6, 1*pi/5, counts, freq=frequency)
    # bpf_2 = bpf_1
    delta_1 = np.zeros(all_counts)
    delta_1[int(all_counts / 2) - 1] = 20
    delta_2 = np.zeros(all_counts)
    delta_2[int(all_counts / 2) - 1] = 30
    # delta_2 = delta_1
    signals_components = []

    # Macro-parameters
    SEISMOGRAMM_SIZE = 3
    SEISMOGRAMM_AMOUNT = 20
    REF_INDEXES = [ind*frequency for ind in [13, 49, 68, 111, 156]]
    REF_VALUES = [0.3876, -0.7896, 0.5431, -0.1011, 0.98]
    GEOREF = geo_reflect(all_counts, REF_INDEXES, REF_VALUES) # Reflectance area
    # First seismogramm
    seismogramm_1 = []
    la = ["Время, мс", "Амплитуда, мВ"]
    signal_1 = np.convolve(delta_1, bpf_1, mode='same') # Pure signal
    # show(signal_1, together=True, label=la, fig_label="Сигнальная компонента")
    # show(delta_1, together=True, label=la, fig_label="Дельта-импульс")

    signal_1 = np.convolve(signal_1, GEOREF, mode='same') # Signal component
    signals_components.append(signal_1) # Saving signal component for visualisation
    clone(signal_1, SEISMOGRAMM_SIZE, seismogramm_1)
    messup(seismogramm_1, 2) # Adds noise

    # Second seismogramm
    seismogramm_2 = []
    signal_2 = np.convolve(delta_2, bpf_2, mode='same')
    # show(signal_2)
    signal_2 = np.convolve(signal_2, GEOREF, mode='same')
    # signal_2 = signal_1
    signals_components.append(signal_2)
    clone(signal_2, SEISMOGRAMM_SIZE, seismogramm_2)
    messup(seismogramm_2, 3)

    # Processing
    seismogramms = [seismogramm_1, seismogramm_2] # Set of seismogramms
    # seismogramms = seism_rand_noise(signals_amount=20, signal_to_clone=signal_1, dist_range=[1, 4],seism_len=2) # Set of seismogramms
    S_T = sort(*seismogramms) # Set of traces, sorted by their position in relevant seismogramm
    optimal_OGT = OPS(*seismogramms)
    straight_OGT = SS(*seismogramms)
    SNR_optimal = window(*optimal_OGT)[3]
    SNR_straight = window(*straight_OGT)[3]
    print(len(SNR_straight))


    # Visualisation
    def color_scale(*colors):
        """Just to paint corresponding traces (with same position in different seismogramms)"""
        scale = []
        for color in colors:
            scale.append(color[0])
        return scale


    # Macro-parameters
    tog = True
    skip = True
    skip_SEISM = False
    skip_SNR = False
    skip_GR = True
    skip_SamT = True
    skip_SC = True
    GR_lab = ["Глубина, м", ""]
    tr_lab = ["Время, мс", "Амплитуда, мВ"]
    SNR_lab = ["Частота, Гц", "Процент, %"]
    # Colors
    colors = []
    color_1 = ["b"] * SEISMOGRAMM_SIZE
    colors.append(color_1)
    color_2 = ["r"] * SEISMOGRAMM_SIZE
    colors.append(color_2)
    color_optimal = ["g"] * SEISMOGRAMM_SIZE
    colors.append(color_optimal)
    color_straight = ["y"] * SEISMOGRAMM_SIZE
    colors.append(color_straight)
    scale = color_scale(*colors)

    # colors = None
    # scale = None
    # color_1 = None
    # color_2 = None
    # color_straight = None
    # color_optimal = None
    # Essentials
    show(GEOREF, skip=skip_GR, together=tog,
         fig_label="Отражательная способность среды", color=color_1, label=GR_lab)
    # Signal component
    comp_leg = ["Сейсмограммы №{}".format(str(i+1)) for i in range(len(seismogramms))]
    show(*signals_components, skip=skip_SC, together=tog,
         fig_label="Сигнальные компоненты", legend=comp_leg, color=scale, label=tr_lab)
    # SEISMOGRAMMS
    for i, seism in enumerate(seismogramms):
        show(*seism, skip=skip_SEISM, together=tog,
             fig_label="Сейсмограмма №{}".format(str(i)), color=color_1, label=tr_lab)
    # show(*seismogramm_1, skip=skip_SEISM, together=tog,
    #      fig_label="Сейсмограмма №1", color=color_1, label=tr_lab)
    # show(*seismogramm_2, skip=skip_SEISM, together=tog,
    #      fig_label="Сейсмограмма №2", color=color_2, label=tr_lab)
    # # TRACES WITH THE SAME POSITIONS
    # for i in range(SEISMOGRAMM_SIZE):
    #     show(*S_T[i], skip=skip_SamT, together=tog,
    #          fig_label="Трассы с позицией №{}\nв сейсмограммах".format(str(i+1)), color=scale, label=tr_lab)
    # PROCESSED SEISMOGRAMMS
    show(*optimal_OGT, skip=skip, together=tog, 
         fig_label="Оптимальная сейсмограмма", color=color_optimal, label=tr_lab)
    show(*straight_OGT, skip=skip, together=tog, 
         fig_label="Просуммированная сейсмограмма", color=color_straight, label=tr_lab)
    # Signal/noise rates
    legend = ["Оптимальная", "Прямая"]
    # for i in range(SEISMOGRAMM_SIZE):
    for i in range(len(seismogramms[0])):
        # SNR = [SNR_optimal[i], SNR_straight[i]]
        SNR = [SNR_optimal[i][:int(counts/2)], SNR_straight[i][:int(counts/2)]]
        show(*SNR, skip=skip_SNR, together=tog, mode="comb",
             fig_label="Отношение сигнал/помеха для трассы №{}".format(str(i+1)),  legend=legend, label=SNR_lab)
        # plt.show()
    plt.show()
