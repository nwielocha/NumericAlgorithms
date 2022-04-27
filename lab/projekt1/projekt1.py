import PySimpleGUI as sg
from sympy import *
from backend import Estimation, Lagrange
import math
sg.theme('Reddit')   # Uzywany motyw
# Layout twojego programu


layout = [  [sg.Text('Program pozwalający na obliczenie logarytmu  za pomocą wielomianów interpolujących funkcję z tabeli podanej poniżej:')],
            [sg.Image(r'C:\Users\Rfrev\alg\wykres.png')],
            [sg.Text('Podaj liczbę której wartość chcesz obliczyć dla wielomianu Lagrange powstałego na podstawie wyżej pokazanej tabeli.')],
            [sg.Text('Liczby z przedziału 1-2048'),sg.Input(key='key1'),sg.Button('Oblicz'),],
            [sg.Text('Za pomocą tego programu możesz również sprawdzić eksperymentalnie jaki podzbiór danych z tabelki daje najlepsze \nprzybliżenie dokładnej wartości logarytmu o podstawie 2 z wartosci podanej wyzej. Zaznacz pola wartości X które chcesz \n uwzględnić w swoim eksperymentalnym wyliczeniu:')],
            [sg.Checkbox('1', default=False,key='1'), sg.Checkbox('2', default=False,key='2'),sg.Checkbox('4', default=False,key='4'),sg.Checkbox('8', default=False,key='8'),sg.Checkbox('16', default=False,key='16'),sg.Checkbox('32', default=False,key='32'),sg.Checkbox('64', default=False,key='64'),sg.Checkbox('128', default=False,key='128'),sg.Checkbox('256', default=False,key='256'),sg.Checkbox('512', default=False,key='512'),sg.Checkbox('1024', default=False,key='1024'),sg.Checkbox('2048', default=False,key='2048')],
            [sg.Button('Sprawdź'),sg.Button('Najlepsze przybliżenie')],
            [sg.Output(size=(98, 20))],
            ]

# Zainicjowanie zmiennej lagrange potrzebnej do dalszych obliczen
lagrange=Lagrange({2 ** i:i for i in range(0, 12)})
# Utworzenie okna na podstawie layoutu

window = sg.Window('Projekt I - Zespół R', layout)
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
            print(type(p))
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
    if event == 'Sprawdź':
        if(values['key1'].isdigit()):
            p=int(values['key1'])
            if(p>=1 and p<=2048):
                lista = [ int(key) for key,value in values.items() if value and key!='key1']
                if(len(lista)>1):
                    wielomian=lagrange.create_polynomial(lista)
                    estymacja=Estimation(lista,wielomian,p)
                    wartosc=estymacja.estimated_value
                    print('Dany podzbiór: x={} Przybliżona wartość log2 z {}: {} Błąd przybliżenia: {:.6f}'.format(lista,p,wartosc,math.log(p,2)-wartosc))
                    x=Symbol('x')

                    plot(estymacja.polynomial,(x,-100,100),xlim=[-100,100],ylim=[-100,100],title='Wielomian: {} \nWartość wielomianu dla {}: {}\n'.format(estymacja.polynomial,p,wartosc))
                else:
                    sg.PopupError('Za mała liczba węzłów, zaznacz conajmniej 2 węzły.')
            else:
                sg.PopupError('Podaj liczbę w zakresie od 1 do 2048.')
        else:
            sg.PopupError('"{}" to nie liczba.' .format(values['key1']))



#Zamkniecie okna jesli uzytkownik kliknie przycisk X
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
window.close()
