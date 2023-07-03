# Importations


import time
import os
from math import sqrt
from matplotlib.colors import ListedColormap
import imageio
from tqdm import trange, tqdm
from HeightMap import *
from Grotte import *
from nbtschematic import SchematicFile
from collections import deque


# Carte


def Patron_carte(BdP):
    # Création du tableau servant de support (rempli avec de la pierre) et des listes utiles
    Liste_o = []
    sable = []
    Overworld = [[[1 for y in range(taille)]
                  for z in range(hauteur)] for x in range(taille)]
    # Parcours tout le tableau
    for x in trange(taille):
        for y in range(taille):
            Hsurface = int(BdP[x, y])
            z = 0
            # Pose de l'air jusqu'à atteindre la hauteur définit par le bruit
            while z < Hsurface:
                Overworld[x][z][y] = 0
                # Regarde si le block posé est de l'eau ou non
                if z >= Heau:
                    Liste_o.append((x, y, z))
                z += 1
            # Regarde quel type de block poser une fois la hauteur atteinte
            if z < Hneige:  # Dalle de neige
                Overworld[x][z-1][y] = 15
            if z < Hneige - 10:  # Block de neige
                Overworld[x][z][y] = 11
            elif z < Heau - 4:  # Block d'herbe
                Overworld[x][z][y] = 2
            else:  # Block de sable
                Overworld[x][z][y] = 5
                # Regarde si le bloc de sable est sous l'eau
                if z >= Heau:
                    sable.append((x, y, z))
            z += 1
            # Place des blocks en dessous (3 block)
            a = 3
            for i in range(a):
                if z + i >= Heau - 4:  # Block de sable
                    Overworld[x][z + i][y] = 5
                else:  # Block de terre
                    Overworld[x][z + i][y] = 3
            # Place la bedrock
            if random.random() < 1 / 3:
                Overworld[x][hauteur - 3][y] = 10
            if random.random() < 1 / 2:
                Overworld[x][hauteur - 2][y] = 10
            Overworld[x][hauteur - 1][y] = 10

    return Overworld, sable, Liste_o


def in_Patron(x, y, z):
    # Regarde si les coordonnées du block est dans le tableau ou non
    return 0 <= x < taille and 0 <= y < taille and 0 <= z < hauteur


# Images


def sauvegarder_grille(Overworld, i, nom_du_fichier) -> None:
    # Echelle de couleur pour les différents types de block
    echelle = ListedColormap(['#d7edf8', 'gray', '#007412', 'brown', 'blue', 'yellow', 'black',
                             'red', '#00fdbd', 'gold', '0.3', 'white', '#c9d279', '#095a03', '#642100', '0.4', '#ff4d00','#300a6a'], 17)
    # Affiche, met un titre, sauvegarde
    plt.matshow(Overworld[i], cmap=echelle, vmin=0, vmax=17)
    plt.title(f"Frame n°{i}")
    plt.xlabel('y')
    plt.ylabel('z')
    plt.savefig(nom_du_fichier)
    plt.close()


def frames(Overworld):
    # Enregistre toutes les frames
    for i in trange(taille):
        sauvegarder_grille(Overworld, i, f"Overworld/Frame/TIPE{i}.jpg")
        plt.close()


def gif():
    frames = []
    # Parcours toutes les frames
    for i in trange(taille):
        file_name = f"Overworld/Frame/TIPE{i}.jpg"
        # Regarde si la frame existe
        if os.path.exists(file_name):
            # La supprime des fichier pour alléger la mémoire
            image = imageio.v2.imread(file_name)
            os.remove(file_name)
        else:
            raise Exception(f"File Not found {file_name}")
        # L'ajoute à la liste pour le Gif
        frames.append(image)
    # Fait le Gif
    imageio.mimsave(f"Overworld/GIF_Map.gif", frames, duration=20)


# Minerais


def Filon(Overworld, x, z, y, cote, Id, prob):
    # Listes des blocks qui seront réellement remplacés
    Xd1 = []
    Yd1 = []
    Zd1 = []
    # Parcours un block de 2*2*2 autour de x, y, z
    for j in range(cote):
        for k in range(cote):
            for i in range(cote):
                # Regarde si le block à remplacer est bien de la pierre et le remplace avec une proba de 0.4
                if Overworld[x+i][z+k][y+j] == 1 and random.random() < prob:
                    Overworld[x+i][z+k][y+j] = Id
                    # L'ajoute aux listes des blocks posés
                    Xd1.append(x)
                    Yd1.append(y)
                    Zd1.append(z)
    return Xd1, Yd1, Zd1


def minerais(Overworld, ax):
    # Regarde le nombre de chunks définir le nombre de minerai à placer
    NdC = ((taille**2)//(Chunks**2))
    # Parcours le dictionnaire
    for (cote, Id, densite, position, prob, color, bille) in tqdm(mine):
        NbMn = densite*NdC  # Nombre de minerai dans la map
        # Prend des listes aléatoires dans [0,1] pour les 3 coordonnées des filons
        _, Y = Perlin_1D(NbMn)
        _, X = Perlin_1D(NbMn)
        _, Z = Perlin_1D(NbMn)
        # Ajuste pour avoir les bons intervaux
        Z *= -position
        Z += hauteur-4
        Y *= taille
        Y -= 4
        X *= taille
        X -= 4
        # Listes des blocks réellement placés
        X1 = []
        Y1 = []
        Z1 = []
        # Parcours les listes des minerais et pose les minerais
        for i in range(NbMn):
            x, y, z = Filon(Overworld, int(X[i]), int(Z[i]), int(Y[i]), cote, Id, prob)
            # Ajoute les blocks réellement posés
            X1 += x
            Y1 += y
            Z1 += z
        X = X1
        Y = Y1
        Z = Z1

        ax.scatter(X, Y, Z, c=color, s=bille)

    # Axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()
    # Titre et sauvegarde
    ax.set_title('Minerai 3D')
    plt.savefig("Overworld/Minerai")


# Grottes


def Explose(Overworld, x, z, y):
    t = 2 + (z > 190) + (z > 220)
    for j in range(-t, t+1):
        for k in range(-t, t+1):
            for i in range(-t, t+1):
                # Si le block n'est pas sur une arrête, on l'explose
                if in_Patron(x+i, y+k, z+j) and sqrt(i**2 + j**2 + k**2) < sqrt(2)*t:
                    Overworld[x+i][z+j][y+k] = 16*(z+j>Hlave)


def Grotte(Overworld, ax):
    # Bruit 1D sur chacun des axes dans un cube amplitude_G*amplitude_G*amplitude_G
    _, Xg = Bruit_de_Grotte_sin(NbPt, fr, amplitude_G, NdBG)
    _, Zg = Bruit_de_Grotte_sin(NbPt, fr, hauteur//2, NdBG)
    _, Yg = Bruit_de_Grotte_sin(NbPt, fr, amplitude_G, NdBG)
    # Deplace aléatoirement les grottes pour qu'elles ne soient pas toutes dans amplitude_G*amplitude_G*amplitude_G
    Xg += randrange(taille-amplitude_G)
    Yg += randrange(taille-amplitude_G)
    Zg += 30
    # Affichage
    ax.scatter(Xg, Yg, Zg, s=.8)
    # Explose sur toute la grotte
    for i in range((NbPt - 1) * fr + 1):
        Explose(Overworld, int(Xg[i]), int(Zg[i]), int(Yg[i]))


def Grotte_3D(ax):
    # Axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()
    # Titre et sauvergarde
    ax.set_title('Grotte 3D')
    plt.savefig("Overworld/Grotte")


# Eau


def Eau(Overworld, Liste_o):
    # Parcours Liste_o et transforme tous les blocs en eau
    for (x, y, z) in tqdm(Liste_o):
        Overworld[x][z][y] = 4


def Source(Overworld, Liste_sable):
    Robinet = deque()
    for (x, y, z) in Liste_sable:
        # Si air au lieu de sable
        if Overworld[x][z][y] == 0:
            Robinet.append((x, y, z))
            Overworld[x][z][y] = 4 # eau
    return Robinet


def Percolation(Overworld, Robinet):
    voisin_horiz = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while Robinet:
        (x, y, z) = Robinet.popleft()

        # Voisins Horizontaux
        for (dx, dy) in voisin_horiz:
            X, Z, Y = x + dx, z, y + dy
            if in_Patron(X, Y, Z) and Overworld[X][Z][Y] == 0:
                Robinet.append((X, Y, Z))
                Overworld[X][Z][Y] = 4

        # Voisins Verticaux
        # Au-dessus
        if in_Patron(x, y, z - 1) and Overworld[x][z - 1][y] == 0 and z > Heau and OverFlow:
            Robinet.append((x, y, z - 1))
            Overworld[x][z - 1][y] = 4

        # En dessous
        if in_Patron(x, y, z + 1):
            if Overworld[x][z + 1][y] == 16:  # si Lave
                Overworld[x][z + 1][y] = 17  # Obsidienne
            elif Overworld[x][z + 1][y] == 0:
                Robinet.append((x, y, z + 1))
                Overworld[x][z + 1][y] = 4  # gravité (eau)

        print(f"\r Longueur de Robinet : {len(Robinet)}", end="")
    print('')


# Arbre


def Liste_arbre():
    # Défini la liste des arbres à placer et le bruit utilisé pour la densité d'arbre
    L_arbre = []
    Bruit_arbre = Bruit_Arbres(taille//Chunks, 5)
    # Parcours les chunks
    for i in trange(taille//Chunks):
        for j in range(taille//Chunks):
            L_arbre_chuck = []  # Liste des arbres par chunk
            arbre = int(Bruit_arbre[i, j])  # Nombres d'arbres à poser
            d = arbre
            while arbre:
                L = [(i*Chunks+k, j*Chunks+l) for k in range(Chunks) for l in range(Chunks)]

                # Coordonnées aléatoires dans la chunk
                (x, y)= L.pop(randrange(Chunks**2 - d + arbre))
                L_arbre_chuck.append((x, y))
                arbre -= 1
            L_arbre += L_arbre_chuck
    # Affichage du bruit
    orig_map = plt.colormaps['gray']
    reversed_map = orig_map.reversed()
    plt.close()
    plt.imshow(Bruit_arbre, origin='upper', cmap=reversed_map)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.colorbar()
    plt.title('Bruit des arbres')
    plt.savefig(f"HeightMap_et_BdP_2D/Bruits_2D_arbre.jpg")
    plt.close()
    return L_arbre


def Amazonie(Overworld, L_arbre, BdP, Cat):
    # Parcours L_arbre
    k = 0
    for (x, y) in tqdm(L_arbre):
        k += 1
        z = int(BdP[x, y])
        # Regarde s'il y a de la terre pour placer l'arbre
        if Overworld[x][z][y] == 2:
            # Plante un arbre
            Ecosia(Overworld, x, y, BdP, Cat, k)
    # Affiche CaT avec les arbres
    echelle = ListedColormap(['#141872', '#0970a6', '#119fe9', '#eeec7e',
                             '#5df147', '#38be2a', '#336e1c', '#004704', 'white'], 8)
    plt.close("all")
    plt.imshow(Cat, origin='upper', cmap=echelle, vmin=0, vmax=8)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.title('Carte au Trésor')
    plt.savefig(f"Overworld/Carte_au_Trésor.jpg")


def Ecosia(Overworld, x, y, BdP, Cat, k):
    # Hauteur et listes des coins
    z = int(BdP[x, y])-1
    coin_1 = [(2, 2), (-2, 2), (2, -2), (-2, -2)]
    coin_2 = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    b = 0.1*(k % 10 == 0)

    # Tronc
    hauteur_arb = randrange(4, 8)  # Hauteur du tronc
    for _ in range(hauteur_arb):  # Place le tronc
        z -= 1
        Overworld[x][z][y] = 14 + b
    Cat[x][y] = 7  # Place les feuilles sur CaT

    # Feuilles bas
    for k in range(1, 3):  # Parcours les deux grands anneaux du bas
        for i in range(-2, 3):
            for j in range(-2, 3):
                # Si la feuille est dans un coin, proba de 2/3 d'apparaitre
                if (random.random() < 2/3 or not (i, j) in coin_1) and in_Patron(x+i, y+j, z+k) and (i, j) != (0, 0):
                    Overworld[x+i][z+k][y+j] = 13 + \
                        b  # Feuille dans L'Overworld
                    Cat[x+i][y+j] = 7  # Feuille sur la CaT

    # Feuilles hauts
    for i in range(-1, 2):  # Parcours le petit anneau du bas
        for j in range(-1, 2):
            # Si la feuille est dans un coin, proba de 1/4 d'apparaitre
            if (random.random() < 1/4 or not (i, j) in coin_2) and in_Patron(x+i, y+j, z-1) and (i, j) != (0, 0):
                Overworld[x+i][z][y+j] = 13 + b
    for i in range(-1, 2):  # Parcours le petit anneau du haut
        for j in range(-1, 2):
            # Si la feuille est dans un coin, elle n'apparait pas
            if (i, j) not in coin_2 and in_Patron(x+i, y+j, z-1):
                Overworld[x+i][z-1][y+j] = 13 + b


# Conversion pour Minecraft


correspondanceID = {
    0: 0,  # Air
    1: 1,  # Stone
    2: 2,  # Grass
    3: 3,  # Dirt
    4: 9,  # Water
    5: 12,  # Sand
    6: 16,  # Coal
    7: 73,  # Redstone
    8: 56,  # Diamond
    9: 14,  # Gold
    10: 7,  # Bedrock
    11: 80,  # Snow block
    12: 15,  # Iron
    13: 18, 13.1: 18,  # Leaves
    14: 17, 14.1: 17,  # Wood
    15: 78,  # Snow
    16: 11,  # Lava
    17: 49  # Obsidienne
}


def CreteMapSchem(Overworld):
    sf = SchematicFile(shape=(hauteur, taille, taille))
    for x in trange(taille):
        for y in range(taille):
            for z in range(hauteur):
                val = correspondanceID[Overworld[x][-z - 1][y]]
                sf.blocks[z, x, y] = val

                if val in (18, 17):
                    if val//1 != val:
                        pass
                        # sf.all_tags
    sf.save(f'Overworld/Map_Overworld.schematic')


# Fonction final


def Make_an_Overworld(graine):
    print('')
    print('Start Overworld')

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
    BdP, Cat = Bruit_Overworld(taille, pixels, precsision, amplitude)
    print(f"End Bruit Perlin : {time.time() - start:.2f} s")
    print('')

    # Patron
    start = time.time()
    print("Start Patron")
    Overworld, Liste_sable, Liste_o = Patron_carte(BdP)
    print(f"End Patron : {time.time() - start:.2f} s")
    print('')

    # Minerai
    start = time.time()
    print("Start Minerai")
    plt.close("all")
    ax = plt.axes(projection="3d")
    minerais(Overworld, ax)
    print(f"End Minerai : {time.time() - start:.2f} s")
    print('')

    # Grotte
    start = time.time()
    plt.close("all")
    print("Start Grotte")
    ax = plt.axes(projection="3d")
    for _ in trange(nbGrotte):
        Grotte(Overworld, ax)
    Grotte_3D(ax)
    print(f"End Grotte : {time.time() - start:.2f} s")
    print('')

    # Eau
    start = time.time()
    print("Start Eau")
    Eau(Overworld, Liste_o)
    Robinet = Source(Overworld, Liste_sable)
    Percolation(Overworld, Robinet)
    print(f"End Eau : {time.time() - start:.2f} s")
    print('')

    # Arbre

    start = time.time()
    print("Start Arbre")
    L_arbre = Liste_arbre()
    Amazonie(Overworld, L_arbre, BdP, Cat)
    print(f"End Arbre : {time.time() - start:.2f} s")
    print('')

    # Frame
    start = time.time()
    print("Start Frame")
    # frames(Overworld)
    print(f"End Frame : {time.time() - start:.2f} s")
    print('')

    # GIF
    start = time.time()
    print("Start Gif")
    # gif()
    print(f"End Gif : {time.time() - start:.2f} s")
    print('')

    # Schematic
    start = time.time()
    print("Start Schematic")
    CreteMapSchem(Overworld)
    print(f"End Schematic : {time.time() - start:.2f} s")
    print('')

    finTime = time.time() - startAll
    print(f"End Overworld : {finTime:.2f} s")
    print('')


# Paramètres de la carte


# Seed et Dimensions
graine = randrange(10000)
taille = 1024
hauteur = 256
# Neige, Lave, Eau, Arbre, Minerai
Hneige = 60
Hlave = 230
Heau = 150
OverFlow = False
Chunks = 16
#      (coté, Id, NbFilon, couche, prob, color, bille)
mine = [(4,  6, 20,  hauteur-4, .6, "black", .001), # Charbon
        (3, 12,  8, hauteur//2, .5,  "gray",   .5), # Fer
        (3,  7,  4, hauteur//5, .6,   "red",   .4), # Redstone
        (2,  9,  4, hauteur//4, .5,  "gold",   .7), # Or
        (2,  8,  2, hauteur//6, .4,  "aqua",   .8)] # Diamant
# HeightMap
precsision = 5
amplitude = 128
pixels = 3000
# Grotte
NbPt = 6
fr = 256
amplitude_G = 256
NdBG = 6
nbGrotte = 15


# Création de l'Overworld


Make_an_Overworld(398)
