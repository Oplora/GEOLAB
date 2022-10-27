from Traces import Traces
import My_Monitor as mn
import My_Functions as fn
import numpy as np


def main():
    # f1 = Traces([-3, 3], 0.5).make(np.sin)
    # f2 = Traces([-3, 3], 0.5).make(fn.id)
    # f3 = Traces.conv(f1,f2)
    # mn.show([f1, f2, f3])

    f1 = Traces([0, 10], 0.5).make(np.sin)
    f2 = Traces([0, 10], 0.5).make(fn.id)
    f3 = Traces.conv(f1, f2)
    n1 = Traces([0, 10], 0.5).noise(10, 3)
    s1 = f2 + n1
    r1 = Traces([0, 10], 0.5).reflectance()
    # f4 = Traces.conv(s1, r1)

    """ Testing makeGrid and resize for boarders type [a,b], where a and b are counts. """
    # print(f1.boarders)
    # print(f1.makeGrid())
    # f1.resize([2, 4])
    # print(f1.boarders)
    # print(f1.makeGrid())

    """ Testing addition and multiplication"""
    # print(f1.values)
    # print(f2.values)
    # f4 = f1 + f2
    # print(f3.values)

    # print(f2.values)
    # f5 = 3 * f2
    # print(f5.values)
    # print(f2.values)

    # print(f2.values, "\n", n1.values,"\n", s1.values,"\n")

    """ Test for convolution"""
    # t1 = Traces([-1, 1], 1)
    # t1.set_values(np.array([1, 2, 3]))
    # t2 = Traces([-1, 1], 1)
    # t2.set_values(np.array([0, 1, 0.5]))
    #
    # my_convolution = Traces.conv(t1, t2)
    # numpy_convolution = np.convolve([1, 2, 3], [0, 1, 0.5])
    # print(my_convolution.get_values(), "\n", numpy_convolution)

    """ Testing My_Monitor.show()"""
    # mn.show(f1)
    # mn.show([f1, f2])
    # mn.show([f1, f2, f3])
    mn.show([f1, f2, f3], mode='att')
    print(f3.get_boarders())
    print(f3.makeGrid())
    print(len(f3.makeGrid()))
    print(f3.get_values())
    print(len(f3.get_values()))

    # f4 = -1 * f1
    # mn.show([f1,f4], mode='att')

    # mn.show(n1)

    # mn.show(r1)

    # mn.show([f2, n1, s1], mode='att')

    # mn.show([r1, s1, f4], mode='att')

if __name__ == '__main__':
    main()
