from numpy import pi, abs, mean
from source_data import *
from Class_image import SeisImage
from Class_monitor import show

def set_cwd(geo_info, signals_info, noises_info):
    from os import mkdir, path, getcwd, chdir
    cdir = path.join(r'S:\GEOLAB\Diploma\Photos\Results', geo_info)
    if not path.exists(cdir):
        mkdir(cdir)
    chdir(cdir)
    cdir = path.join(getcwd(), signals_info)
    if not path.exists(cdir):
        mkdir(cdir)
    chdir(cdir)
    cdir = path.join(getcwd(), noises_info)
    if not path.exists(cdir):
        mkdir(cdir)
    chdir(cdir)


# PARAMETERS

SEISMIC_SOURCES = 40  # Amount of traces in image
GEO_LAYERS = 5  # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 0  # Measure of layer falling speed. Shows how fast do they fall
RANDOM = True
g_info = f"Seed - {SEED}. " \
         f"Traces - {SEISMIC_SOURCES}. " \
         f" Layers - {GEO_LAYERS}"

FREQ1 = [1 * pi / 12, 1 * pi / 4]
AMP1 = 80
FREQ2 = [1 * pi / 12, 1 * pi / 3]
AMP2 = 60
FREQ3 = [1 * pi / 6, 5 * pi / 12]
AMP3 = 40
freq1 = [f"{round(f / pi, 3)}"+'π' for f in FREQ1]
freq2 = [f"{round(f / pi, 3)}"+'π' for f in FREQ2]
freq3 = [f"{round(f / pi, 3)}"+'π' for f in FREQ3]
s_info = f"A1- {AMP1}, W1 - {freq1}. " \
         f"A2 - {AMP2}, W2 - {freq2}" \
         f"A3 - {AMP3}, W2 - {freq3}"

NOISE_PROC1 = 0.05
NOISE_PROC2 = 0.04
NOISE_PROC3 = 0.03
n_info = f"Noise 1th - {NOISE_PROC1*100}%. " \
         f"Noise 2th - {NOISE_PROC2*100}%" \
         f"Noise 2th - {NOISE_PROC3*100}%"

# SET NAME FOR CURRENT WORKING DIRECTORY
set_cwd(g_info,s_info,n_info)

if __name__ == '__main__':

    # SIGNAL COMPONENT PARAMETERS

    b1 = band_pass_filter(FREQ1[0], FREQ1[1], show=0)
    b2 = band_pass_filter(FREQ2[0], FREQ2[1], show=0)
    b3 = band_pass_filter(FREQ3[0], FREQ3[1], show=0)

    w1 = wave(b1, amplitude=AMP1)
    w2 = wave(b2, amplitude=AMP2)
    w3 = wave(b3, amplitude=AMP3)
    W1 = SeisImage(w1)
    W2 = SeisImage(w2)
    W3 = SeisImage(w3)

    show(w1[ALL_COUNTS//2 - 1:], w2[ALL_COUNTS//2 - 1:], w3[ALL_COUNTS//2 - 1:],mode='sep', color=[(0.70, 0.35, 0.15), (0.90, 0.45, 0), (0.80, 0.40, 0.20)],
         fig_title='Возбужденные сигналы', xy_labels=['Время, мс', 'Амплитуда, мВ'])
    # Noises
    n1 = NOISE_PROC1 * AMP1
    n2 = NOISE_PROC2 * AMP2
    n3 = NOISE_PROC3 * AMP3

    # Reflectivity in general for area
    AR = area_reflectivity(GEO_LAYERS, SEISMIC_SOURCES, shift=HIGHT_DIFFERENCES, rand=RANDOM)
    R = SeisImage(AR)

    # SEISMIC IMAGES
    si1 = seismic_image(AR, w1, n1)
    si2 = seismic_image(AR, w2, n2)
    si3 = seismic_image(AR, w3, n3)

    u1 = SeisImage(si1)
    u2 = SeisImage(si2)
    u3 = SeisImage(si3)
    U = [u3, u2, u1]

    __ideal = [SeisImage(seismic_image(AR, w1)), SeisImage(seismic_image(AR, w2))]

    # PROCESSING

    p_u1 = u1.optimal()
    p_u2 = u2.optimal()
    p_u3 = u3.optimal()
    OU = SeisImage.MCOP(U)
    SU = mean(U, axis=0)
    __Ideal_result = mean(__ideal, axis=0)

    # VISUALISATION
    colors = {'u1': [(0.70, 0.35, 0.15), (0.70, 0.35, 0.15)],
              'u2': [(0.90, 0.45, 0), (0.90, 0.45, 0)],
              'opti_u1': [(0.35, 0.70, 0.15), (0.35, 0.70, 0.15)],
              'opti_u2': [(0.45, 0.90, 0), (0.45, 0.90, 0)],
              'straight': [(0.8, 0.16, 0), (0.8, 0.16, 0)],
              'optimal': [(0.16, 0.8, 0), (0.16, 0.8, 0)],
              }
    colors = {'u1': (0.70, 0.35, 0.15),
              'u2': (0.90, 0.45, 0),
              'u3': (0.80, 0.40, 0.20),
              'opti_u1': (0.35, 0.70, 0.15),
              'opti_u2': (0.45, 0.90, 0),
              'opti_u3': (0.40, 0.80, 0.20),
              'straight': (0.8, 0.16, 0),
              'optimal': (0.16, 0.8, 0),
              }
    # labels = [['Время, мс', 'Частота, Гц'], ['Амплитуда, мВ', 'Процент, %']]
    labels = ['Время, мс', 'Частота, Гц']
    labels = ['Расстояние, м', 'Время, мс']
    # _snr = 'both'
    _snr = 0
    R.show(mode='join', with_next=0, fig_title='Отражательная способность среды', xy_labels=labels, color=(0.45, 0.45, 1), save=0, close=0)
    u1.show(mode='join',snr=_snr, with_next=0, fig_title='Первое изображение', xy_labels=labels, color=colors.get('u1'), save=0, close=0)
    u2.show(mode='join',snr=_snr, with_next=0, fig_title='Второе изображение', xy_labels=labels, color=colors.get('u2'), save=0, close=0)
    u3.show(mode='join',snr=_snr, with_next=0, fig_title='Третье изображение', xy_labels=labels, color=colors.get('u3'), save=0, close=0)
    p_u1.show(mode='join',snr=_snr, with_next=0, fig_title='Оптимальное первое изображение', xy_labels=labels, color=colors.get('opti_u1'), save=0, close=0)
    p_u2.show(mode='join',snr=_snr, with_next=0, fig_title='Оптимальное второе изображение', xy_labels=labels, color=colors.get('opti_u2'), save=0, close=0)
    p_u3.show(mode='join',snr=_snr, with_next=0, fig_title='Оптимальное третье изображение', xy_labels=labels, color=colors.get('opti_u3'), save=0, close=0)
    SU.show(mode='join',snr=_snr, with_next=0, fig_title='Прямая сумма трасс', xy_labels=labels, color=colors.get('straight'), save=0, close=0)
    OU.show(mode='join',snr=_snr, with_next=0, fig_title='Оптимальная сумма трасс', xy_labels=labels, color=colors.get('optimal'), save=0, close=0)
