# NumericAlgorithms

## Project I

Obliczyć <img src="https://render.githubusercontent.com/render/math?math=\log_2 22"> za pomocą wielomianów interpolujących funkcję z tabeli

|   x  | f(x) |
| ---- | ---- |
| 1    |    0 |
| 2    |    1 |
| 4    |    2 |
| 8    |    3 |
| 16   |   4  |
| 32   |    5 |
| 64   |    6 |
| 128  |   7  |
| 256  |    8 |
| 512  |    9 |
| 1024 |  10  |
| 2048 |   11 |

Sprawdzić eksperymentalnie jaki podzbiór danych z tabelki daje najlepsze
przybliżenie dokładnej wartości logarytmu (czyli dla jakiego zestawu tych węzłów wielomian Lagrange’a przebiega najbliżej punktu <img src="https://render.githubusercontent.com/render/math?math=(22, \(\log_2 22\))">.

## Projekt II

Pobrać od użytkownika punkt startowy \((x_{0}, y_{0})\). Zbadać eksperymentalnie zbieżność metody Newtona dla układu równań

\[
\begin{cases}
    4x^{2}+9y^{2}-16=0\\
    2y^{2}+4y-x+2=0
\end{cases}
\]

Program powinien stwierdzać podejrzewaną zbieżność lub rozbieżność i w przypadku zbieżności podawać przybliżone rozwiązanie układu, do którego zbiega
metoda.

