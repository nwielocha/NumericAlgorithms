import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import *
import math
from sympy import Matrix, Symbol, Float
from Classes import *

sg.theme('Reddit')   # Uzywany motyw
# Layout twojego programu


def make_win2():
    layout = [[sg.Canvas(size=(500, 500), key='-CANVAS-')],
    [sg.Image(r'legenda.png',size=(500,25))]]
    return sg.Window('Second Window', layout, finalize=True,element_justification='c')


def _clear():
    for item in canvas.get_tk_widget().find_all():
       canvas.get_tk_widget().delete(item)


def create_plot(y,x):
    # x axis value list.
    #kolor jak zbiega do A
    A = np.array([ [0, 0, 255]])
    #kolor jak zbiega do B
    B = np.array([ [0, 255, 0]])
    #kolor jak nie zbiega do żadnej
    C = np.array([ [255, 0, 0]])

    for i in np.arange(-3, 3.1, x):
        for j in np.arange(-3, 3.1, x):
            if(i != 0 or j != 0):
                #tu wstaw kod na sprawdzenie gdzie te punkty zbiegaja
                zbiega = NewtonProcessor.loop_calculations(Point(float(i), float(j)), y);
                if zbiega == 2:
                    plt.scatter(i, j, s=20, c=A/255.0)
                if zbiega == 1:
                    plt.scatter(i, j, s=20, c=B/255.0)
                if zbiega == 0:
                    plt.scatter(i, j, s=20, c=C/255.0)


    # Draw point based on above x, y axis values.
    # Set chart title.
    plt.title("Zbieżność punktów X Y ")
    # Set x, y label text.
    plt.xlabel("X")
    plt.ylabel("Y")
    return plt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

if __name__ == '__main__':
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
            x=Symbol('x')
            y=Symbol('y')
            NewtonProcessor = NewtonMethod(4 * x ** 2 + 9 * y ** 2 - 16,
                                       2 * y ** 2 + 4 * y - x + 2,
                                       x_point=1, y_point=1)
            window2 = make_win2()
            canvas=window2['-CANVAS-']
            p=float(values['key1'])
            p2=float(values['key2'])
            draw_figure(canvas.TKCanvas, create_plot(p,p2))
    #Obliczenie najlepszego przyblizenia dla podanej przez uzytkownika zmiennej z automatycznym doborem wybranych wezlow przez program

    #Obliczenie przyblizenia dla podanej przez uzytkownika zmiennej dla wielomianu lagrange stworzonego na podstawie wycinku podanego przez uzytkownika

    #Zamkniecie okna jesli uzytkownik kliknie przycisk X
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
    window.close()
