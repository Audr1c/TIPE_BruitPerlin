## Importaion
import random
from random import randrange

import numpy as np
import matplotlib.pyplot as plt

## Aléatoire

def plus_ou_moins():
    return (-1) ** (random.randint(0, 1))

def random_int():
    return random.randint(0, 3)  # renvoie un entier aléatoire entre 0 et 4

def random1(u):
    return random.random()*u * plus_ou_moins()

## Interpolation

def lissage_sin(k, y, Y, fr):
    dy = 1 / fr  # définition du pas
    deltaY = 0  # initialisation
    for j in range(fr):
        Y[k*fr+j]=(y[k]+ (y[k+1] - y[k]) * (6 * deltaY ** 5 - 15 * deltaY ** 4 + 10 * deltaY ** 3))  # ajout d'ordonné
        deltaY += dy  # passage au point suivant
    # tableau modifie avec effet de bord

def spline_cube(da, db, k, x, y, Y, fr):
    x=list(x)
    a = x[k]
    b = x[k+1]

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
    Q = c1l1 * y[k] + c2l1 * y[k+1] + c3l1 * db + c4l1 * da
    S = c1l2 * y[k] + c2l2 * y[k+1] + c3l2 * db + c4l2 * da
    D = c1l3 * y[k] + c2l3 * y[k+1] + c3l3 * db + c4l3 * da
    F = c1l4 * y[k] + c2l4 * y[k+1] + c3l4 * db + c4l4 * da

    r = (b - a) / fr  # définition du pas
    t = 0  # initialisation
    for i in range(fr):
        o=k*fr+i
        Y[o] = Q * (a + t) ** 3 + S * (t + a) ** 2 + D * (t + a) + F  # ajout d'ordonné
        t += r  # passage au point suivant

## Crach Test

def Crash_Test(Inter, NbPt):
    random.seed(g)  # permet de généreer un suites de points aléatoires
    x = np.linspace(0, Inter, NbPt)  # liste des abcisses ( espacées à inetrvalle régulié )
    u = x[1] - x[0]  # distance entre 2 abcisses concécutives
    y = [random.randint(50, Inter -50)]  # liste des ordonnées, initiées
    for k in range(len(x) - 1):
        a = y[k] + random1(u)
        y.append(a)  # ajouts des autres ordonnées en fonction des précédentes

    return (x, y)

def Crash_Test_spline(Inter, NbPt, fr):
    x, y = Crash_Test(Inter, NbPt)  # liste du bruit
    X = np.linspace(0,Inter,(NbPt-1)*fr+1)  # création de nouvelle liste d'abcisses
    Y = np.linspace(0,Inter,(NbPt-1)*fr+1)  # création de nouvelle liste d'ordonnés
    d1 = plus_ou_moins()*random.random()*(x[2]-x[0])
    d2 = plus_ou_moins()*random.random()*(X[2]-X[0])
    for k in range(NbPt - 1):  # interpolation entre trois points de la liste
        spline_cube(d1, d2, k, x, y, Y, fr)
        d1 = d2
        d2 = plus_ou_moins()*random.random()*(X[2]-X[0])
    Y[-1]=y[-1]
    return X, Y  # liste avec l'interpolation

def Crash_Test_sin(Inter, NbPt, fr):
    _, y = Crash_Test(Inter, NbPt)  # liste du bruit
    X = np.linspace(0,Inter,(NbPt-1)*fr+1)  # création de nouvelle liste d'abcisses
    Y = np.linspace(0,Inter,(NbPt-1)*fr+1)  # création de nouvelle liste d'ordonnés
    for k in range(NbPt - 1):  # interpolation entre trois points de la liste
        lissage_sin(k, y, Y, fr)
    Y[-1]=y[-1]
    return X, Y

def Comparatif_Crash_Test(Inter, NbPt, fr):
    random.seed(g)
    x, y = Crash_Test_spline(Inter, NbPt, fr)
    random.seed(g)
    z, t = Crash_Test(Inter, NbPt)
    random.seed(g)
    u, p = Crash_Test_sin(Inter, NbPt, fr)

    plt.close("all")
    plt.plot(u, p, 'r', label='Interpolation sinusoidale')
    plt.plot(x, y, 'b', label='Interpolation cubique')
    plt.plot(z, t, '* k', label='Points aléatoires')
    plt.title('Crash Test avec 2 interpolations')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc=0)
    plt.savefig("Grotte_et_BdP_1D/Comparatif_Crash_Test")

## Liste aléatoire

def Perlin_1D(NbPt):
    x = np.array(range(NbPt))
    y = np.array([random.random() for _ in range(NbPt)])
    return x, y

def Perlin_1D_spline(NbPt, fr):
    x, y = Perlin_1D(NbPt)  # liste du bruit
    X = np.linspace(0,10,(NbPt-1)*fr+1)  # création de nouvelle liste d'abcisses
    Y = np.linspace(0,10,(NbPt-1)*fr+1)  # création de nouvelle liste d'ordonnés
    d1 = plus_ou_moins()*random.random()*(x[1]-x[0])*1/2
    d2 = plus_ou_moins()*random.random()*(X[1]-X[0])*1/2
    for k in range(NbPt - 1):  # interpolation entre trois points de la liste
        spline_cube(d1, d2, k, x, y, Y, fr)
        d1=d2
        d2 =plus_ou_moins()*random.random()*(x[1]-x[0])*1/2
    Y[-1]=y[-1]
    return X, Y  # liste avec l'interpolation

def Perlin_1D_sin(NbPt, fr):
    _, y = Perlin_1D(NbPt)  # liste du bruit
    X = np.linspace(0,10,(NbPt-1)*fr+1)  # création de nouvelle liste d'abcisses
    Y = np.linspace(0,10,(NbPt-1)*fr+1)  # création de nouvelle liste d'ordonnés
    for k in range(NbPt - 1):  # interpolation entre trois points de la liste
        lissage_sin(k, y, Y, fr)
    Y[-1]=y[-1]
    return X, Y  # liste avec l'interpolation

def Comparatif_Perin_1D(NbPt, fr):
    random.seed(g)
    z, y = Perlin_1D_spline(NbPt, fr)
    random.seed(g)
    x, t = Perlin_1D(NbPt)
    h= np.linspace(0,10,NbPt)
    random.seed(g)
    u, p = Perlin_1D_sin(NbPt, fr)
    
    plt.close("all")
    plt.plot(z, p, 'r', label='Interpolation sinusoidale')
    plt.plot(u, y, 'b', label='Interpolation cubique')
    plt.plot(h, t, '* k', label='Points aléatoires')
    plt.title('Bruit de Perlin en 1D avec 2 Interpolations')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc=0)
    plt.savefig("Grotte_et_BdP_1D/Cubique_VS_Sinusoïdale")

## Fonction final

def Bruit_de_Grotte_sin(NbPt, fr, amplitude, NbBr, save):
    Y=[]
    for _ in range(NbBr):
        x,y=Perlin_1D_sin(NbPt, fr)
        y *=amplitude
        NbPt*=2
        NbPt-=1
        amplitude//=2
        fr//=2
        Y.append(y)
        if save :
            plt.close()
            plt.plot(x, y, 'r')
            plt.title(f'Bruit de Perlin en 1D d amplitude {amplitude}')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.savefig(f"Grotte_et_BdP_1D/Courbes/Courbe_amplitude_{amplitude}")
    if save :
        Y = sum(Y)
        plt.close()
        plt.plot(x, Y, 'r')
        plt.title(f'Bruit de Perlin en 1D')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.savefig(f"Grotte_et_BdP_1D/Bruit_1D")
    return x, Y

def Bruit_de_Grotte_spline(NbPt, fr, amplitude, NbBr):
    Y=[]
    for i in range(NbBr):
        x,y=Perlin_1D_spline(NbPt, fr)
        y *=amplitude
        NbPt*=2
        NbPt-=1
        amplitude//=2
        fr//=2
        Y.append(y)
    return x,sum(Y)

## Paramètre

g = randrange(10000)  # seed généré aléatoirement entr 0 et 10000
random.seed(g)
NbPt = 20  # nombre de points dans l'intervalle choisi aléatoirement
Inter = 100  # taille de l'intervalle des abcisses, ici [0;50]
fr = 64  # nombre de points interpolés
save = True
Bruit_de_Grotte_sin(NbPt, fr, 128, 6, save)