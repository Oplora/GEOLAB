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

SEISMIC_SOURCES = 6 # Amount of traces in image
# SEISMOGRAMM_AMOUNT = 20
GEO_LAYERS = 5  # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 5  # Measure of layer falling speed. Shows how fast do they fall

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
    U = [u1, u2]

    # PROCESSING
    p_U1 = U1.optimal()
    p_u1 = u1.optimal()
    p_u2 = u2.optimal()
    # OU = SeisImage.MCOP(U)
    # SU = mean(U, axis=0)


    # VISUALISATION
    # OU.show(snr=1, fig_title="Оптимальная сумма", with_next=1)
    # SU.show(snr=1, fig_title="Прямая сумма")

    # U1.show(fig_title='Чистое изображение')
    u1.show(snr=0, fig_title='Обрабатываемое изображение', color='g', with_next=1)
    p_u1.show(snr=0, fig_title='Отфильтрованное изображение', color='g', with_next=0)
    # Monitor.show(*U1.traces, fig_title='Чистое изображение', with_next=1)
    # Monitor.show(*u1.traces, fig_title='Обрабатываемое изображение', color='g', with_next=1)
    # Monitor.show(*p_u1.traces, fig_title='Отфильтрованное изображение', color='g', with_next=1)
    # Monitor.show(*p_u1.snrs, fig_title='СНР отфильтрованное изображение', color='g', with_next=0)

