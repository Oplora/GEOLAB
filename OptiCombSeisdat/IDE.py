from tkinter import *
from tkinter import ttk


"""
1) Basics https://pythonru.com/uroki/obuchenie-python-gui-uroki-po-tkinter
2) Binding events https://python-course.eu/tkinter/events-and-binds-in-tkinter.php


Сделать интерфейс, в котором можно будет создавать шум, сигнал. Выводить исходный сигнал и шум при нажатии на
соответсвующие кнопки "Показать".
Сделать окошко, на котором будет отображаться текущий сигнал (с шумом, без шума, отфилтрованный, неотфильтрованный - 
не важно, главное что это текущий объект, ск оторым мы работаем). 
"""

window = Tk()
window.geometry('1200x700')
window.title("Добро пожаловать в приложение PythonRu")

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Первая')
tab_control.pack(expand=1, fill='both')
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Second')
tab_control.pack(expand=1, fill='both')

lbl1 = Label(tab1, text='First page')
lbl1.grid(column=0, row=0)
lbl2 = Label(tab2, text='Second page')
lbl2.grid(column=0, row=0)
# menu = Menu(window)
# menu.add_cascade(label='Создание сигнала')
# window.config(menu=menu)
window.mainloop()