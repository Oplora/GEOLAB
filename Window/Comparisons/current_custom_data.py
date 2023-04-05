# import libimp
from ops import *
import source_data as sd
from numpy import pi, abs, mean
from source_data import *
from monitor import show
from scipy.signal import correlate
import copy_ops as testing
from Class_image import SeisImage


# MACRO-PARAMETERS

SEISMIC_SOURCES = 3 # Amount of traces in image
# SEISMOGRAMM_AMOUNT = 20
GEO_LAYERS = 5 # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 10 # Measure of layer falling speed. Shows how fast do they fall


if __name__ == '__main__':

    # SIGNAL COMPONENT PARAMETERS

    b1 = band_pass_filter(pi / 3, 1 * pi / 2, show=False)
    b2 = band_pass_filter(pi / 4, 2 * pi / 3)

    w1 = wave(b1, amplitude=20)
    w2 = wave(b2, amplitude=20)

    # Noises
    n1 = 2
    n2 = 3

    # Reflectivity in general for area
    AR = area_reflectivity(GEO_LAYERS, SEISMIC_SOURCES, shift=HIGHT_DIFFERENCES)

    # SEISMIC IMAGES
    si1 = seismic_image(AR, w1, n1)
    si2 = seismic_image(AR, w2, n2)

    U1 = SeisImage(seismic_image(AR, w1))
    u1 = SeisImage(si1)
    u2 = SeisImage(si2)


    #PROCESSING
    p_u1 = u1.optimal()
    p_U1 = U1.optimal()



    # VISUALISATION
    show(*U1.traces, fig_title='Чистое изображение', with_next=1)
    show(*u1.traces, fig_title='Обрабатываемое изображение', color='g', with_next=1)
    show(*p_u1.traces, fig_title='Отфильтрованное изображение', color='g', with_next=1)
    show(*u1.snrs, fig_title='СНР обрабатываемое изображение', color='g', with_next=1)
    show(*p_u1.snrs, fig_title='СНР отфильтрованное изображение', color='g', with_next=0)



