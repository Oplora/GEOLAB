import matplotlib.pyplot as plt


def show(*values, fig_label=None, legend=None, mode='sep', color=None, dist=0, shift=0, skip=False, together=False,
         label=None):
    """ Make graphs for given arrays. """
    amount_of_plots = len(values)
    if mode == 'sep':
        fig, axes = plt.subplots(nrows=amount_of_plots, ncols=1, figsize=(13, 13))
        if amount_of_plots == 1:
            counts = [k for k in range(len(values[0]))]
            axes.plot(counts, values[0])
        else:
            for i in range(amount_of_plots):
                counts = [k for k in range(len(values[i]))]
                if color is not None:
                    axes[i].plot(counts, values[i], color=color[i])
                else:
                    axes[i].plot(counts, values[i])
                if legend is not None:
                    if not isinstance(legend, bool):
                        name = legend[i]
                    else:
                        name = str(i)
                    axes[i].set_title(name, fontsize=10)
                    plt.subplots_adjust(left=0.1,
                                        bottom=0.1,
                                        right=0.9,
                                        top=0.85,
                                        wspace=0.4,
                                        hspace=0.4)
        if isinstance(label, list):
            fig.supxlabel(label[0], style="italic")
            fig.supylabel(label[1], style="italic")
        fig.suptitle('{}'.format(str(fig_label)), fontsize=20, fontweight='bold')
    elif mode == 'comb':
        extra_fig = plt.figure()
        if isinstance(label, list):
            extra_fig.supxlabel(label[0])
            extra_fig.supylabel(label[1])
        extra_fig.set_figheight(13)
        extra_fig.set_figwidth(13)
        extra_fig.suptitle('{}'.format(str(fig_label)), fontsize=20, fontweight='bold')
        for i in range(amount_of_plots):
            size = len(values[i])
            if legend is not None and not isinstance(legend, bool):
                name = legend[i]
            else:
                name = str(i)
            plt.plot(range(size), values[i] + [dist * i] * size + shift, label=name, color=color)
        if legend is not None:
            plt.legend()
        # plt.title('{}'.format(str(fig_label)), fontsize=10)
    if skip:
        plt.close()
    if not together:
        plt.show()
