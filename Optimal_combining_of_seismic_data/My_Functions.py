
def id(x):
    """ Identity function """
    return x

def linear(k, b):
    x = id()
    return k * x + b


class Person:
    def __init__(self, name):
        self.__name = name  # устанавливаем имя
        self.__age = int()  # устанавливаем возраст

    # def set_age(self, age):
    #     if 1 < age < 110:
    #         self.__age = age
    #     else:
    #         print("Недопустимый возраст")
    #
    # def get_age(self):
    #     return self.__age
    #
    # def get_name(self):
    #     return self.__name
    #
    # def display_info(self):
    #     print(f"Имя: {self.__name}\tВозраст: {self.__age}")
# a = Person("ivan")
# a.lol = 123213
# print(a.lol)