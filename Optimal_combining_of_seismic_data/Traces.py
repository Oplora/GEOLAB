import math
import random as rnd
import numpy as np


class Traces:

    def __init__(self, boarders, t_step=0, function=None):

        self.__values = np.array([])
        """
                self.__values is a set for trace values
        """
        self.__name = str()
        """
                self.name is a name for type of trace: noise (Noise), signal without noise (Pure Signal),
                signal with noise (Signal), convolution (Convolution), reflectance (Reflectance).
                This attribute helps in visualising traces in My_Monitor file
        """

        if (boarders[0] >= boarders[1]) or (len(boarders) > 2) \
                or (not isinstance(boarders[0], int)) or (not isinstance(boarders[1], int)):
            raise Exception("Exception: Incorrect boarders")
        else:
            self.__boarders = boarders.copy()  # time scale
        """
                self.__boarders consists of two integer numbers: number of first count and number of last count.
                Form having time relevant count use Traces.makeGrid()
        """
        if t_step <= 0:
            raise Exception("Exception: Time step should be positive and less or equal than interval ending")
        else:
            self.__t_step = t_step
        """
                self.__t_step is a time interval between neighbouring counts
        """
        # OLD CODE BELOW
        # if t_step <= 0 or (t_step > boarders[1] - boarders[0]):
        #     raise Exception("Exception: Time step should be positive and less or equal than interval ending")
        # else:
        #     self.__t_step = t_step

        # if function is not None:
        #     x = self.__boarders[0]
        #     while True:
        #         self.__values = np.append(self.__values, function(x))
        #         x += self.__t_step
        #         if x > self.__boarders[1]:
        #             break

    def get_name(self):
        return self.__name

    def get_values(self):
        return self.__values
    def set_values(self, custom_values):
        self.__values = custom_values

    def get_boarders(self):
        return self.__boarders

    def get_t_step(self):
        return self.__t_step

    def __add__(self, other):
        """ Define addition in receiver class """

        if self.__boarders == other.__boarders and self.__t_step == other.__t_step:
            sum = Traces(self.__boarders, self.__t_step)
            sum.__values = np.add(self.__values, other.__values)

            if self.get_name() == other.get_name():
                sum.__name = self.get_name()
            elif self.get_name() != other.get_name():
                sum.__name = "Signal"
            return sum
        else:
            print("Not valid inputs")
            return None

    def __rmul__(self, other):
        """ Define multiplication of trace and number. It multiplies values with given number """
        if isinstance(other, float) or isinstance(other, int):
            mul = Traces(self.__boarders, self.__t_step)
            copy = self.__values.copy()
            mul.__values = copy * other
            return mul

    def copy_this(self):
        """ Function that copies given trace"""
        # copied_boarders = self.__boarders.copy()
        copy = Traces(self.__boarders, self.__t_step)
        copy.__values = self.__values.copy()
        return copy

    def make(self, function):
        """ Function making signal. Just for testing code"""
        x = self.__boarders[0]
        self.__name = "Pure Signal"
        while True:
            self.__values = np.append(self.__values, function(x))
            x += 1
            if x > self.__boarders[1]:
                break
        return self

        # OLD CODE BELOW
        # x = self.__boarders[0]
        # while True:
        #     self.__values = np.append(self.__values, function(x))
        #     x += self.__t_step
        #     if x > self.__boarders[1]:
        #         break
        # return self

    def makeGrid(self):
        """ Function that makes grid for time axis"""
        time_grid = []
        point = self.__boarders[0]
        while point <= self.__boarders[1]:
            time_grid.append(point * self.__t_step)
            point += 1
        return time_grid

        # OLD CODE BELOW
        # time_grid = []
        # point = self.__boarders[0]
        # while point <= self.__boarders[1]:
        #     time_grid.append(point)
        #     point += self.__t_step
        # return time_grid

    def resize(self, new_boarders):
        """ Procedure that change trace boarders on new one """

        # Exception
        if new_boarders[0] >= new_boarders[1]:
            raise Exception("Incorrect boarders")

        differences_left = abs(new_boarders[0] - self.__boarders[0])
        differences_right = abs(self.__boarders[1] - new_boarders[1])

        # Interval beginning
        if self.__boarders[0] >= new_boarders[0]:
            amount_of_new_points = differences_left
            self.__boarders[0] = new_boarders[0]
            self.__values = np.flip(np.append(np.flip(self.__values, 0), [0] * amount_of_new_points), 0)

        elif self.__boarders[0] < new_boarders[0]:
            amount_of_deleting_points = differences_left
            self.__boarders[0] = new_boarders[0]
            self.__values = np.delete(self.__values, list(range(amount_of_deleting_points)))

        # Interval ending
        if self.__boarders[1] <= new_boarders[1]:
            amount_of_new_points = differences_right
            self.__boarders[1] = new_boarders[1]
            self.__values = np.append(self.__values, [0] * amount_of_new_points)

        elif self.__boarders[1] > new_boarders[1]:
            amount_of_deleting_points = differences_right
            self.__boarders[1] = new_boarders[1]
            last_index = len(self.__values)
            self.__values = np.delete(self.__values, list(range(last_index - amount_of_deleting_points, last_index)))

        # OLD CODE BELOW
        # def resize(self, new_boarders):
        #     """ Procedure that change trace boarders on new one """
        #
        #     # Exceptions
        #     if new_boarders[0] >= new_boarders[1]:
        #         raise Exception("Incorrect interval")
        #     elif (self.__t_step > new_boarders[1] - new_boarders[0]):
        #         raise Exception("Interval is too short for given time step")
        #     mod_left = int((new_boarders[0] - self.__boarders[0]) // self.__t_step)
        #     if float(((new_boarders[0] - self.__boarders[0]) % self.__t_step)) != 0:
        #         sign = np.sign(self.__boarders[0])
        #         val_boar = [str((abs(self.__boarders[0]) - self.__t_step * mod_left) * sign),
        #                     str((abs(self.__boarders[0]) - self.__t_step * (mod_left + 1)) * sign)]
        #         raise Exception("Incorrect left boarder. Better use {0} or {1}".format(val_boar[0], val_boar[1]))
        #     mod_right = int((self.__boarders[1] - new_boarders[1]) // self.__t_step)
        #     if float(((new_boarders[1] - self.__boarders[1]) % self.__t_step)) != 0:
        #         sign = np.sign(self.__boarders[1])
        #         val_boar = [str((abs(self.__boarders[1]) - self.__t_step * mod_right) * sign),
        #                     str((abs(self.__boarders[1]) - self.__t_step * (mod_right + 1)) * sign)]
        #         raise Exception("Incorrect right boarder. Better use {0} or {1}".format(val_boar[1], val_boar[0]))
        #
        #     # Interval beginning
        #     if self.__boarders[0] >= new_boarders[0]:
        #
        #         amount_of_new_points = math.trunc((self.__boarders[0] - new_boarders[0]) / self.__t_step)
        #         self.__boarders[0] = new_boarders[0]
        #
        #         self.__values = np.flip(np.append(np.flip(self.__values, 0), [0] * amount_of_new_points), 0)
        #
        #     elif self.__boarders[0] < new_boarders[0]:
        #
        #         amount_of_deleting_points = mod_left
        #         self.__boarders[0] = new_boarders[0]
        #
        #         self.__values = np.delete(self.__values, list(range(amount_of_deleting_points)))
        #
        #     # Interval ending
        #     if self.__boarders[1] <= new_boarders[1]:
        #
        #         amount_of_new_points = math.trunc((new_boarders[1] - self.__boarders[1]) / self.__t_step)
        #         self.__boarders[1] = new_boarders[1]
        #
        #         self.__values = np.append(self.__values, [0] * amount_of_new_points)
        #
        #     elif self.__boarders[1] > new_boarders[1]:
        #
        #         amount_of_deleting_points = mod_right
        #         self.__boarders[1] = new_boarders[1]
        #
        #         last_index = len(self.__values)
        #         self.__values = np.delete(self.__values, list(range(last_index - amount_of_deleting_points, last_index)))

    def conv(self, other):
        """ Function that convolves traces with same boarders and step """

        amount_of_counts_in_trace = len(self.makeGrid())
        counts_in_convolution = amount_of_counts_in_trace + amount_of_counts_in_trace - 1

        duplicate = self.copy_this()
        old_boarders = self.__boarders.copy()
        new_left_boarder = duplicate.__boarders[0] - (amount_of_counts_in_trace - 1)
        new_right_boarder = duplicate.__boarders[1] + (amount_of_counts_in_trace - 1)
        duplicate.resize([new_left_boarder, new_right_boarder])

        flipped = np.flip(other.__values)
        # convolution_boarders = [0, counts_in_convolution - 1]
        l_boar = -math.ceil((old_boarders[1] - old_boarders[0]) / 2)
        r_boar = counts_in_convolution - 1 - abs(l_boar)
        convolution_boarders = [l_boar, r_boar]
        convolution = Traces(convolution_boarders, duplicate.__t_step)
        convolution.__name = "Convolution"

        for i in range(0, counts_in_convolution):
            window = duplicate.__values[i:amount_of_counts_in_trace + i]  # convoluting part
            # print(window)
            # print(flipped)
            sum = np.dot(window, flipped)
            convolution.__values = np.append(convolution.__values, sum)
        return convolution

        # OLD CODE BELOW
        # def conv(self, other):
        #     """ Function that convolves traces with same boarders and step """
        #     # На всякий случай для себя. Проверка предыдущего кода на отлов неправильных бордеров
        #     if (self.__boarders[1] - self.__boarders[0]) % self.__t_step != 0:
        #         print("ALARM!!!")
        #
        #     amount_of_counts_in_trace_1 = int(
        #         (self.__boarders[1] - self.__boarders[0]) / self.__t_step) + 1  # [0,1], step = 0.5, counts = 3
        #     # amount_of_counts_in_trace_2 = int((other.__boarders[1] - other.__boarders[0]) / other.__t_step)
        #     counts = amount_of_counts_in_trace_1 + amount_of_counts_in_trace_1 - 1
        #
        #     duplicate = self.copy_this()
        #     new_left_boarder = duplicate.__boarders[0] - amount_of_counts_in_trace_1 * duplicate.__t_step
        #     new_right_boarder = duplicate.__boarders[1] + amount_of_counts_in_trace_1 * duplicate.__t_step
        #     duplicate.resize([new_left_boarder, new_right_boarder])
        #
        #     flipped = np.flip(other.__values)
        #     convolution_boarders = [0, int(counts * duplicate.__t_step)]
        #     convolution = Traces(convolution_boarders, duplicate.__t_step)
        #
        #     sum = 0
        #     # print(duplicate.__values)
        #     # print(flipped)
        #     for i in range(1,counts + 1):
        #         window = duplicate.__values[i:amount_of_counts_in_trace_1 + i]  # convoluting part
        #         # print(window, " + ", flipped, "\n")
        #         sum = np.dot(window, flipped)
        #         convolution.__values = np.append(convolution.__values, sum)
        #     return convolution

    def noise(self, math_exp, standard_deviation, paint=None):

        Noise = Traces(self.__boarders, self.__t_step)
        Noise.__name = "Noise"
        Noise.__values = np.append(Noise.__values, [rnd.gauss(math_exp, standard_deviation) for _ in self.makeGrid()])

        if isinstance(paint, Traces):
            Noise = Traces.conv(self, Noise)

        return Noise

    def reflectance(self):
        """ Make reflecting power of geological environment (создает грёбну)"""
        Reflectance = Traces(self.__boarders, self.__t_step)
        Reflectance.__name = "Reflectance"
        Reflectance.__values = np.append(Reflectance.__values, [rnd.uniform(-1, 1) for _ in self.makeGrid()])
        return Reflectance


# f1 = Traces([-1, 1], 0.5).make(np.sin)
# f2 = Traces([-1, 1], 0.5).make(fn.id)
# f3 = Traces.conv(f1, f2)

# f1 = Traces([0, 10], 0.5)

# print(f1.name)
# f3 = f1+f2

# print(dir(mn))
# print(f1.__boarders)
# mn.show([f1,f2])
# a = np.convolve(f1.__values, f2.__values)
# print(f3.__values, "\n", a, "\n\n\n")
# print(f2.__values)
# f2.resize([-0.5, 0.5])
# print(f2.__values)

# print(f1.makeGrid())
