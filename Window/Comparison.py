import Seismic_data as sd
from ops import show


if __name__ == '__main__':

    optimal = r'S:\GEOLAB\Window\Optimal_sum.su'
    noisy = r'C:\Users\oplor\Desktop\Data_test\rudlan-clear-noise.su'
    
    # STREAMS
    st_o = sd.Read(optimal, unpack_trace_headers=True)
    st_n = sd.Read(noisy, unpack_trace_headers=True)

    str_st = sd.new_stream()
    opti_st = sd.new_stream()

    # PROCESSING
    ogt_values = sd.minmax_key_val(st_o, sd.ogt)
    min_ogt = ogt_values[0]
    max_ogt = ogt_values[1]
    for num in range(min_ogt, max_ogt + 1):
        # SORTING STREAMS BY KEYS
        ogt_number = num
        st_o_ogt_sorted = sd.get_substream(st_o, sd.ogt, ogt_number)
        ST_O = sd.sort(st_o_ogt_sorted, sd.offset)
        
        st_n_ogt_sorted = sd.get_substream(st_n, sd.ogt, ogt_number)
        ST_N = sd.sort(st_n_ogt_sorted, sd.offset)

        # INITIAL TRACES PARAMETERS
        o_values = sd.rough_data(ST_O)
        n_values = sd.rough_data(ST_N)

        # VISUALISING DATA
        show(*o_values, mode='comb', shift=min_ogt,
             dist=1, color='b', fig_label="Оптимальная ейсмограмма ОГТ №{}".format(str(num)))
        show(*n_values, mode='comb', shift=min_ogt,
             dist=1, color='b', fig_label="Сейсмограмма ОГТ №{} с шумом".format(str(num)))

