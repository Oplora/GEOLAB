from numpy import pi, abs, mean
from source_data import *
from Class_image import SeisImage


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
    # return path.join(geo_info, signals_info, noises_info)


# PARAMETERS

SEISMIC_SOURCES = 3  # Amount of traces in image
GEO_LAYERS = 5  # Layers amount (reflectivity picks) of modeling area
HIGHT_DIFFERENCES = 0  # Measure of layer falling speed. Shows how fast do they fall
RANDOM = True
g_info = f"Seed - {SEED}. " \
         f"Traces - {SEISMIC_SOURCES}. " \
         f" Layers - {GEO_LAYERS}"

FREQ1 = [pi / 12, 1 * pi / 3]
AMP1 = 50
FREQ2 = [1 * pi / 6, 1 * pi / 2]
AMP2 = 30
freq1 = [f"{round(f / pi, 3)}"+'π' for f in FREQ1]
freq2 = [f"{round(f / pi, 3)}"+'π' for f in FREQ2]
s_info = f"A1- {AMP1}, W1 - {freq1}. " \
         f"A2 - {AMP2}, W2 - {freq2}"

NOISE_PROC1 = 0.02
NOISE_PROC2 = 0.02
n_info = f"Noise 1th - {NOISE_PROC1}%. " \
         f"Noise 2th - {NOISE_PROC2}%"

# SET NAME FOR CURRENT WORKING DIRECTORY
set_cwd(g_info,s_info,n_info)

if __name__ == '__main__':

    # SIGNAL COMPONENT PARAMETERS

    b1 = band_pass_filter(FREQ1[0], FREQ1[1], show=0)
    b2 = band_pass_filter(FREQ2[0], FREQ2[1], show=0)

    w1 = wave(b1, amplitude=AMP1)
    w2 = wave(b2, amplitude=AMP2)

    # Noises
    n1 = NOISE_PROC1 * AMP1
    n2 = NOISE_PROC2 * AMP2

    # Reflectivity in general for area
    AR = area_reflectivity(GEO_LAYERS, SEISMIC_SOURCES, shift=HIGHT_DIFFERENCES, rand=RANDOM)
    R = SeisImage(AR)

    # SEISMIC IMAGES
    si1 = seismic_image(AR, w1, n1)
    si2 = seismic_image(AR, w2, n2)

    u1 = SeisImage(si1)
    u2 = SeisImage(si2)
    U = [u2, u1]

    __ideal = [SeisImage(seismic_image(AR, w1)), SeisImage(seismic_image(AR, w2))]

    # PROCESSING

    p_u1 = u1.optimal()
    p_u2 = u2.optimal()
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

    _snr = 'both'
    R.show(with_next=0, fig_title='Аккустические импедансы', color=(0.45, 0.45, 1), save=True, close=1)
    u1.show(snr=_snr, with_next=0, fig_title='Первое изображение', color=colors.get('u1'), save=True, close=True)
    u2.show(snr=_snr, with_next=0, fig_title='Второе изображение', color=colors.get('u2'), save=True, close=True)
    p_u1.show(snr=_snr, with_next=1, fig_title='Оптимальное первое изображение', color=colors.get('opti_u1'), save=True, close=True)
    p_u2.show(snr=_snr, with_next=1, fig_title='Оптимальное второе изображение', color=colors.get('opti_u2'), save=True, close=True)
    SU.show(snr=_snr, with_next=1, fig_title='Прямая сумма трасс', color=colors.get('straight'), save=True, close=True)
    OU.show(snr=_snr, with_next=1, fig_title='Оптимальная сумма трасс', color=colors.get('optimal'), save=True, close=True)
    # __Ideal_result.show(snr=_snr, with_next=1, fig_title='Идеальный случай', color=(0, 0, 1), save=True, close=True)
    # Monitor.show(*[SU.traces, OU.traces],mode='sort', fig_title='Straight and optimal sum', with_next=0, color=color)
    # Monitor.show(*[SU.snrs, OU.snrs], mode='sort', fig_title='Чистое изображение', with_next=0, color=color)

    # Monitor.show(*u1.traces, fig_title='Обрабатываемое изображение', color='g', with_next=1)
    # Monitor.show(*p_u1.traces, fig_title='Отфильтрованное изображение', color='g', with_next=1)
    # Monitor.show(*p_u1.snrs, fig_title='СНР отфильтрованное изображение', color='g', with_next=0)
