from main import *
import Seismic_data as sd

if __name__ == '__main__':
    filename = r'C:\\Users\\oplor\\Desktop\\line1x1.su'
    st = sd.Read(filename, unpack_trace_headers=True)
    # ftt = sd.get_trace(st, 0, 2)  # ftt - first three traces
    ftt = st
    traces_values = sd.rough_data(ftt)
    # f_trace_0 = [abs(v) for v in fourier_shift(traces_values[0], domain='f')]
    # show(f_trace_0, fig_label="First signal spectrum")
    # show(*ftt, fig_label="Without noise")
    for el in traces_values:
        add_noise(el)
    # show(*ftt, fig_label="With noise")
    # snr_0_1 = window(traces_values[0], traces_values[1], width=len(traces_values[0]))
    # snr_1_2 = window(traces_values[1], traces_values[2], width=len(traces_values[0]))
    # show(snr_0_1["0"], snr_0_1["1"], snr_1_2["0"], snr_1_2["1"], fig_label="SNR 0, SNR 1 (0-1)\nSNR 1 (1-2), SNR 2")
    # show(snr_0_1["1"], snr_1_2["0"], mode="comb")

    wide = len(traces_values[0])
    snr = window(*traces_values, width=150)
    k = 0
    while k <= len(st):
        # show(snr["{}".format(str(k))], snr["{}".format(str(k+1))], fig_label="SNR {0} - {1}".format(str(k), str(k+1)))
        show(snr[1]["{}".format(str(k))], snr[0]["{}".format(str(k))], mode='comb', fig_label="SNR left right {}".format(str(k)))
        k += 1