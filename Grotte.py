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

def lissage_sin(k, y, Y, alpha):
    dy = 1 / alpha  # définition du pas
    deltaY = 0  # initialisation
    for j in range(alpha):
        Y[k*alpha+j]=(y[k]+ (y[k+1] - y[k]) * (6 * deltaY ** 5 - 15 * deltaY ** 4 + 10 * deltaY ** 3))  # ajout d'ordonné
        deltaY += dy  # passage au point suivant
    # tableau modifie avec effet de bord

def spline_cube(da, db, k, x, y, Y, alpha):
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

    r = (b - a) / alpha  # définition du pas
    t = 0  # initialisation
    for i in range(alpha):
        o=k*alpha+i
        Y[o] = Q * (a + t) ** 3 + S * (t + a) ** 2 + D * (t + a) + F  # ajout d'ordonné
        t += r  # passage au point suivant

## Crach Test

def bruit_de_perlin1D(i, p):  # permet de généreer un suites de points aléatoires
    x = np.linspace(0, i, p)  # liste des abcisses ( espacées à inetrvalle régulié )
    u = x[1] - x[0]  # distance entre 2 abcisses concécutives
    y = [random.randint(50, i -50)]  # liste des ordonnées, initiées
    for k in range(len(x) - 1):
        a = y[k] + random1(u)
        y.append(a)  # ajouts des autres ordonnées en fonction des précédentes

    return (x, y)

def bruit_de_perlin1D_spline(i, p, alpha):
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

def bruit_de_perlin1D_sin(i, p, alpha):
    x, y = bruit_de_perlin1D(i, p)  # liste du bruit
    X = []  # création de nouvelle liste d'abcisses
    Y = []  # création de nouvelle liste d'ordonnés
    for k in range(p - 1):  # interpolation entre trois points de la liste
        lissage_sin(x[k], x[k + 1], y[k], y[k + 1], X, Y, alpha)
    X.append(x[-1])
    Y.append(y[-1])
    return X, Y

## Liste aléatoire

def liste_aleatoire(NbPt):
    x = np.array(range(NbPt))
    y = np.array([random.random() for _ in range(NbPt)])
    return x, y

def liste_aleatoire_spline(p, fr):
    x, y = liste_aleatoire(p)  # liste du bruit
    X = np.linspace(0,10,(p-1)*fr+1)  # création de nouvelle liste d'abcisses
    Y = np.linspace(0,10,(p-1)*fr+1)  # création de nouvelle liste d'ordonnés
    d1 = plus_ou_moins()*random.random()*(x[1]-x[0])
    d2 = plus_ou_moins()*random.random()*(X[1]-X[0])
    for k in range(p - 1):  # interpolation entre trois points de la liste
        spline_cube(d1, d2, k, x, y, Y, fr)
        d1=d2
        d2 =plus_ou_moins()*random.random()*(x[1]-x[0])
    Y[-1]=y[-1]
    return X, Y  # liste avec l'interpolation

def liste_aleatoire_sin(p, fr):
    x, y = liste_aleatoire(p)  # liste du bruit
    X = np.linspace(0,10,(p-1)*fr+1)  # création de nouvelle liste d'abcisses
    Y = np.linspace(0,10,(p-1)*fr+1)  # création de nouvelle liste d'ordonnés
    for k in range(p - 1):  # interpolation entre trois points de la liste
        lissage_sin(k, y, Y, fr)
    Y[-1]=y[-1]
    return X, Y  # liste avec l'interpolation

## Fonction final

def Bruit_de_Grotte_sin(NbPt, fr, amplitude, NbBr):
    Y=[]
    for i in range(NbBr):
        x,y=liste_aleatoire_sin(NbPt, fr)
        y *=amplitude
        NbPt*=2
        NbPt-=1
        amplitude//=2
        fr//=2
        Y.append(y)
    return x,sum(Y)

def Bruit_de_Grotte_spline(NbPt, fr, amplitude, NbBr):
    Y=[]
    for i in range(NbBr):
        x,y=liste_aleatoire_spline(NbPt, fr)
        y *=amplitude
        NbPt*=2
        NbPt-=1
        amplitude//=2
        fr//=2
        Y.append(y)
    return x,sum(Y)

'''
plt.close("all")
plt.plot(z, t, '* k', label='Points aléatoires')
plt.plot(u, p, 'r', label='Interpolation sinusoidale')
plt.plot(x, y, 'b', label='Interpolation cubique')
plt.title('Bruit de Perlin en 1D (seed = ' + str(g) + ')')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend(loc=0)
plt.savefig("Grotte_et_BdP_1D/Bruit_de_Perlin_1D")'''
## Test 1

## Test 2

# Paramètre

g = randrange(10000)  # seed généré aléatoirement entr 0 et 10000
i = 100  # taille de l'intervalle des abcisses, ici [0;50]
j = 150  # taille de l'intervalle des ordonnées, ici [0;75]
p = 8  # nombre de points dans l'intervalle choisi aléatoirement
alpha = 40  # nombre de points interpolés

# Fonction

random.seed(g)
# x, y = liste_aleatoire_spline(p, alpha)
# x,y= Bruit_de_Grotte_spline(4,128,64,8)
random.seed(g)
z, t = liste_aleatoire(p)
h= np.linspace(0,10,p)
random.seed(g)
# u, p = Bruit_de_Grotte_sin(4,128,64,8)
# u, p = liste_aleatoire_sin(p, alpha)
# Affichage

plt.close("all")
# plt.plot(u, p, 'r', label='Interpolation sinusoidale')
# plt.plot(x, y, 'b', label='Interpolation cubique')
# plt.plot(h, t, '* k', label='Points aléatoires')
plt.title('Bruit de Perlin en 1D (seed = ' + str(g) + ')')
plt.xlabel('x')
plt.ylabel('f(x)')
# plt.legend(loc=0)
plt.savefig("Grotte_et_BdP_1D/liste_aléatoire")



# Paramètre

g = randrange(10000)  # seed généré aléatoirement entr 0 et 10000
i = 100  # taille de l'intervalle des abcisses, ici [0;50]
p = 4  # nombre de points dans l'intervalle choisi aléatoirement
alpha = 30  # nombre de points interpolés

# Fonction

random.seed(g)
# x, y = bruit_de_perlin1D_spline(i, p, alpha)
random.seed(g)
z, t = bruit_de_perlin1D(i, p)
random.seed(g)
#u, p = bruit_de_perlin1D_sin(i, p, alpha)

# Affichage
plt.close("all")
plt.plot(z, t, '* k', label='Points aléatoires')
#plt.plot(u, p, 'r', label='Interpolation sinusoidale')
# plt.plot(x, y, 'b', label='Interpolation cubique')
plt.title('Bruit de Perlin en 1D (seed = ' + str(g) + ')')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend(loc=0)
plt.savefig("Grotte_et_BdP_1D/Bruit_de_Perlin_1D")
