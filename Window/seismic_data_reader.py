import re
from ops import window, straight_sum, opti_sum, optis, fourier_shift, normalized_coefficients
from monitor import show
import numpy as np
import obspy
from obspy.core import read, UTCDateTime
from obspy.io.segy.core import _read_segy, _read_su, _is_su
from obspy.io.segy.segy import iread_su
from obspy.core.util import get_example_file


# https://ds.iris.edu/mda/ - meta-data
# http://ds.iris.edu/ds/nodes/dmc/data/formats/ - data formats
# https://web.mit.edu/cwpsu_v44r1/sumanual_600dpi_letter.pdf - SU info

# KEYS
offset = 'distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group'
ogt = 'ensemble_number'

def get_cdp(stream, number):
    if isinstance(stream, obspy.core.stream.Stream):
        for tr in stream:
            if tr.stats.su.trace_header.ensemble_number == number:
                return tr.data
        raise Exception("No trace with given cdp found in stream.")
        return None


def get_substream(stream, by_key, key_value):
    if isinstance(stream, obspy.core.stream.Stream):
        sub_stream = obspy.core.stream.Stream()
        for i in range(len(stream)):
            if stream[i].stats.su.trace_header.__getitem__(by_key) == key_value:
                sub_stream.append(stream[i])
        return sub_stream
    return None


def sort(stream, by_key):
    if isinstance(stream, obspy.core.stream.Stream):
        sorted_stream = obspy.core.stream.Stream(sorted(stream, key=lambda x: x.stats.su.trace_header[by_key]))
        return sorted_stream


def get_trace(stream, first_index, second_index=None):
    if isinstance(stream, obspy.core.stream.Stream):
        second_index = first_index if second_index is None else second_index
        if first_index not in range(len(stream)) or second_index not in range(
                len(stream)) or first_index > second_index:
            raise IndexError("Index out of range.")
        return obspy.core.stream.Stream([stream[i] for i in range(first_index, second_index + 1)])


def Read(filename, unpack_trace_headers=False):
    if _is_su(filename):
        return _read_su(filename, unpack_trace_headers=unpack_trace_headers)


def rough_data(stream):
    if isinstance(stream, obspy.core.stream.Stream):
        data = []
        for trace in stream:
            trace_values = np.asarray(trace.data)
            data.append(trace_values)
        return data
    else:
        return None


def find_in(stream, trace_num, attribute):
    if isinstance(stream, obspy.core.stream.Stream):
        header = str(stream[trace_num].stats.su.trace_header)
        for el in header.split(','):
            r = re.findall(str(attribute), el)
            if len(r):
                print(el)
    return None


def new_stream():
    return obspy.core.stream.Stream()


def head_atribute_value(stream, key):
    """ Returns all values by given key from stream"""
    if isinstance(stream, obspy.core.stream.Stream):
        key_values = []
        for tr in stream:
            key_values.append(tr.stats.su.trace_header.__getitem__(key))
        return key_values


def minmax_key_val(stream, key):
    if isinstance(stream, obspy.core.stream.Stream):
        key_val = head_atribute_value(stream, key)
        minmax = [key_val[0], key_val[0]]
        for val in key_val:
            if minmax[0] > val:
                minmax[0] = val
            if minmax[1] < val:
                minmax[1] = val
        return minmax


def process(stream1, stream2):
    if isinstance(stream1, obspy.core.stream.Stream) and isinstance(stream2, obspy.core.stream.Stream):
        if (len(stream1) != len(stream2)):
            raise ValueError("Streams have different lengths")
        else:
            trace_amount = len(stream1)
            Basic_sum = []
            Opti_sum = []
            snr = []
            for i in range(trace_amount):
                temp = []
                for st in [stream1, stream2]:
                    temp.append(st[i].data)
                Basic_sum.append(straight_sum(*temp))
                snr_i = window(*temp, width=len(temp[0]))[2]
                Opti_sum.append(opti_sum(*temp, **snr_i))
            for i in range(trace_amount):
                values = [stream1[i].data, stream2[i].data]
                snr_i = window(*values, width=len(stream1[0]))[2]
                snr.append(snr_i)
                Basic_sum.append(straight_sum(*values))
                Opti_sum.append(opti_sum(*values, **snr_i))
        return [Basic_sum, Opti_sum, snr]


def opti_stream(*stream_list):
    """ Makes stream of optimal summaries."""
    Opti_Stream = new_stream()
    trace_amount = len((stream_list[0]))
    offset = 'distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group'
    ogt = 'ensemble_number'
    for i in range(trace_amount):
        current_processing_traces = []
        current_offset = stream_list[0][i].stats.su.trace_header.__getitem__(offset)
        current_ogt = stream_list[0][i].stats.su.trace_header.__getitem__(ogt)
        for st in stream_list:
            current_processing_traces.append(np.asarray(st[i].data))
        opti_trace = obspy.core.trace.Trace(optis(current_processing_traces))
        opti_trace.stats.update(adict=stream_list[0][i].stats.copy())
        opti_trace.stats.su.update({offset: current_offset, ogt: current_ogt})
        Opti_Stream.append(opti_trace)
    return Opti_Stream


def straight_stream(*streams):
    """ Makes stream of straight summaries."""
    Str_Stream = new_stream()
    trace_amount = len((streams[0]))
    for i in range(trace_amount):
        current_processing_traces = []
        current_offset = streams[0][i].stats.su.trace_header.__getitem__(
            'distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group')
        current_ogt = streams[0][i].stats.su.trace_header.__getitem__('ensemble_number')
        for st in streams:
            current_processing_traces.append(np.asarray(st[i].data))
        straight_trace = obspy.core.trace.Trace(straight_sum(*current_processing_traces))
        straight_trace.stats.update(adict=streams[0][i].stats.copy())
        straight_trace.stats.su.update({'offset': current_offset, 'ogt': current_ogt})
        Str_Stream.append(straight_trace)
    return Str_Stream


def testing_code_show(*proc_streams, str_st, opti_st, trace_index, label, test=1):
    proc_st_val = []
    for st in proc_streams:
        proc_st_val.append(rough_data(st))
    str_st_val = rough_data(str_st)
    opti_st_val = rough_data(opti_st)
    freq_dom_str_st_val = [abs(v) for v in fourier_shift(str_st_val[trace_index], domain='f')]
    freq_dom_opti_st_val = [abs(v) for v in fourier_shift(opti_st_val[trace_index], domain='f')]
    traces_val_with_given_index = []
    those_traces_in_freq_domain = []
    for st_val in proc_st_val:
        st_val = np.asarray(st_val)
        traces_val_with_given_index.append(st_val[trace_index])
        those_traces_in_freq_domain.append([abs(v) for v in fourier_shift(st_val[trace_index], domain='f')])
    norm_coef = normalized_coefficients(**(window(*traces_val_with_given_index)[2]))
    for key in norm_coef.keys():
        print("Коэф-ты {} ".format(key), norm_coef[key])
    print("-------------------------------------------------------------------------------------------")
    if test == 1:
        # show(*traces_val_with_given_index, str_st_val[trace_index], opti_st_val[trace_index], mode='comb',
        #      fig_label="__{}__\nТрассы:\nПоследняя: opti_sum\nПредпоследняя: straight_sum\nДо этого - трассы, которые складывал".format(label))
        show(str_st_val[trace_index], opti_st_val[trace_index], mode='comb',
             fig_label="__{}__\nТрассы:\nПредпоследняя: straight_sum\nПоследняя: opti_sum".format(label))
        show(freq_dom_str_st_val, freq_dom_opti_st_val, mode='comb',
             fig_label="__{}__\nСпектры:\nПредпоследняя: straight_sum\nПоследняя: opti_sum".format(label))
        show(*traces_val_with_given_index, mode='comb', fig_label="__{}__\nСуммируемые трассы".format(label))
        show(*traces_val_with_given_index, str_st_val[trace_index], mode='comb',
             fig_label="__{}__\nСуммируемые трассы и прямая сумма в конце".format(label))
        show(*those_traces_in_freq_domain, mode='comb', fig_label="__{}__\nСпектры суммируемых трасс".format(label))
    elif test == 2:
        show(str_st_val[trace_index], opti_st_val[trace_index], proc_st_val[0][trace_index], mode='comb',
             fig_label="__{}__\nТрассы:\n0 - straight_sum\n1 - opti_sum\n2 - clear".format(label))
    elif test == 3:
        opti_SNR = window(opti_st_val[0], opti_st_val[trace_index])[2]
        str_SNR = window(str_st_val[0], str_st_val[trace_index])[2]
        for key in opti_SNR.keys():
            show(opti_SNR.get(key), str_SNR.get(key), mode='comb')
            print("SNR_OPTI:\n", opti_SNR(key))
            print("-------------------------------------")
            print("SNR_STRAIGHT:\n", str_SNR(key))


def combine(stream1, stream2):
    return stream1.__eq__(stream2)
    if isinstance(stream1, obspy.core.stream.Stream) and isinstance(stream2, obspy.core.stream.Stream):
        new_stream = obspy.core.stream.Stream()
        for i in range(len(stream1)):
            new_stream.append(stream1[i])
            new_stream.append(stream2[i])
        return new_stream
    else:
        print("ERROR")
        return None
