import inspect

import matplotlib.pyplot as plt
import numpy as np



def show(object, mode='sep'):
    """ Procedure that display trace or set of traces"""
    from Traces import Traces
    plt.style.use('seaborn')
    if isinstance(object, Traces):
        time_axis = object.makeGrid()
        values = object.get_values().tolist()
        trace_type = object.get_name()
        plt.plot(time_axis, values)
        plt.title(trace_type)

        plt.grid(True)
        plt.xlabel('Time')
        plt.ylabel('Value')

    elif isinstance(object, list):
        if mode == 'sep':
            fig, axs = plt.subplots(nrows=1, ncols=len(object), sharex=True, squeeze=False)
            for i in range(0, len(object)):
                reversed_values = (object[i]).get_values().tolist()[::-1]
                # time = [x for x in range(len(object[i].values))]
                time = object[i].makeGrid()
                axs[0, i].plot(reversed_values, time)
                axs[0, i].set_title(object[i].get_name())
                axs[0,i].set_ylabel('Time')
                axs[0,i].set_xlabel('Value')
            fig.suptitle('Сейсмограмма')
        elif mode == 'att':
            for i in range(0, len(object)):
                time_axis = object[i].makeGrid()
                values = (object[i]).get_values().tolist()
                trace_type = object[i].get_name()
                plt.plot(time_axis, values, label=trace_type)
            plt.grid(True)
            plt.legend()
            plt.xlabel('Time')
            plt.ylabel('Value')
    plt.show()
