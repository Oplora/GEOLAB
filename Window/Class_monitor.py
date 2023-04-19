import matplotlib.pyplot as plt
from numpy import linspace, pi
from exceptions import specific_catch, os_path

def multiple_formatter(denominator=2, number=pi, latex='\pi'):
    import numpy as np
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def _multiple_formatter(x, pos):
        den = denominator
        num = np.int(np.rint(den * x / number))
        com = gcd(num, den)
        (num, den) = (int(num / com), int(den / com))
        if den == 1:
            if num == 0:
                return r'$0$'
            if num == 1:
                return r'$%s$' % latex
            elif num == -1:
                return r'$-%s$' % latex
            else:
                return r'$%s%s$' % (num, latex)
        else:
            if num == 1:
                return r'$\frac{%s}{%s}$' % (latex, den)
            elif num == -1:
                return r'$\frac{-%s}{%s}$' % (latex, den)
            else:
                return r'$\frac{%s%s}{%s}$' % (num, latex, den)

    return _multiple_formatter


class Multiple:

    def __init__(self, denominator=2, number=pi, latex='\pi'):
        self.denominator = denominator
        self.number = number
        self.latex = latex

    def locator(self):
        return plt.MultipleLocator(self.number / self.denominator)

    def formatter(self):
        return plt.FuncFormatter(multiple_formatter(self.denominator, self.number, self.latex))


# DEFAULT AXES
DEFAULT_COLOR = "b"
DEFAULT_AX_LEGEND_NAME = "Trace №"
AX_TITLE_FONTSIZE = 10
AX_LEGEND_FONTSIZE = 10

# DEFAULT FIGURE
HEIGHT = 13
WIDTH = 17
OX_LABEL_STYLE = "italic"
OY_LABEL_STYLE = OX_LABEL_STYLE
FIG_FONTSIZE = 20
FIG_FONTWEIGHT = 'bold'
TITLE_WEIGHT = 'bold'

# GLOBAL VARIABLES
GRAPHS_AMOUNT = 0
MODE = None


# DEFAULT METHODS
def plot_and_design(axis: plt.Axes, graph, color, X_axis=None):
    if X_axis is not None:
        start, stop, num = X_axis
        counts = linspace(start, stop, num)
        axis.grid(True)
        axis.xaxis.set_major_locator(plt.MultipleLocator(pi / 2))
        axis.xaxis.set_minor_locator(plt.MultipleLocator(pi / 12))
        axis.xaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter()))
    else:
        axis.axhline(0, color='black', lw=1)
        counts = range(len(graph))
    if color is not None:
        axis.plot(graph, counts, color=color)
        # axis.plot(counts, graph, color=color)
    else:
        # axis.plot(graph, counts)
        axis.plot(counts, graph)


def separately(graphs: list, **visual: dict) -> None:
    """Make one figure with multiple axes.
    Axes contain only one graph from 'graphs'"""
    fig, axes = plt.subplots(nrows=GRAPHS_AMOUNT, ncols=1)
    colors = extract('color', visual)
    legends = extract('legend', visual)
    X_axes = extract('X_axis', visual)
    for i in range(GRAPHS_AMOUNT):
        axis = axes if GRAPHS_AMOUNT == 1 else axes[i]
        produce(PLOT_AND_DESIGN)(axis, graphs[i], colors[i], X_axes[i])
        manage_legend(axis, legends[i], i, adjust=True)
    customize_figure(fig, **visual)


def jointly(graphs: list, **visual: dict) -> None:
    """Make one figure with one axis.
     Axis contains all graphs from 'graphs'"""
    from numpy import add
    fig, axis = plt.subplots()
    colors = extract('color', visual)
    legend = visual.get('legend')
    for i in range(GRAPHS_AMOUNT):
        shift = [i * max(graphs[0]) * 0.5 for _ in range(len(graphs[i]))]
        # shift = [i * 100 for _ in range(len(graphs[i]))]
        graph = add(graphs[i], shift)
        produce(PLOT_AND_DESIGN)(axis, graph, colors[i])
    manage_legend(axis, legend)
    customize_figure(fig, **visual)


def combined(graphs_list: list[list], **visual: dict) -> None:
    """Make one figure with multiple axes.
     Axes contain all graphs with same index from 'graphs_list'"""
    GRAPHS_AMOUNT = len(graphs_list[0])
    fig, axes = plt.subplots(nrows=GRAPHS_AMOUNT, ncols=1)
    colors = extract('color', visual)
    for j, graph in enumerate(graphs_list):
        for i in range(GRAPHS_AMOUNT):
            axis = axes if GRAPHS_AMOUNT == 1 else axes[i]
            produce(PLOT_AND_DESIGN)(axis, graph[i], colors[j])
    customize_figure(fig, **visual)


def sep_comb(graphs_list: list[list], **visual: dict) -> None:
    """Make one figure with multiple axes.
     Axes contain all graphs with same index from 'graphs_list'"""
    GRAPHS_AMOUNT = len(graphs_list[0])
    images_amount = len(graphs_list)
    fig, axes = plt.subplots(nrows=GRAPHS_AMOUNT, ncols=images_amount)
    colors = extract('color', visual)
    X_axes = extract('X_axis', visual)
    for j, graph in enumerate(graphs_list):
        for i in range(GRAPHS_AMOUNT):
            axis = axes if GRAPHS_AMOUNT == 1 else axes[i][j]
            produce(PLOT_AND_DESIGN)(axis, graph[i], colors[j], X_axes[j])
    customize_figure(fig, axes, **visual)


PLOT_AND_DESIGN = plot_and_design
SEPARATELY = separately
JOINTLY = jointly
SORTED = combined
SEP_COMB = sep_comb


def produce(method):
    def inner(*args, **kwargs):
        return method(*args, **kwargs)

    return inner


def set_graphs_amount(*graphs):
    try:
        iter(graphs[0][0])
        set_graphs_amount(*graphs[0])
    except TypeError:
        global GRAPHS_AMOUNT
        GRAPHS_AMOUNT = len(graphs)


def show(*graphs, fig_title=None, legend=None, mode='sep', color=None, xy_labels=None, X_axis=None,
         with_next=False, save=False, close=False):
    """ Make visualizational image for given graphs. """
    # global GRAPHS_AMOUNT
    global MODE
    MODE = mode
    set_graphs_amount(*graphs)
    visual_customization = {'color': color, 'xy_labels': xy_labels, 'fig_title': fig_title, 'legend': legend,
                            'X_axis': X_axis}
    if MODE == 'sep':
        produce(SEPARATELY)(graphs, **visual_customization)
    elif MODE == 'join':
        produce(JOINTLY)(graphs, **visual_customization)
    elif MODE == 'comb':
        produce(SORTED)(graphs, **visual_customization)
    elif MODE == 'sepcomb':
        produce(SEP_COMB)(graphs, **visual_customization)
    if save:
        plt.savefig(fig_title)
    if close:
        plt.close()
    if not with_next:
        plt.show()


def customize_figure(fig: plt.Figure, axes=None, **visual: dict) -> None:
    fig.set_figheight(HEIGHT)
    fig.set_figwidth(WIDTH)
    fig.suptitle(f"{visual.get('fig_title')}", fontsize=FIG_FONTSIZE, fontweight=FIG_FONTWEIGHT)
    if isinstance(visual.get('xy_labels'), list):
        x_label = visual.get('xy_labels')[0]
        y_label = visual.get('xy_labels')[1]
        if MODE == 'sepcomb':
            plt.setp(axes[-1, 0], xlabel=x_label[0])
            plt.setp(axes[-1, 1], xlabel=x_label[1])
            plt.setp(axes[:, 0], ylabel=y_label[0])
            plt.setp(axes[:, 1], ylabel=y_label[1])
        elif MODE == 'sep':
            fig.supxlabel(x_label, style=OX_LABEL_STYLE)
            fig.supylabel(y_label, style=OY_LABEL_STYLE)
        elif MODE == 'join':
            fig.supxlabel(x_label, style=OX_LABEL_STYLE)
            fig.supylabel(y_label, style=OY_LABEL_STYLE)


def extract(key: str, from_dictionary: dict):
    value = from_dictionary.get(key)
    if value is None:
        return [None] * GRAPHS_AMOUNT
    elif isinstance(value, list):
        return value
    else:
        return [value] * GRAPHS_AMOUNT


def manage_legend(axis, legend, index=-1, adjust=False):
    if legend is None:
        return
    elif legend is True:
        name = DEFAULT_AX_LEGEND_NAME + str(index)
    elif isinstance(legend, str):
        name = legend
    else:
        raise TypeError("Wrong legend format")
    axis.set_title(name, fontsize=AX_LEGEND_FONTSIZE)
    if adjust:
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=0.4, hspace=0.4)



