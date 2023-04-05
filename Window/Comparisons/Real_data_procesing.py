# import libimp
from ops import *
from Class_monitor import show
import seismic_data_reader as sd

# KEYS
offset = 'distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group'
ogt = 'ensemble_number'

if __name__ == '__main__':

    # FILE NAMES
    clear = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear.su'
    clear_noise = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear-noise.su'

    # STREAMS
    st_c = sd.Read(clear, unpack_trace_headers=True)
    st_cn = sd.Read(clear_noise, unpack_trace_headers=True)

    str_st = sd.new_stream()
    opti_st = sd.new_stream()

    # PROCESSING
    ogt_values = sd.minmax_key_val(st_c, ogt)
    min_ogt = ogt_values[0]
    max_ogt = ogt_values[1]
    for num in range(min_ogt, max_ogt + 1):
        # SORTING STREAMS BY KEYS
        ogt_number = num
        st_c_ogt_sorted = sd.get_substream(st_c, ogt, ogt_number)
        ST_C = sd.sort(st_c_ogt_sorted, offset)
        st_cn_ogt_sorted = sd.get_substream(st_cn, ogt, ogt_number)
        ST_CN = sd.sort(st_cn_ogt_sorted, offset)

        # INITIAL TRACES PARAMETERS
        c_values = sd.rough_data(ST_C)
        cn_values = sd.rough_data(ST_CN)

        # VISUALISING DATA
        show(*c_values, mode='comb', shift=min_ogt,
             dist=1, color='b', fig_label="Сейсмограмма ОГТ №{} без шума".format(str(num)))
        show(*cn_values, mode='comb', shift=min_ogt,
             dist=1, color='b', fig_label="Сейсмограмма ОГТ №{} с шумом".format(str(num)))

        # PROCESSING DATA
        st = [ST_C, ST_CN]
        st_values = [c_values, cn_values]

        # SNR_C = window(*c_values)[2]
        # SNR_CN = window(*cn_values)[2]
        # for i in range(len(SNR_C)):
        #     j = str(i)
        #     show(SNR_C[j], SNR_CN[j], mode='comb', fig_label='0 - SNR чистого сигнала\n1 - SNR зашумленного сигнала')
        str_st += sd.straight_stream(*st)
        opti_st += sd.opti_stream(*st)

    show(sd.rough_data(opti_st))
    # SAVING
    # opti_st.write('Optimal_sum.su', format='SU')
    # str_st.write('Straight_sum.su', format='SU')


