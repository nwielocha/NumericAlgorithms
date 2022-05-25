import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import *
import math
from sympy import Matrix, Symbol, Float
import os.path
from PIL import Image, ImageTk
class Point:

    def __init__(self, x_cord: Float, y_cord: Float):
        self.x = x_cord
        self.y = y_cord


class Crossing:

    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2


class NewtonMethod:

    def __init__(self, equation1, equation2, x_point=None, y_point=None):
        self.equation_1 = equation1
        self.equation_2 = equation2
        self.point = Point(x_point, y_point)

    def create_inverted_derivative_matrix(self) -> Matrix:
        """
        Creates matrix out of two equations passed through constructor.
        Matrix contains two derivatives of each passed equation - calculated by x and y variable
        :return: Matrix of passed equations derivatives
        """
        self.matrix = Matrix([[self.equation_1.diff(Symbol('x')),
                               self.equation_1.diff(Symbol('y'))],
                              [self.equation_2.diff(Symbol('x')),
                               self.equation_2.diff(Symbol('y'))]])
        return self.matrix ** -1

    def sub_variables_for_values(self, point: Point, matrix: Matrix) -> Matrix:
        """
        Substitute variables x,y with given Point coordinates
        :param point: Point object
        :param matrix: Matrix of equations which each element is going to be substituted with given values
        :return: Matrix of values
        """
        for i in range(0, len(matrix)):
            matrix[i] = Float(matrix[i].subs(Symbol('x'), point.x).subs(Symbol('y'), point.y), 4)
        return matrix

    def core_calculation(self, point: Point) -> Matrix:
        """
        Function creates 3 components needed to calculate  next iteration point.
        1st component - Matrix of x and y
        2nd component - Matrix of equations derivatives substituted with x'y from given point
        3rd component - Matrix of equations substituted with x'y from given component
        :param point: Point which is used to perform calculation
        :return: Point object used to calculate next values
        """
        first_component = Matrix([[point.x], [point.y]])
        second_component = self.sub_variables_for_values(point, self.create_inverted_derivative_matrix())
        third_component = Matrix([[self.equation_1],
                                  [self.equation_2]])
        third_component = self.sub_variables_for_values(point, third_component)

        return first_component - (second_component * third_component)

    def loop_calculations(self, point, limit):
        cross_point1 = Point(2, 0)
        cross_point2 = Point(0.2122922239929, -1.3258007243645)
        crossings = Crossing(cross_point1, cross_point2)
        for i in range(0, 10):
            matrix = self.core_calculation(point)
            point = Point(matrix[0], matrix[1])
            if abs(cross_point1.x - point.x) <= limit:
                if abs(cross_point1.y - point.y) <= limit:
                    return 1
            if abs(cross_point2.x - point.x) <= limit:
                if abs(cross_point2.x - point.x) <= limit:
                    return 2

        return 0

sg.theme('Reddit')   # Uzywany motyw
# Layout twojego programu
def make_win2():
    layout = [[sg.Canvas(size=(500, 500), key='-CANVAS-')],
    [sg.Image(r'legenda.png',size=(500,25))]]
    return sg.Window('Second Window', layout, finalize=True,element_justification='c')
def make_win3(filename):
    layout = [[sg.Image(size=(300, 300), key='-IMAGE-')],
    [sg.Image(r'legenda.png',size=(500,25))]]
    return sg.Window('Second Window', layout, finalize=True,element_justification='c')
def _clear():
    for item in canvas.get_tk_widget().find_all():
       canvas.get_tk_widget().delete(item)
def create_plot(y,x,name):
    # x axis value list.
    #kolor jak zbiega do A
    A = np.array([ [0, 0, 255]])
    #kolor jak zbiega do B
    B = np.array([ [0, 255, 0]])
    #kolor jak nie zbiega do żadnej
    C = np.array([ [255, 0, 0]])
    status = 1
    ilosc = np.arange(-3,3.1,x)
    ilosc = len(ilosc)
    ilosc = ilosc * ilosc
    czas = ilosc/100*14/60
    ilosc2=ilosc
    for i in np.arange(-3,3.1,x):
        for j in np.arange(-3,3.1,x):
            if(i!=0 or j!=0):
                status=status+1
                print('Liczę: {}/{} Szacowany czas: {:.2f} minut'.format(status,ilosc,czas))
                ilosc2=ilosc2-1
                czas= ilosc2/100*14/60
                zbiega=NewtonProcessor.loop_calculations(Point(float(i),float(j)),y);
                if zbiega == 2:
                    plt.scatter(i, j, s=10,marker='s', c=A/255.0)
                if zbiega == 1:
                    plt.scatter(i, j, s=10,marker='s', c=B/255.0)
                if zbiega == 0:
                    plt.scatter(i, j, s=10,marker='s', c=C/255.0)


    # Draw point based on above x, y axis values.
    # Set chart title.
    plt.title("Zbieżność punktów X Y ")
    # Set x, y label text.
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(name)
    return plt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
layout = [  [sg.Text('Program pozwalający na określenie do kąd zbiegają punkty obliczone za pomocą metody Newtona dla układu równań \n podanego poniżej:  ')],
            [sg.Image(r'uklad.png')],

            [sg.Image(r'wykres1.png',size=(325,325))],

            #[sg.Text('Podaj punkt startowy [Xo,Yo] dla którego chcesz sprawdzić zbieżnośc metodą Newtona dla układu równań.')],
            #[sg.Text('X z przedziału [-3,3]: '),sg.Input(key='key1',size=(3, 1)),sg.Text('Y z przedziału [-3,3]: '),sg.Input(key='key2',size=(3, 1)),sg.Button('Oblicz'),],
            [sg.Text('Podaj interesujące Cię przybliżenie:'),sg.Input(key='key1',size=(5,1))],
            [sg.Text('Podaj częstotliwość punktów:'),sg.Input(key='key2',size=(5,1)),sg.Button('Oblicz')],
            ]
# Zainicjowanie zmiennej lagrange potrzebnej do dalszych obliczen
# Utworzenie okna na podstawie layoutu

window = sg.Window('Projekt II - Zespół R', layout,finalize=True,size=(750, 550),element_justification='c')

# Zczytywanie zachowan uzytkownika ( czy cos kliknal/wpisal/zakonczyl program)
while True:

    event, values = window.read()
#Obliczenie wartosci podanej przez uzytkownika zmiennej dla wielomianu lagrange stworzonego na podstawie calej tabeli danych
    if event == 'Oblicz':
        name="Gotowe/"
        name = name + values['key1']
        name = name + "_"
        name = name + values['key2']
        name=name+".png"
        print(name)
        file_exist = os.path.exists(name)
        if file_exist:
            window3 = make_win3(name)
            im = Image.open(name)
            image = ImageTk.PhotoImage(image=im)
            window3['-IMAGE-'].update(data=image)
            print("hehe")
        else:
            x=Symbol('x')
            y=Symbol('y')
            NewtonProcessor = NewtonMethod(4 * x ** 2 + 9 * y ** 2 - 16,
                                   2 * y ** 2 + 4 * y - x + 2,
                                   x_point=1, y_point=1)
            window2 = make_win2()
            canvas=window2['-CANVAS-']
            p=float(values['key1'])
            p2=float(values['key2'])
            draw_figure(canvas.TKCanvas, create_plot(p,p2,name))
#Obliczenie najlepszego przyblizenia dla podanej przez uzytkownika zmiennej z automatycznym doborem wybranych wezlow przez program

#Obliczenie przyblizenia dla podanej przez uzytkownika zmiennej dla wielomianu lagrange stworzonego na podstawie wycinku podanego przez uzytkownika




#Zamkniecie okna jesli uzytkownik kliknie przycisk X
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
window.close()
