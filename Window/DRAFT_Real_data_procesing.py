import re

from ops import *
import Seismic_data as sd


def from_get(ar, index, fig_label=False):
    akf = ar[0][index]
    f_akf = [abs(v) for v in fourier_shift(akf, domain='f')]
    vkf = ar[1][index]
    f_vkf = [abs(v) for v in fourier_shift(vkf, domain='f')]
    if index < 0:
        index += len(ar[0])
    snr = ar[2][str(index)]
    return [akf, f_akf, vkf, f_vkf, snr] #if not fig_label else [akf, f_akf, vkf, f_vkf, snr, "AKF_t, AKF_w\nVKF_t, VKF_w\nSNR"]


if __name__ == '__main__':

    # KEYS
    offset = 'distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group'
    ogt = 'ensemble_number'

    # FILE NAME
    clear = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear.su'
    clear_noise = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear-noise.su'
    clear_wide = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear-wide.su'
    clear_wide_noise = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear-wide-noise.su'

    # STREAMS
    st_c = sd.Read(clear, unpack_trace_headers=True)
    st_cn = sd.Read(clear_noise, unpack_trace_headers=True)
    st_cw = sd.Read(clear_wide, unpack_trace_headers=True)
    st_cwn = sd.Read(clear_wide_noise, unpack_trace_headers=True)
    # for i in range(len(st_c)):
    #     for j in range(len(st_c[i])):
    #         if sd.rough_data(st_cn)[i][j] != sd.rough_data(st_cwn)[i][j]:
    #             print(i)
    #             print(sd.rough_data(st_cn)[i][j],', ', sd.rough_data(st_cwn)[i][j])
    #             show(sd.rough_data(st_cn)[i], sd.rough_data(st_cwn)[i])

    # SORTING STREAMS BY KEYS
    ogt_number = 1
    st_c_ogt_sorted = sd.get_substream(st_c, ogt, ogt_number)
    ST_C = sd.sort(st_c_ogt_sorted, offset)
    st_cn_ogt_sorted = sd.get_substream(st_cn, ogt, ogt_number)
    ST_CN = sd.sort(st_cn_ogt_sorted, offset)
    st_cw_ogt_sorted = sd.get_substream(st_cw, ogt, ogt_number)
    ST_CW = sd.sort(st_cw_ogt_sorted, offset)
    st_cwn_ogt_sorted = sd.get_substream(st_cwn, ogt, ogt_number)
    ST_CWN = sd.sort(st_cwn_ogt_sorted, offset)

    # INITIAL TRACES PARAMETERS
    c_values = sd.rough_data(ST_C)
    # c_processed_data = window(*c_values, width=len(c_values[0]))
    # # c_akf = c_processed_data[0]
    # # c_vkf = c_processed_data[1]
    # c_snr = c_processed_data[2]
    #
    # # for i in range(len(ST_C)):
    # #     show(c_akf[i], c_vkf[i], c_snr["0"])
    # # show(*from_get(c_processed_data, -1), fig_label="AKF_t, AKF_w\nVKF_t, VKF_w\nSNR")
    #
    cn_values = sd.rough_data(ST_CN)
    # cn_processed_data = window(*cn_values, width=len(cn_values[0]))
    # # cn_akf = cn_processed_data[0]
    # # cn_vkf = cn_processed_data[1]
    # cn_snr = cn_processed_data[2]
    #
    cw_values = sd.rough_data(ST_CW)
    # cw_processed_data = window(*cw_values, width=len(cw_values[0]))
    # # cw_akf = cw_processed_data[0]
    # # cw_vkf = cw_processed_data[1]
    # cw_snr = cw_processed_data[2]
    #
    cwn_values = sd.rough_data(ST_CWN)
    # cwn_processed_data = window(*cwn_values, width=len(cwn_values[0]))
    # # cwn_akf = cwn_processed_data[0]
    # # cwn_vkf = cwn_processed_data[1]
    # cwn_snr = cwn_processed_data[2]

    # for i in range(10):
    #     show(c_values[i], cw_values[i], cn_values[i], cwn_values[i], mode='comb')

    # PROCESSING DATA

    st = [ST_C, ST_CN]
    st_values = [c_values, cn_values]
    str_st = sd.straight_stream(*st)
    opti_st = sd.opti_stream(*st)

    # TESTING CODE

    # # str_st_values = sd.rough_data(str_st)
    # # opti_st_values = sd.rough_data(opti_st)
    # # print(len(str_st))
    # max_index = len(str_st) - 1
    # middle_index = int(max_index / 2)
    #
    # # number = 2
    # # sd.testing_code_show(*st, str_st=str_st, opti_st=opti_st, trace_index=0, label='Первая', test=number)
    # # sd.testing_code_show(*st, str_st=str_st, opti_st=opti_st, trace_index=middle_index, label='Средняя', test=number)
    # # sd.testing_code_show(*st, str_st=str_st, opti_st=opti_st, trace_index=max_index, label='Последняя', test=number)
    #
    # sd.testing_code_show(*st, str_st=str_st, opti_st=opti_st, trace_index=max_index, label='Последняя', test=3)
    #
    # # print("Data first:\n", c_values[0])
    # # print("Data last:\n", c_values[40])
    # # show(c_values[0],c_values[40], mode='comb')
    # # print("--------------------------------")
    # # print("Data first:\n", cn_values[0])
    # # print("Data last:\n", cn_values[40])
    # # show(cn_values[0], cn_values[40], mode='comb')

    # ___/ OLD CODE \___

    # c_cw_val = sd.rough_data(sd.combine(ST_C, ST_CW))
    # c_cw_processed_data = window(*c_cw_val, width=len(c_cw_val[0]))
    # c_cw_snr = c_cw_processed_data[2]
    #
    # C_CW_Basic_sum_trace = straight_sum(*c_values)

    # res1 = sd.process(ST_C, ST_CN)
    # basic_sum_1 = (res1[0])
    # opti_sum_1 = (res1[1])
    # snr = (res1[2])
    # for i in range(len(basic_sum_1)):
    #     show(basic_sum_1[i], ST_C[0], opti_sum_1[i], mode='comb', fig_label="Trace "+str(i)+"\nBasic sum (0)\nOpti sum (1)")
    #     show(basic_sum_1[i], opti_sum_1[i], fig_label="Basic sum\nOpti sum")
    #     show(snr[i]["0"], snr[i]["1"])



    # S_10_20 = [c_values[0], cn_values[0]]
    # S_11_21 = [c_values[1], cn_values[1]]
    # # S_10_20 = [c_values[0], cw_values[0]]
    # # S_11_21 = [c_values[1], cw_values[1]]
    # # print(S_10_20)
    # # print("----------------")
    # # print(S_11_21)
    # str_s_12_0 = straight_sum(*S_10_20)
    # str_s_12_1 = straight_sum(*S_11_21)
    # # print(str_s_12_0)
    # # print("**************************")
    # # print(str_s_12_1)
    # # show(str_s_12_0, c_values[0], cw_values[0])
    # # SNR_of_straight_sum = window(str_s_12_0, str_s_12_1)[2]
    # os_12_0 = opti_sum(*S_10_20, **(window(*S_10_20)[2]))
    # os_12_1 = opti_sum(*S_11_21, **(window(*S_11_21)[2]))
    # show(str_s_12_0, os_12_0, mode='comb', fig_label="STR\nOS")
    # show(str_s_12_1, os_12_1, mode='comb', fig_label="STR\nOS")
    # SNR_of_opti_sum = window(os_12_0, os_12_1)[2]
    # show(SNR_of_opti_sum["0"], SNR_of_straight_sum["0"], fig_label="SNR's: os1, ss1", mode='comb')
    # show(SNR_of_opti_sum["1"], SNR_of_straight_sum["1"], fig_label="SNR's: os2, ss2", mode='comb')

    # C_Basic_sum_trace = straight_sum(*c_values)
    # C_Opti_sum_trace = opti_sum(*c_values, **c_snr)
    # show(C_Basic_sum_trace, C_Opti_sum_trace)

    # CN_Basic_sum_trace = straight_sum(*cn_values)
    # CN_Opti_sum_trace = opti_sum(*cn_values, **cn_snr)
    # show(CN_Basic_sum_trace, CN_Opti_sum_trace)

    # CW_Basic_sum_trace = straight_sum(*cw_values)
    # CW_Opti_sum_trace = opti_sum(*cw_values, **cw_snr)
    # show(CW_Basic_sum_trace, CW_Opti_sum_trace)

    # CWN_Basic_sum_trace = straight_sum(*cwn_values)
    # CWN_Opti_sum_trace = opti_sum(*cwn_values, **cwn_snr)
    # show(CWN_Basic_sum_trace, CWN_Opti_sum_trace, mode='comb')
    # show(CWN_Basic_sum_trace, CWN_Opti_sum_trace)


