# import libimp
from ops import *
import source_data as sd
from numpy import pi
from source_data import *
from monitor import show


# MACRO-PARAMETERS

SEISMIC_SOURCES = 3 # Amount of traces in image
# SEISMOGRAMM_AMOUNT = 20
GEO_LAYERS = 5 # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 10 # Measure of layer falling speed. Shows how fast do they fall


if __name__ == '__main__':

    # SIGNAL COMPONENT PARAMETERS

    b1 = band_pass_filter(pi / 7, 1 * pi / 3, show=False)
    b2 = band_pass_filter(pi / 3, 1 * pi / 2)

    w1 = wave(b1, amplitude=20)
    w2 = wave(b2, amplitude=30)

    # Noises
    n1 = 2
    n2 = 1.3

    # Reflectivity in general for area
    AR = area_reflectivity(GEO_LAYERS, SEISMIC_SOURCES, shift=HIGHT_DIFFERENCES)

    # SEISMIC IMAGES
    si1 = seismic_image(AR, w1, n1)
    si2 = seismic_image(AR, w2, n2)

    # VISUALISATION
    show(*si1)
    show(*si2)




