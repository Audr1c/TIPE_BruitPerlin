## Importaion
import random
from math import pi
from random import randrange

from numpy import linspace
import matplotlib.pyplot as plt
from math import sin


## Fonctions préliminaires

# Aléatoire

def plus_ou_moins():
    return (-1) ** (random.randint(0, 1))


def random_int():
    return random.randint(0, 3)  # renvoie un entier aléatoire entre 0 et 4


def random1(u):
    return random.random()*4*u * plus_ou_moins()


# Interpolation

def sinusoidal_pair(x1, x2, y1, y2, X, Y, alpha):
    M = (y2 + y1) / 2  # valeur moyenne de l'interpolation
    m = (y2 - y1) / 2  # amplitude du sinus
    w = pi / (x2 - x1)  # frequence du sinus
    phi = w * x1 + pi / 2  # déphasage du sinus
    r = (x2 - x1) / alpha  # definition du pas
    t = 0  # initialisation
    for i in range(alpha):
        X.append(x1 + t)  # ajout d'abcisse
        Y.append(M + m * sin(w * t - phi))  # ajout d'ordonné
        t += r  # passage au point d'après
    return X, Y


def sinusoidal_impair(x1, x2, y1, y2, X, Y, alpha):
    M = (y2 + y1) / 2  # valeur moyenne de l'interpolation
    m = (y2 - y1) / 2  # amplitude du sinus
    w = pi / (x2 - x1)  # frequence du sinus
    phi = w * x1 - pi / 2  # déphasage du sinus
    r = (x2 - x1) / alpha  # definition du pas
    t = 0  # initialisation
    for i in range(alpha):
        X.append(x1 + t)  # ajout d'abcisse
        Y.append(M + m * sin(w * t - phi))  # ajout d'ordonné
        t += r  # passage au point d'après
    return X, Y


def spline_cube(da, db, a, b, A, B, X, Y, alpha):
    # coefficients de la matrice pour que la dérivée en a soit égal à d1
    c = a ** 4 - 4 * b * a ** 3 + 6 * b ** 2 * a ** 2 - 4 * b ** 3 * a + b ** 4

    c1l1 = (2 * b - 2 * a) / c

    c2l1 = (2 * a - 2 * b) / c

    c3l1 = ((a - b) ** 2) / c

    c4l1 = ((a - b) ** 2) / c

    c1l2 = (3 * a ** 2 - 3 * b ** 2) / c

    c2l2 = (3 * b ** 2 - 3 * a ** 2) / c

    c3l2 = (-2 * a ** 3 + 3 * b * a ** 2 - b ** 3) / c

    c4l2 = (-a ** 3 + 3 * b ** 2 * a - 2 * b ** 3) / c

    c1l3 = (6 * a * b ** 2 - 6 * a ** 2 * b) / c

    c2l3 = (6 * a ** 2 * b - 6 * a * b ** 2) / c

    c3l3 = (a ** 4 - 3 * b ** 2 * a ** 2 + 2 * b ** 3 * a) / c

    c4l3 = (b ** 4 - 3 * a ** 2 * b ** 2 + 2 * a ** 3 * b) / c

    c1l4 = (b ** 4 - 4 * a * b ** 3 + 3 * a ** 2 * b ** 2) / c

    c2l4 = (a ** 4 - 4 * b * a ** 3 + 3 * b ** 2 * a ** 2) / c

    c3l4 = (-b * a ** 4 + 2 * b ** 2 * a ** 3 - b ** 3 * a ** 2) / c

    c4l4 = (-a * b ** 4 + 2 * a ** 2 * b ** 3 - a ** 3 * b ** 2) / c

    # coefficients du polynome en faisant le produit matriciel
    Q = c1l1 * A + c2l1 * B + c3l1 * db + c4l1 * da
    S = c1l2 * A + c2l2 * B + c3l2 * db + c4l2 * da
    D = c1l3 * A + c2l3 * B + c3l3 * db + c4l3 * da
    F = c1l4 * A + c2l4 * B + c3l4 * db + c4l4 * da

    r = (b - a) / alpha  # définition du pas
    t = 0  # initialisation
    for i in range(alpha):
        X.append(a + t)  # ajout d'abcisse
        Y.append(Q * (a + t) ** 3 + S * (t + a) ** 2 + D * (t + a) + F)  # ajout d'ordonné
        t += r  # passage au point suivant
    da = db
    return X, Y, da


## Bruit de Perlin


def bruit_de_perlin1D(i, p):  # permet de généreer un suites de points aléatoires
    x = linspace(0, i, p)  # liste des abcisses ( espacées à inetrvalle régulié )
    u = x[1] - x[0]  # distance entre 2 abcisses concécutives
    y = [random.randint(0, i - 1)]  # liste des ordonnées, initiées
    for k in range(len(x) - 1):
        a = y[k] + random1(u)
        y.append(a)  # ajouts des autres ordonnées en fonction des précédentes

    return (x, y)


def liste_aleatoire(i, j, p):
    x = linspace(0, i, p)
    y = [random.randint(0,j-1) for k in range(p)]
    return x, y


# Sinusoidal

def bruit_de_perlin1D_sin(i, g, p, alpha):
    x, y = bruit_de_perlin1D(i, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []  # création de nouvelle liste d'ordonnés
    for k in range(p - 1):  # interpolation entre deux points de la liste
        if k % 2 == 0:
            X, Y = sinusoidal_pair(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
        else:
            X, Y = sinusoidal_impair(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
    return (X, Y)  # liste avec l'interpolation


def liste_aleatoire_sin(i, j, p, alpha):
    x, y = liste_aleatoire(i, j, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []  # création de nouvelle liste d'ordonnés
    for k in range(p - 1):  # interpolation entre deux points de la liste
        if k % 2 == 0:
            X, Y = sinusoidal_pair(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
        else:
            X, Y = sinusoidal_impair(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
    return (X, Y)  # liste avec l'interpolation


def bruit_de_perlin1D_sin_random(i, p, alpha):  # fonction avec une seed aléatoire
    return bruit_de_perlin1D_sin(i, randrange(10000), p, alpha)


# Polynomial

def bruit_de_perlin1D_spline1(i, g, p, alpha):
    x, y = bruit_de_perlin1D(i, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []  # création de nouvelle liste d'ordonnés
    d1 = 0
    d2 = random_int()
    for k in range(p - 1):  # interpolation entre trois points de la liste
        X, Y, d1 = spline_cube(d1, d2, x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
        d2 = plus_ou_moins() * random_int()
    X.append(x[-1])
    Y.append(y[-1])
    return X, Y  # liste avec l'interpolation

def liste_aleatoire_spline1(i, j, p, alpha):
    x, y = liste_aleatoire(i, j, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []
    d1 = 0
    d2 = random_int()
    for k in range(p - 1):  # interpolation entre trois points de la liste
        X, Y, d1 = spline_cube(d1, d2, x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
        d2 = plus_ou_moins() * random_int()
    X.append(x[-1])
    Y.append(y[-1])
    return X, Y  # liste avec l'interpolation


def liste_aleatoire_spline(i, j, p, alpha):
    x, y = liste_aleatoire(i, j, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []  # création de nouvelle liste d'ordonnés
    for k in range(p - 1):  # interpolation entre trois points de la liste
        lissage_bis(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
    X.append(x[-1])
    Y.append(y[-1])
    return X, Y  # liste avec l'interpolation


def bruit_de_perlin1D_spline_random(i, p):  # fonction avec une seed aléatoire
    return bruit_de_perlin1D_spline(i, randrange(10000))


##
def bruit_de_perlin1D_spline(i, g, p, alpha):
    x, y = bruit_de_perlin1D(i, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []  # création de nouvelle liste d'ordonnés
    for k in range(p - 1):  # interpolation entre trois points de la liste
        lissage_bis(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
    X.append(x[-1])
    Y.append(y[-1])
    return X, Y


def lissage_bis(a, b, A, B, X, Y, alpha):
    dx = (b - a) / alpha
    deltaX = 0
    dy = 1 / alpha  # définition du pas
    deltaY = 0  # initialisation
    for j in range(alpha):
        X.append(a + deltaX)  # ajout d'abcisse
        Y.append(A + (B - A) * (6 * deltaY ** 5 - 15 * deltaY ** 4 + 10 * deltaY ** 3))  # ajout d'ordonné
        deltaY += dy  # passage au point suivant
        deltaX += dx
    # tableau modifie avec effet de bord


if __name__ == "__main__":
    ## Test 1

    # Paramètre

    g = randrange(10000)  # seed généré aléatoirement entr 0 et 10000
    i = 100  # taille de l'intervalle des abcisses, ici [0;50]
    p = 25  # nombre de points dans l'intervalle choisi aléatoirement
    alpha = 30  # nombre de points interpolés

    # Fonction

    x, y = bruit_de_perlin1D_spline(i, g, p, alpha)
    z, t = bruit_de_perlin1D(i, p)
    u, p = bruit_de_perlin1D_sin(i, g, p, alpha)

    # Affichage
    plt.close("all")
    plt.plot(z, t, '* k', label='Points aléatoires')
    plt.plot(u, p, 'r', label='Interpolation sinusoidale')
    plt.plot(x, y, 'b', label='Interpolation cubique')
    plt.title('Bruit de Perlin en 1D (seed = ' + str(g) + ')')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc=0)
    plt.savefig("1_Dimension/Bruit_de_Perlin_1D")

    ## Test 2

    # Paramètre

    g = randrange(10000)  # seed généré aléatoirement entr 0 et 10000
    i = 100  # taille de l'intervalle des abcisses, ici [0;50]
    j = 150  # taille de l'intervalle des ordonnées, ici [0;75]
    p = 8  # nombre de points dans l'intervalle choisi aléatoirement
    alpha = 40  # nombre de points interpolés

    # Fonction

    x, y = liste_aleatoire_spline(i, j, p, alpha)
    z, t = liste_aleatoire(i, j, p)
    u, p = liste_aleatoire_sin(i, j, p, alpha)

    # Affichage

    plt.close("all")
    plt.plot(z, t, '* k', label='Points aléatoires')
    plt.plot(u, p, 'r', label='Interpolation sinusoidale')
    plt.plot(x, y, 'b', label='Interpolation cubique')
    plt.title('Bruit de Perlin en 1D (seed = ' + str(g) + ')')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc=0)
    plt.savefig("1_Dimension/liste_aléatoire")
