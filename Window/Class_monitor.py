import matplotlib.pyplot as plt
from numpy import linspace
from exceptions import specific_catch, os_path

"""
Нужно переписать методы, связанные с цветом и легендой. Конкретно нужно избавиться от добавления индекекса в аргументы
функции. Его исключение может вызвать ошибку, связанную с попыткой итерирования объекта None - если мы не подаем на вход 
color или legend, а в функцию кладем visual.get('color')[i] и visual.get('legend')[i]


Сделать коммит! 
1. Не переписал ссылающийся код в других файлах (Старые обозначения, названия, параметры)
"""


class Monitor:
    # DEFAULT METHODS
    __jointly = None

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
    FIG_FONTSIZE = 20
    FIG_FONTWEIGHT = 'bold'
    TITLE_WEIGHT = 'bold'

    # GLOBAL VARIABLES
    graphs_amount = 0

    @staticmethod
    def _customize_figure(fig: plt.Figure, **visual: dict) -> None:
        fig.set_figheight(Monitor.HEIGHT)
        fig.set_figwidth(Monitor.WIDTH)
        fig.suptitle(f"{visual.get('fig_title')}", fontsize=Monitor.FIG_FONTSIZE, fontweight=Monitor.FIG_FONTWEIGHT)
        if isinstance(visual.get('xy_labels'), list):
            fig.supxlabel(visual.get('xy_labels')[0], style=Monitor.OX_LABEL_STYLE)
            fig.supylabel(visual.get('xy_labels')[1], style=Monitor.OY_LABEL_STYLE)

    @staticmethod
    def _extract(key: str, from_dictionary: dict):
        value = from_dictionary.get(key)
        if value is None:
            return [None] * Monitor.graphs_amount
        elif isinstance(value, list):
            return value
        else:
            return [value] * Monitor.graphs_amount

    @staticmethod
    def _manage_legend(axis, legend, index=-1, adjust=False):
        if legend is None:
            return
        elif legend is True:
            name = Monitor.DEFAULT_AX_LEGEND_NAME + str(index)
        elif isinstance(legend, str):
            name = legend
        else:
            raise TypeError("Wrong legend format")
        axis.set_title(name, fontsize=Monitor.AX_LEGEND_FONTSIZE)
        if adjust:
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=0.4, hspace=0.4)

    @staticmethod
    def _plot_and_manage_color(axis: plt.Axes, graph, color, X_axis=None):
        if X_axis is not None:
            start, stop, num = X_axis
            counts = linspace(start, stop, num)
        else:
            counts = range(len(graph))
        if color is not None:
            axis.plot(counts, graph, color=color)
        else:
            axis.plot(counts, graph)

    @staticmethod
    def show(*graphs, fig_title=None, legend=None, mode='sep', color=None, xy_labels=None, X_axis=None,
             with_next=False):
        """ Make visualizational image for given graphs. """
        # global graphs_amount
        Monitor.__set_graphs_amount(*graphs)
        visual_customization = {'color': color, 'xy_labels': xy_labels, 'fig_title': fig_title, 'legend': legend,
                                'X_axis': X_axis}
        if mode == 'sep':
            Monitor._show_separately(graphs, **visual_customization)
        elif mode == 'comb':
            Monitor.__show_jointly(graphs, **visual_customization)
        elif mode == 'sort':
            Monitor._show_sorted(graphs, **visual_customization)
        if not with_next:
            plt.show()

    @staticmethod
    def _show_separately(graphs: list, **visual: dict) -> None:
        """Make one figure with multiple axes.
        Axes contain only one graph from 'graphs'"""
        fig, axes = plt.subplots(nrows=Monitor.graphs_amount, ncols=1)
        colors = Monitor._extract('color', visual)
        legends = Monitor._extract('legend', visual)
        X_axes = Monitor._extract('X_axis', visual)
        for i in range(Monitor.graphs_amount):
            axis = axes if Monitor.graphs_amount == 1 else axes[i]
            Monitor._plot_and_manage_color(axis, graphs[i], colors[i], X_axes[i])
            Monitor._manage_legend(axis, legends[i], i, adjust=True)
        Monitor._customize_figure(fig, **visual)

    @staticmethod
    def __show_jointly(graphs: list, **visual: dict) -> None:
        """Make one figure with one axis.
         Axis contains all graphs from 'graphs'"""
        fig, axis = plt.subplots()
        colors = Monitor._extract('color', visual)
        legend = visual.get('legend')
        for i in range(Monitor.graphs_amount):
            Monitor._plot_and_manage_color(axis, graphs[i], colors[i])
        Monitor._manage_legend(axis, legend)
        Monitor._customize_figure(fig, **visual)

    @staticmethod
    def _show_sorted(graphs_list: list[list], **visual: dict) -> None:
        """Make one figure with multiple axes.
         Axes contain all graphs with same index from 'graphs_list'"""
        Monitor.graphs_amount = len(graphs_list[0])
        fig, axes = plt.subplots(nrows=Monitor.graphs_amount, ncols=1)
        colors = Monitor._extract('color', visual)
        for j, graph in enumerate(graphs_list):
            for i in range(Monitor.graphs_amount):
                axis = axes if Monitor.graphs_amount == 1 else axes[i]
                Monitor._plot_and_manage_color(axis, graph[i], colors[j])
        Monitor._customize_figure(fig, **visual)

    @classmethod
    def __set_graphs_amount(cls, *graphs):
        try:
            iter(graphs[0][0])
            cls.__set_graphs_amount(*graphs[0])
        except TypeError:
            cls.graphs_amount = len(graphs)

    # @classmethod
    # def set_joint_method(cls, function=None):
    #     if function is None and cls.__jointly is None:
    #         cls.__jointly = cls.__show_jointly
    #     else:
    #         cls.__jointly = function
