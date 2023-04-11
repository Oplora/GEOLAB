# import libimp
from ops import *
import source_data as sd
from numpy import pi, abs, mean
from source_data import *
from Class_monitor import Monitor
from scipy.signal import correlate
import copy_ops as testing
from Class_image import SeisImage

# MACRO-PARAMETERS

SEISMIC_SOURCES = 4 # Amount of traces in image
# SEISMOGRAMM_AMOUNT = 20
GEO_LAYERS = 5  # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 0  # Measure of layer falling speed. Shows how fast do they fall

if __name__ == '__main__':
    # SIGNAL COMPONENT PARAMETERS

    b1 = band_pass_filter(pi / 3, 1 * pi / 2, show=0)
    b2 = band_pass_filter(2 * pi / 3, 3 * pi / 4, show=0)

    w1 = wave(b1, amplitude=50)
    w2 = wave(b2, amplitude=20)

    # Noises
    n1 = 2.5
    n2 = 1

    # Reflectivity in general for area
    AR = area_reflectivity(GEO_LAYERS, SEISMIC_SOURCES, shift=HIGHT_DIFFERENCES)

    # SEISMIC IMAGES
    si1 = seismic_image(AR, w1, n1)
    si2 = seismic_image(AR, w2, n2)

    u1 = SeisImage(si1)
    u2 = SeisImage(si2)
    U = [u2, u1]

    # PROCESSING

    p_u1 = u1.optimal()
    p_u2 = u2.optimal()
    OU = SeisImage.MCOP(U)
    # # print(type(OU), OU.get_trace(), sep='\n')
    SU = mean(U, axis=0)


    # VISUALISATION

    u1.show(snr=0, with_next=1, fig_title='First image')
    u2.show(snr=0, with_next=1, fig_title='Second image')
    u2.show(snr=1, with_next=1, fig_title='Second image')
    #
    # p_u1.show(snr=1, fig_title='Optimal first image', with_next=1)
    # SeisImage.optimal(p_u2).show(snr=0, fig_title='Optimal optimal second image', with_next=1)
    # p_u2.show(snr=0, fig_title='Optimal second image', with_next=1)
    p_u2.show(snr=1, fig_title='Optimal second image', with_next=1)
    # # Monitor.show(*[u2.snrs, u1.snrs],mode='sort', fig_title='Чистое изображение', with_next=0)
    #
    color = ['k', 'r']
    SU.show(snr=1, color=color[0], with_next=1, fig_title='Straight sum')
    OU.show(snr=1, color=color[1], with_next=1, fig_title='Optimal sum')
    SU.show(snr=0, color=color[0], with_next=1, fig_title='Straight sum')
    OU.show(snr=0, color=color[1], with_next=0, fig_title='Optimal sum')
    # Monitor.show(*[SU.traces, OU.traces],mode='sort', fig_title='Straight and optimal sum', with_next=0, color=color)
    # Monitor.show(*[SU.snrs, OU.snrs], mode='sort', fig_title='Чистое изображение', with_next=0, color=color)

    # Monitor.show(*u1.traces, fig_title='Обрабатываемое изображение', color='g', with_next=1)
    # Monitor.show(*p_u1.traces, fig_title='Отфильтрованное изображение', color='g', with_next=1)
    # Monitor.show(*p_u1.snrs, fig_title='СНР отфильтрованное изображение', color='g', with_next=0)

