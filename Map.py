## Importations

import time
import numpy
from numpy.random import rand
from matplotlib.colors import ListedColormap
import imageio
from tqdm import trange
from perlin2DEliott import *
from perlin1DEliott import *
from nbtschematic import SchematicFile

## Carte

def Patron_carte(BruitP2D):
    Liste_o = []
    sable = []
    CarteListe3D = [[[1 for y in range(taille)] for z in range(hauteur)] for x in trange(taille)]

    for x in trange(taille):
        for y in range(taille):
            Hsurface = int(BruitP2D[x, y])
            z = 0
            while z < Hsurface:
                CarteListe3D[x][z][y] = 0
                if z >= Heau:
                    Liste_o.append((x, y, z))
                z += 1
            if z < Hneige:
                CarteListe3D[x][z][y] = 11
            elif z < Heau - 4:
                CarteListe3D[x][z][y] = 2
            else:
                CarteListe3D[x][z][y] = 5
                if z >= Heau:
                    sable.append((x, y, z))
            z += 1
            a = 3
            for i in range(a):
                if z + i >= Heau - 4:
                    CarteListe3D[x][z + i][y] = 5
                else:
                    CarteListe3D[x][z + i][y] = 3
            if random.random() < 1 / 3:
                CarteListe3D[x][hauteur - 3][y] = 10
            if random.random() < 1 / 2:
                CarteListe3D[x][hauteur - 2][y] = 10
            CarteListe3D[x][hauteur - 1][y] = 10

    return CarteListe3D, sable, Liste_o

## Images

def sauvegarder_grille(grille: list, g, i, nom_de_fichier: str) -> None:
    echelle = ListedColormap(['#d7edf8', 'gray', '#007412', 'brown', 'blue', '#e9f05d', 'black', 'red', '#00fdbd', 'gold', '0.3', 'white','#c9d279','#095a03'], 13)
    plt.matshow(grille, cmap=echelle, vmin=0, vmax=13)
    plt.title(f"x={i} g={g}")  # 'x=' + str(i) + ' g=' + str(g)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.savefig(nom_de_fichier)

def frames(CarteListe3D):
    for i in trange(taille):
        sauvegarder_grille(CarteListe3D[i], graine, i, f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        plt.close()

def gif():
    frames = []
    for i in trange(taille):
        image = imageio.v2.imread(f"Affichage_de_la_map/Frame/TIPE{i}.jpg")
        frames.append(image)
    imageio.mimsave(f"Affichage_de_la_map/GIF.gif", frames, duration=7)

## Minerais

def diamant(C, x, z, y):
    for j in range(2):
        for k in range(2):
            for i in range(2):
                if C[x+i][z+k][y+j]==1 and random.random()<0.4:
                    C[x+i][z+k][y+j] = 8

def charbon(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 6

def redstone(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 7

def iron(C, x, z, y):
    for j in range(2):
        for k in range(2):
            for i in range(2):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 12

def gold(C, x, z, y):
    for j in range(1):
        for k in range(1):
            for i in range(1):
                if C[x+i][z+k][y+j]==1 and random.random()<0.5:
                    C[x+i][z+k][y+j] = 9

def minerais(CarteListe3D, ax):
    h = ((taille**2)/2500)

    # charbon
    print("charbon")
    k = int(15*h)
    _, Yc = liste_aleatoire(k, taille - 4, k)
    _, Xc = liste_aleatoire(k, taille - 4, k)
    _, Z = liste_aleatoire(k, hauteur // 2 - 4, k)
    Zc = [i + hauteur // 2 for i in Z]
    for i in trange(k):
        charbon(CarteListe3D, int(Xc[i]), int(Zc[i]), int(Yc[i]))

    # redstone
    print("redstone")
    k = int(11*h)
    _, Yr = liste_aleatoire(k, taille - 4, k)
    _, Xr = liste_aleatoire(k, taille - 4, k)
    _, Z = liste_aleatoire(k, hauteur // 4 - 4, k)
    Zr = [i + 3*(hauteur // 4) for i in Z]
    for i in trange(k):
        redstone(CarteListe3D, int(Xr[i]), int(Zr[i]), int(Yr[i]))

    # fer
    print("fer")
    k = int(11*h)
    _, Yi = liste_aleatoire(k, taille - 3, k)
    _, Xi = liste_aleatoire(k, taille - 3, k)
    _, Z = liste_aleatoire(k, hauteur // 3 - 3, k)
    Zi = [i + 2*(hauteur // 3) for i in Z]
    for i in trange(k):
        iron(CarteListe3D, int(Xi[i]), int(Zi[i]), int(Yi[i]))

    # or
    print("or")
    k = int(8*h)
    _, Yo = liste_aleatoire(k, taille - 2, k)
    _, Xo = liste_aleatoire(k, taille - 2, k)
    _, Z = liste_aleatoire(k, hauteur // 2 - 2, k)
    Zo = [i + hauteur // 2 for i in Z]
    for i in trange(k):
        gold(CarteListe3D, int(Xo[i]), int(Zo[i]), int(Yo[i]))

    # diamant
    print("diamant")
    k = int(5*h)
    _, Yd = liste_aleatoire(k, taille - 2, k)
    _, Xd = liste_aleatoire(k, taille - 2, k)
    _, Z = liste_aleatoire(k, hauteur // 5 - 2, k)
    Zd = [i + 4 * (hauteur // 5) for i in Z]
    for i in trange(k):
        diamant(CarteListe3D, int(Xd[i]), int(Zd[i]), int(Yd[i]))

    ax.scatter(Xr, Yr, Zr, c='red', s=0.7)
    ax.scatter(Xi, Yi, Zi, c='beige', s=0.7)
    ax.scatter(Xo, Yo, Zo, c='gold', s=0.7)
    ax.scatter(Xc, Yc, Zc, c='black', s=0.7)
    ax.scatter(Xd, Yd, Zd, c='aqua', s=0.7)

## Grottes

def Explose(C, x, z, y):

    # regarde si le bloc n'est pas trop près des bords

    if z < 1 or z > hauteur - 2 or y < 1 or y > taille - 2 or x < 1 or x > taille - 2:

        return None

    # fait l'explosion

    else:  # explose un cube de 3*3 autour du cube

        C[x][z][y] = 0
        C[x][z + 1][y] = 0
        C[x][z - 1][y] = 0
        C[x][z + 1][y + 1] = 0
        C[x][z][y + 1] = 0
        C[x][z - 1][y + 1] = 0
        C[x][z + 1][y - 1] = 0
        C[x][z][y - 1] = 0
        C[x][z - 1][y - 1] = 0

        C[x + 1][z][y] = 0
        C[x + 1][z + 1][y] = 0
        C[x + 1][z - 1][y] = 0
        C[x + 1][z + 1][y + 1] = 0
        C[x + 1][z][y + 1] = 0
        C[x + 1][z - 1][y + 1] = 0
        C[x + 1][z + 1][y - 1] = 0
        C[x + 1][z][y - 1] = 0
        C[x + 1][z - 1][y - 1] = 0

        C[x - 1][z][y] = 0
        C[x - 1][z + 1][y] = 0
        C[x - 1][z - 1][y] = 0
        C[x - 1][z + 1][y + 1] = 0
        C[x - 1][z][y + 1] = 0
        C[x - 1][z - 1][y + 1] = 0
        C[x - 1][z + 1][y - 1] = 0
        C[x - 1][z][y - 1] = 0
        C[x - 1][z - 1][y - 1] = 0

        if z != 1 and z != hauteur - 2 and y != 1 and y != taille - 2 and x != 1 and x != taille - 2:  # explose un bloc de 5*5 sans les arretes si le bloc n'est pas trop près des bords

            C[x + 2][z][y] = 0
            C[x + 2][z + 1][y] = 0
            C[x + 2][z - 1][y] = 0
            C[x + 2][z + 1][y + 1] = 0
            C[x + 2][z][y + 1] = 0
            C[x + 2][z - 1][y + 1] = 0
            C[x + 2][z + 1][y - 1] = 0
            C[x + 2][z][y - 1] = 0
            C[x + 2][z - 1][y - 1] = 0

            C[x - 2][z][y] = 0
            C[x - 2][z + 1][y] = 0
            C[x - 2][z - 1][y] = 0
            C[x - 2][z + 1][y + 1] = 0
            C[x - 2][z][y + 1] = 0
            C[x - 2][z - 1][y + 1] = 0
            C[x - 2][z + 1][y - 1] = 0
            C[x - 2][z][y - 1] = 0
            C[x - 2][z - 1][y - 1] = 0

            C[x + 1][z + 2][y + 1] = 0
            C[x - 1][z + 2][y + 1] = 0
            C[x][z + 2][y + 1] = 0
            C[x + 1][z + 2][y] = 0
            C[x - 1][z + 2][y] = 0
            C[x][z + 2][y] = 0
            C[x + 1][z + 2][y - 1] = 0
            C[x - 1][z + 2][y - 1] = 0
            C[x][z + 2][y - 1] = 0

            C[x + 1][z - 2][y + 1] = 0
            C[x - 1][z - 2][y + 1] = 0
            C[x][z - 2][y + 1] = 0
            C[x + 1][z - 2][y] = 0
            C[x - 1][z - 2][y] = 0
            C[x][z - 2][y] = 0
            C[x + 1][z - 2][y - 1] = 0
            C[x - 1][z - 2][y - 1] = 0
            C[x][z - 2][y - 1] = 0

            C[x + 1][z + 1][y + 2] = 0
            C[x - 1][z + 1][y + 2] = 0
            C[x][z + 1][y + 2] = 0
            C[x + 1][z][y + 2] = 0
            C[x - 1][z][y + 2] = 0
            C[x][z][y + 2] = 0
            C[x + 1][z - 1][y + 2] = 0
            C[x - 1][z - 1][y + 2] = 0
            C[x][z - 1][y + 2] = 0

            C[x + 1][z + 1][y - 2] = 0
            C[x - 1][z + 1][y - 2] = 0
            C[x][z + 1][y - 2] = 0
            C[x + 1][z][y - 2] = 0
            C[x - 1][z][y - 2] = 0
            C[x][z][y - 2] = 0
            C[x + 1][z - 1][y - 2] = 0
            C[x - 1][z - 1][y - 2] = 0
            C[x][z - 1][y - 2] = 0

def Grotte(CarteListe3D, ax):

    _, Xg = bruit_de_perlin1D_spline(taille, NbPt, alpha)
    _, Zg = bruit_de_perlin1D_spline(hauteur, NbPt, alpha)
    _, Yg = bruit_de_perlin1D_spline(taille, NbPt, alpha)

    ax.scatter(Xg, Yg, Zg, s=.8)

    for i in range((NbPt - 1) * alpha + 1):
        Explose(CarteListe3D, int(Xg[i]), int(Zg[i]), int(Yg[i]))

def Grotte_3D(ax):

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()

    ax.set_title('Grotte seed=' + str(graine))
    plt.savefig("Affichage_de_la_map/Grotte")

## Eau

def Eau(CarteListe3D, Liste_o): # Transforme tous les blocs de Liste_o en eau
    for e in Liste_o:
            x, y, z = e
            CarteListe3D[x][z][y] = 4

def Troue(C, Liste_sable):
    Robinet = []
    for (x, y, z) in Liste_sable:   # Parcours tous les blocs de sable qui sont juste en dessous de l'eau
        if C[x][z][y] == 0: # Regarde si le bloc a été explosé
            Robinet.append((x, y, z))    # Si oui, ont l'ajoute à Robinet pour qu'il soit remplacé par de l'eau dans la suite
    return Robinet

def Percolation(C, Robinet):
    for (x, y, z) in Robinet:
        C[x][z][y] = 4  # Le change en eau
    while len(Robinet) != 0:    # Percolation tant que tous les voisins ne sont pas remplis
        (x, y, z) = Robinet[0]  # Prends le premier

        # Regarde les voisins, si ils sont vides, on met de l'eau et on les ajoutes à Robinet pour ragarder les voisins des voisins
        if z != hauteur - 1 and C[x][z + 1][y] == 0:
            Robinet.append((x, y, z + 1))
            C[x][z + 1][y] = 4
        if x != 0 and C[x - 1][z][y] == 0:
            Robinet.append((x - 1, y, z))
            C[x - 1][z][y] = 4
        if x != taille - 1 and C[x + 1][z][y] == 0:
            Robinet.append((x + 1, y, z))
            C[x + 1][z][y] = 4
        if y != 0 and C[x][z][y - 1] == 0:
            Robinet.append((x, y - 1, z))
            C[x][z][y - 1] = 4
        if y != taille - 1 and C[x][z][y + 1] == 0:
            Robinet.append((x, y + 1, z))
            C[x][z][y + 1] = 4
        if z - 1 >= hauteur // 3 and C[x][z - 1][y] == 0 and z > Heau and OverFlow:
            Robinet.append((x, y, z - 1))
            C[x][z - 1][y] = 4
        Robinet.pop(0)  # Enlève l'élément qui a été étudié pour que la boucle finisse
        print(f"\r Longueur de Robinet : {len(Robinet)}", end="")
    print()

## Arbre

def Liste_arbre():
    L_arbre=[]
    Bruit_arbre=Perlin(10, (taille**2)//2500, (taille**2)//2500)
    Bruit_arbre += 0.5
    Bruit_arbre *= 4
    for i in range(taille//50):
        for j in range(taille//50):
            arbre=0
            d=Bruit_arbre[i,j]*10
            while arbre < d:
                x=i*50+randrange(50)
                y=j*50+randrange(50)
                if (x,y) not in L_arbre:
                    L_arbre.append((x,y))
                    arbre+=1
    return L_arbre

def Pantation(C,L_arbre,BdP):
    for (x,y) in L_arbre:
        z=int(BdP[x,y])
        if z<Heau-3:
                C[x][z-1][y]=13

## Conversion pour Minecraft

correspondanceID = {
                    0 : 0,  # Air
                    1 : 1,  # Stone
                    2 : 2,  # Grass
                    3 : 3,  # Dirt
                    4 : 9,  # Water
                    5 : 12,  # Sand
                    6 : 16,  # Coal
                    7 : 73,  # Redstone
                    8 : 56,  # Diamond
                    9 : 14,  # Gold
                    10: 7,  # Bedrock
                    11: 80,  # Snow
                    12: 15,  # Iron
                    13: 17  #Wood
                    }

def CreteMapSchem(grid: list, deltaX: int, deltaY: int, deltaZ: int, graine):
    sf = SchematicFile(shape=(deltaZ, deltaY, deltaX))  # z = hauteur faux mais pas grave
    for x in trange(deltaX):
        for y in range(deltaY):
            for z in range(deltaZ):
                sf.blocks[z, y, x] = correspondanceID[grid[x][-z - 1][y]]  # carte renversé
    sf.save(f'OutSchem/Carte{graine}.schematic')

## Fonction final

def Fait_une_Map(graine):
    
    # Timer et parametrage du random
    startAll = time.time()
    random.seed(graine)
    np.random.seed(graine)
    print('')

    print(f"Graine: {graine}")
    print('')

    # Bruit
    start = time.time()
    print("Start Bruit Perlin")
    M  = Bruit_de_map(graine, taille, pixels, precsision, amplitude)
    print(f"End Bruit Perlin TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Patron
    start = time.time()
    print("Start Patron")
    Map, Liste_sable, Liste_o = Patron_carte(M)
    print(f"End Patron TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Minerai
    start = time.time()
    print("Start Minerai")
    plt.close("all")
    ax = plt.axes(projection="3d")
    minerais(Map, ax)
    print(f"End Minerai TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Grotte
    start = time.time()
    print("Start Grotte")
    for _ in trange(nbGrotte):
        Grotte(Map, ax)
    Grotte_3D(ax)
    print(f"End Grotte TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Eau
    start = time.time()
    print("Start Eau")
    Eau(Map, Liste_o)
    Robinet = Troue(Map, Liste_sable)
    Percolation(Map, Robinet)
    print(f"End Eau TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Arbre

    L_arbre=Liste_arbre()
    Pantation(Map,L_arbre,M)

    # Frame
    start = time.time()
    print("Start Frame")
    frames(Map)
    print(f"End Frame TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # GIF
    start = time.time()
    print("Start Gif")
    gif()
    print(f"End Gif TimeToFinish: {time.time() - start:.2f} s")
    print('')

    # Schematic
    start = time.time()
    print("Start Schematic")
    CreteMapSchem(Map, taille, taille, hauteur, graine)
    print(f"End Schematic TimeToFinish: {time.time() - start:.2f} s")
    print('')

    finTime = time.time() - startAll
    print(f"Program Finished in {finTime:.2f} s")
    print('')

## Paramètres de la carte

precsision = 5
amplitude = 128
pixels = 1000
NbPt = 10
alpha = 50
Hneige = 60
Heau = 150
nbGrotte = 8
taille = 500
hauteur = 256
graine = randrange(10000)
OverFlow=False

if pixels < taille:
    raise ValueError("TG")

## Création de la carte

Fait_une_Map(graine)
