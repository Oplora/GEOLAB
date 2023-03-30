import matplotlib.pyplot as plt
from exceptions import specific_catch, os_path

"""
Нужно переписать методы, связанные с цветом и легендой. Конкретно нужно избавиться от добавления индекекса в аргументы
функции. Его исключение может вызвать ошибку, связанную с попыткой итерирования объекта None - если мы не подаем на вход 
color или legend, а в функцию кладем visual.get('color')[i] и visual.get('legend')[i]


Сделать коммит! 
1. Не переписал ссылающийся код в других файлах (Старые обозначения, названия, параметры)
"""

# DEFAULT AXES
DEFAULT_COLOR = "b"
DEFAULT_AX_LEGEND_NAME = "Trace №"
AX_TITLE_FONTSIZE = 10
AX_LEGEND_FONTSIZE = 10

# DEFAULT FIGURE
HEIGHT = 13
WIDTH = 13
OX_LABEL_STYLE = "italic"
OY_LABEL_STYLE = OX_LABEL_STYLE
FIG_TITLE_FONTSIZE = 20
FIG_FONTWEIGHT = 'bold'
TITLE_WEIGHT = 'bold'

# GLOBAL VARIABLES
graphs_amount = 0



def customize_figure(fig: plt.Figure, **visual: dict) -> None:
    fig.set_figheight(HEIGHT)
    fig.set_figwidth(WIDTH)
    fig.suptitle('{}'.format(str(visual.get('fig_title'))), fontsize=FIG_TITLE_FONTSIZE, fontweight=FIG_FONTWEIGHT)
    if isinstance(visual.get('xy_labels'), list):
        fig.supxlabel(visual.get('xy_labels')[0], style=OX_LABEL_STYLE)
        fig.supylabel(visual.get('xy_labels')[1], style=OY_LABEL_STYLE)


def extract(key: str, from_dictionary: dict):
    value = from_dictionary.get(key)
    if value is None:
        return [None] * graphs_amount
    elif isinstance(value, list):
        return value
    else:
        return [value] * graphs_amount


def manage_legend(axis, legend, index=-1, adjust=False):
    if legend is None:
        return
    elif legend is True:
        name = DEFAULT_AX_LEGEND_NAME + str(index)
    elif isinstance(legend, str):
        name = legend
    else:
        print("Wrong legend format")
        return None
    axis.set_title(name, fontsize=AX_LEGEND_FONTSIZE)
    if adjust:
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=0.4, hspace=0.4)




def plot_and_manage_color(axis: plt.Axes, graph, color):
    counts = range(len(graph))
    if color is not None:
        axis.plot(counts, graph, color=color)
    else:
        axis.plot(counts, graph)


def show(*graphs, fig_title=None, legend=None, mode='sep', color=None, xy_labels=None, skip=False, with_next=False):
    """ Make visualizational image for given graphs. """
    global graphs_amount
    graphs_amount = len(graphs)
    visual_customization = {'color': color, 'xy_labels': xy_labels, 'fig_title': fig_title, 'legend': legend}
    if mode == 'sep':
        show_separately(graphs, **visual_customization)
    elif mode == 'comb':
        show_jointly(graphs, **visual_customization)
    if skip:
        plt.close()
    if not with_next:
        plt.show()


def show_separately(graphs: list, **visual: dict) -> None:
    """Make one figure with multiple axes, i.d. different plots"""
    fig, axes = plt.subplots(nrows=graphs_amount, ncols=1)
    colors = extract('color', visual)
    legends = extract('legend', visual)
    for i in range(graphs_amount):
        axis = axes if graphs_amount == 1 else axes[i]
        plot_and_manage_color(axis, graphs[i], colors[i])
        manage_legend(axis, legends[i], i, adjust=True)
    customize_figure(fig, **visual)


def show_jointly(graphs: list, **visual: dict) -> None:
    fig, axis = plt.subplots()
    colors = extract('color', visual)
    legend = visual.get('legend')
    for i in range(graphs_amount):
        plot_and_manage_color(axis, graphs[i], colors[i])
    manage_legend(axis, legend)
    customize_figure(fig, **visual)

