# import libimp
from ops import *
import source_data as sd
from numpy import pi, abs, mean
from source_data import *
from monitor import show
from scipy.signal import correlate
import copy_ops as testing


# MACRO-PARAMETERS

SEISMIC_SOURCES = 3 # Amount of traces in image
# SEISMOGRAMM_AMOUNT = 20
GEO_LAYERS = 5 # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 0 # Measure of layer falling speed. Shows how fast do they fall


if __name__ == '__main__':

    # SIGNAL COMPONENT PARAMETERS

    b1 = band_pass_filter(pi / 3, 2 * pi / 2, show=False)
    b2 = band_pass_filter(pi / 4, 2 * pi / 3)

    w1 = wave(b1, amplitude=40)
    w2 = wave(b2, amplitude=20)

    # Noises
    n1 = 2
    n2 = 3

    # Reflectivity in general for area
    AR = area_reflectivity(GEO_LAYERS, SEISMIC_SOURCES, shift=HIGHT_DIFFERENCES)

    # SEISMIC IMAGES
    si1 = seismic_image(AR, w1, n1)
    si2 = seismic_image(AR, w2, n2)


    #PROCESSING
    # a = testing.window(*si1)
    images = [si1, si2]  # Set of seismogramms
    # a = testing.window(*images)
    # optimal_OGT = OPS(*images)
    # straight_OGT = SS(*images)
    # SNR_optimal = window(*optimal_OGT)[3]
    # SNR_straight = window(*straight_OGT)[3]



    # VISUALISATION
    # f_b1 = np.fft.rfft(b1,n=ALL_COUNTS, norm=fourier_normalization)
    # signal_rate = np.asarray([abs(value) for value in f_b1])
    # show(signal_rate, fig_title='Furier bpf')

    # show(*[correlate(b1,b1), correlate(f_b1,f_b1)],color=['b','r'])
    # snr_legend = 'Красная - оптимальная\nЧерная - прямая'
    # # show(*si1)
    # # show(*si2)
    # # tog = True
    # # show(*optimal_OGT, with_next=tog,
    # #      fig_title="Оптимальная сейсмограмма")
    # # show(*straight_OGT,
    # #      fig_title="Просуммированная сейсмограмма")
    # for i in range(len(images[0])):
    #     # SNR = [SNR_optimal[i], SNR_straight[i]]
    #     SNR = [SNR_optimal[i][:int(COUNTS/2)], SNR_straight[i][:int(COUNTS/2)]]
    #     show(*SNR, mode='comb', color=['r','k'], legend=snr_legend)
    # show(*si1)
    # for snr in testing.window(*si1):
    #     show(snr)

    W1 = seismic_image(AR, w1)
    #
    # # t1 = W1[0]
    # # f_t1 = np.fft.rfft(t1, n=ALL_COUNTS, norm=fourier_normalization)
    # # t1 = np.fft.irfft(f_t1, n=ALL_COUNTS, norm=fourier_normalization)
    # # signal_rate = np.asarray([abs(value) for value in f_t1])
    # # show(signal_rate, fig_title='Furier si1')
    # # show(t1)
    # show(AR[0], w1, W1[0])
    # r, s = AR[0], w1
    # # print(len(t1), ALL_COUNTS,sep='|')
    # f_r = np.fft.rfft(r, n=ALL_COUNTS, norm=fourier_normalization)
    # f_s = np.fft.rfft(s, n=ALL_COUNTS, norm=fourier_normalization)
    # r = np.fft.irfft(f_r, n=ALL_COUNTS, norm=fourier_normalization)
    # s = np.fft.irfft(f_s, n=ALL_COUNTS, norm=fourier_normalization)
    # signal_rate = [np.asarray([abs(value) for value in f_r]), np.asarray([abs(value) for value in f_s])]
    # show(*signal_rate, fig_title='Furier')
    # show(s)

    # # show(*W1)
    # for snr in testing.window(*W1):
    #     show(snr)
    processed_image = testing.optimal_filter(*si1)
    processed_pure_image = testing.optimal_filter(*W1)
    show(*W1, fig_title='Чистое (эталонное) изображение', with_next=True)
    show(*si1, fig_title='Обрабатываемое изображение', with_next=True)

    # W1_snr = testing.window(*W1)
    # Filtered_snr = testing.window(*si1)
    show(*processed_pure_image, fig_title='Отфильтрованное чистое изображение', with_next=True)
    show(*processed_image, fig_title='Отфильтрованное изображение', with_next=True)
    show(mean(processed_image,axis=0))
    # # for i, trace in enumerate(W1):
    #     processed_trace = processed_image[i]
    #     # show(processed_image[i], fig_title='Отфильтрованное изображение', with_next=True)
    #     show(trace, processed_trace, mode='comb', fig_title='Сравнение эталонной \nи отфильтрованной трассы', with_next=True)
    #     show(W1_snr[i], Filtered_snr[i], mode='comb', fig_title='Сравнение эталонной \nи отфильтрованной трассы')


