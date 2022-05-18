import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import *
from backend import Estimation, Lagrange
import math
sg.theme('Reddit')   # Uzywany motyw
# Layout twojego programu
def create_plot():
    # x axis value list.
    #kolor jak zbiega do A
    A = np.array([ [0, 0, 255]])
    #kolor jak zbiega do B
    B = np.array([ [0, 255, 0]])
    #kolor jak nie zbiega do żadnej
    C = np.array([ [255, 0, 0]])
    for i in np.arange(-3,3,0.5):
        for j in np.arange(-3,3,0.5):
            zbiega=0;
            if zbiega == 2:
                plt.scatter(i, j, s=5, c=A/255.0)
            if zbiega == 1:
                plt.scatter(i, j, s=5, c=B/255.0)
            if zbiega == 0:
                plt.scatter(i, j, s=5, c=C/255.0)
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
layout = [  [sg.Text('Program pozwalający na określenie do kąd zbiegają punkty obliczone za pomocą metody Newtona dla układu równań \n podanego poniżej:  ')],
            [sg.Image(r'uklad.png')],
            #[sg.Text('Podaj punkt startowy [Xo,Yo] dla którego chcesz sprawdzić zbieżnośc metodą Newtona dla układu równań.')],
            #[sg.Text('X z przedziału [-3,3]: '),sg.Input(key='key1',size=(3, 1)),sg.Text('Y z przedziału [-3,3]: '),sg.Input(key='key2',size=(3, 1)),sg.Button('Oblicz'),],
            [sg.Canvas(size=(500, 500), key='-CANVAS-')],
            ]

# Zainicjowanie zmiennej lagrange potrzebnej do dalszych obliczen
lagrange=Lagrange({2 ** i:i for i in range(0, 12)})
# Utworzenie okna na podstawie layoutu

window = sg.Window('Projekt II - Zespół R', layout,finalize=True)
draw_figure(window['-CANVAS-'].TKCanvas, create_plot())
# Zczytywanie zachowan uzytkownika ( czy cos kliknal/wpisal/zakonczyl program)
while True:

    event, values = window.read()
#Obliczenie wartosci podanej przez uzytkownika zmiennej dla wielomianu lagrange stworzonego na podstawie calej tabeli danych
    if event == 'Oblicz':
        if(values['key1'].isdigit()):
            x=int(values['key1'])
            if(x>=1 and x<=2048):
                z=lagrange.estimation_by_value(x)
                text = sg.popup('Przybliżona wartość logarytmu o podstawie 2 z {} to: \n{} '.format(x,z.estimated_value))
            else:
                sg.PopupError('Podaj liczbę w zakresie od 1 do 2048.')
        else:
            sg.PopupError('"{}" to nie liczba.' .format(values['key1']))


#Obliczenie najlepszego przyblizenia dla podanej przez uzytkownika zmiennej z automatycznym doborem wybranych wezlow przez program
    if event == 'Najlepsze przybliżenie':

        if(values['key1'].isdigit()):
            p=int(values['key1'])
            if(p>=1 and p<=2048):
                result=lagrange.best_estimation(p,math.log(p,2))
                print('Dany podzbiór: x={} Przybliżona wartość log2 z {}: {} Błąd przybliżenia: {:.6f}'.format(result.nodes,result.estimated_value,p,math.log(p,2)-result.estimated_value))
                #text = sg.popup('Otrzymany wielomian to:\n {} \n wartość tego wielomianu dla x = 22 to:\n {}'.format(result.polynomial,result.estimated_value))
                x=Symbol('x')
                plot(result.polynomial,(x,-400,400),xlim=[-400,400],ylim=[-400,400],title='Wielomian: {} \nWartość wielomianu dla {}: {}\n'.format(result.polynomial,p,result.estimated_value))
            else:
                sg.PopupError('Podaj liczbę w zakresie od 1 do 2048.')
        else:
            sg.PopupError('"{}" to nie liczba.' .format(values['key1']))

#Obliczenie przyblizenia dla podanej przez uzytkownika zmiennej dla wielomianu lagrange stworzonego na podstawie wycinku podanego przez uzytkownika




#Zamkniecie okna jesli uzytkownik kliknie przycisk X
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
window.close()
