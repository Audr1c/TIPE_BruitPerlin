## Importations

import time
import os
from matplotlib.colors import ListedColormap
import imageio
from tqdm import trange, tqdm
from HeightMap import *
from Grotte import *
from nbtschematic import SchematicFile

## Carte

def Patron_carte(BruitP2D):
    Liste_o = []
    sable = []
    CarteListe3D = [[[1 for y in range(taille)] for z in range(hauteur)] for x in range(taille)]

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
                CarteListe3D[x][z-1][y] = 15
            if z < Hneige - 10:
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

def in_Patron(x, y, z):
    return 0<=x<taille and 0<=y<taille and 0<=z<hauteur

## Images

def sauvegarder_grille(grille: list, i, nom_de_fichier: str) -> None:
    echelle = ListedColormap(['#d7edf8', 'gray', '#007412', 'brown', 'blue', 'yellow', 'black', 'red', '#00fdbd', 'gold', '0.3', 'white','#c9d279','#095a03','#642100','0.4'], 15)
    plt.matshow(grille, cmap=echelle, vmin=0, vmax=15)
    plt.title(f"Frame n°{i}")
    plt.xlabel('y')
    plt.ylabel('z')
    plt.savefig(nom_de_fichier)
    plt.close()

def frames(CarteListe3D):
    for i in trange(taille):
        sauvegarder_grille(CarteListe3D[i], i, f"Overworld/Frame/TIPE{i}.jpg")
        plt.close()

def gif():
    frames = []
    for i in trange(taille):
        file_name = f"Overworld/Frame/TIPE{i}.jpg"
        if os.path.exists(file_name):
            image = imageio.v2.imread(file_name)
            os.remove(file_name)
        else:
            raise Exception(f"File Not found {file_name}")
        frames.append(image)
    imageio.mimsave(f"Overworld/GIF_Map.gif", frames, duration=20)

## Minerais

def diamant(C, x, z, y):
    for j in range(2):
        for k in range(2):
            for i in range(2):
                if C[x+i][z+k][y+j]==1 and random.random()<0.4:
                    C[x+i][z+k][y+j] = 8

def charbon(C, x, z, y):
    Xc1=[]
    Yc1=[]
    Zc1=[]
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 6
                    Xc1.append(x)
                    Yc1.append(y)
                    Zc1.append(z)
    return Xc1, Yc1, Zc1

def redstone(C, x, z, y):
    for j in range(3):
        for k in range(3):
            for i in range(3):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 7

def iron(C, x, z, y):
    Xc1=[]
    Yc1=[]
    Zc1=[]
    for j in range(2):
        for k in range(2):
            for i in range(2):
                if C[x+i][z+k][y+j]==1 and random.random()<0.6:
                    C[x+i][z+k][y+j] = 12
                    Xc1.append(x)
                    Yc1.append(y)
                    Zc1.append(z)
    return Xc1, Yc1, Zc1

def gold(C, x, z, y):
    for j in range(1):
        for k in range(1):
            for i in range(1):
                if C[x+i][z+k][y+j]==1 and random.random()<0.5:
                    C[x+i][z+k][y+j] = 9

def minerais(CarteListe3D, ax):
    NdC = ((taille**2)//(Chunks**2))

    # charbon
    print("charbon")
    NbMn = 11*NdC
    _, Yc = liste_aleatoire(NbMn)
    _, Xc = liste_aleatoire(NbMn)
    _, Zc = liste_aleatoire(NbMn)
    Zc *= hauteur-4
    Yc *= taille
    Yc -= 4
    Xc *= taille
    Xc -= 4
    X = []
    Y = []
    Z = []
    for i in trange(NbMn):
        x, y, z = charbon(CarteListe3D, int(Xc[i]), int(Zc[i]), int(Yc[i]))
        X +=x
        Y +=y
        Z +=z
    Xc = X
    Yc = Y 
    Zc = Z

    # redstone
    print("redstone")
    NbMn = 4*NdC
    _, Yr = liste_aleatoire(NbMn)
    _, Xr = liste_aleatoire(NbMn)
    _, Zr = liste_aleatoire(NbMn)
    Zr *= hauteur//5
    Zr += 4*(hauteur//5)-4
    Yr *= taille
    Yr -= 4
    Xr *= taille
    Xr -= 4
    for i in trange(NbMn):
        redstone(CarteListe3D, int(Xr[i]), int(Zr[i]), int(Yr[i]))

    # fer
    print("fer")
    NbMn = 8*NdC
    _, Yi = liste_aleatoire(NbMn)
    _, Xi = liste_aleatoire(NbMn)
    _, Zi = liste_aleatoire(NbMn)
    Zi *= hauteur//2
    Zi += (hauteur//2)-4
    Yi *= taille
    Yi-= 4
    Xi *= taille
    Xi -= 4

    X = []
    Y = []
    Z = []
    for i in trange(NbMn):
        x, y, z = iron(CarteListe3D, int(Xi[i]), int(Zi[i]), int(Yi[i]))
        X +=x
        Y +=y
        Z +=z
    Xi = X
    Yi = Y 
    Zi = Z
    # or
    print("or")
    NbMn = 4*NdC
    _, Yo = liste_aleatoire(NbMn)
    _, Xo = liste_aleatoire(NbMn)
    _, Zo = liste_aleatoire(NbMn)
    Zo *= hauteur//4
    Zo += 3*(hauteur//4)-4
    Yo *= taille
    Yo-= 4
    Xo *= taille
    Xo -= 4
    for i in trange(NbMn):
        gold(CarteListe3D, int(Xo[i]), int(Zo[i]), int(Yo[i]))

    # diamant
    print("diamant")
    NbMn = 2*NdC
    _, Yd = liste_aleatoire(NbMn)
    _, Xd = liste_aleatoire(NbMn)
    _, Zd = liste_aleatoire(NbMn)
    Zd *= hauteur//5
    Zd += 4*(hauteur//5)-4
    Yd *= taille
    Yd-= 4
    Xd *= taille
    Xd -= 4
    for i in trange(NbMn):
        diamant(CarteListe3D, int(Xd[i]), int(Zd[i]), int(Yd[i]))

    ax.scatter(Xr, Yr, Zr, c='red', s=0.7)
    ax.scatter(Xi, Yi, Zi, c='gray', s=0.7)
    ax.scatter(Xo, Yo, Zo, c='gold', s=0.8)
    ax.scatter(Xc, Yc, Zc, c='black', s=0.4)
    ax.scatter(Xd, Yd, Zd, c='aqua', s=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()

    ax.set_title('Minerai 3D')
    plt.savefig("Overworld/Minerai")

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

    _, Xg = Bruit_de_Grotte_sin(NbPt, fr, amplitude_G, NdBG)
    _, Zg = Bruit_de_Grotte_sin(NbPt, fr, amplitude_G, NdBG)
    _, Yg = Bruit_de_Grotte_sin(NbPt, fr, amplitude_G, NdBG)
    Xg += randrange(taille-2*amplitude_G)
    Yg += randrange(taille-2*amplitude_G)
    Zg += 30

    ax.scatter(Xg, Yg, Zg, s=.8)

    for i in range((NbPt - 1) * fr + 1):
        Explose(CarteListe3D, int(Xg[i]), int(Zg[i]+150), int(Yg[i]))

def Grotte_3D(ax):

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.invert_zaxis()

    ax.set_title('Grotte 3D')
    plt.savefig("Overworld/Grotte")

## Eau

def Eau(CarteListe3D, Liste_o): # Transforme tous les blocs de Liste_o en eau
    for e in tqdm(Liste_o):
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
    while Robinet:    # Percolation tant que tous les voisins ne sont pas remplis
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
        if C[x][z - 1][y] == 0 and z > Heau and OverFlow:
            Robinet.append((x, y, z - 1))
            C[x][z - 1][y] = 4
        Robinet.pop(0)  # Enlève l'élément qui a été étudié pour que la boucle finisse
        print(f"\r Longueur de Robinet : {len(Robinet)}", end="")

## Arbre

def Liste_arbre():
    L_arbre=[]
    Bruit_arbre=Perlin(10, taille//Chunks, taille//Chunks)
    Bruit_arbre += 0.5
    Bruit_arbre *= 4
    for i in trange(taille//Chunks):
        for j in range(taille//Chunks):
            L_arbre_chuck=[]
            arbre=0
            d=Bruit_arbre[i,j]*4
            while arbre < d:
                x=i*Chunks+randrange(Chunks)
                y=j*Chunks+randrange(Chunks)
                if (x,y) not in L_arbre:
                    L_arbre_chuck.append((x,y))
                    arbre+=1
            L_arbre+=L_arbre_chuck
    orig_map=plt.colormaps['gray']
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

def Plantation(C, L_arbre, BdP, Cat):
    for (x,y) in tqdm(L_arbre):
        z=int(BdP[x,y])
        if z<Heau-3:
                Ecosia(C, x, y, BdP, Cat)

    echelle = ListedColormap(['#141872','#0970a6', '#119fe9','#eeec7e', '#5df147', '#38be2a','#336e1c','#004704','white'], 8)
    plt.close("all")
    plt.imshow(Cat, origin='upper', cmap=echelle, vmin=0, vmax=8)
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.title('Carte au Trésor')
    plt.savefig(f"Overworld/Carte_au_Trésor.jpg")

def Ecosia(C, x, y, BdP, Cat):
    z=int(BdP[x,y])
    coin_1=[(2, 2), (-2, 2), (2, -2), (-2, -2)]
    coin_2=[(1, 1), (-1, 1), (1, -1), (-1, -1)]
    
    # Tronc 
    hauteur_arb = randrange(4,8) # [4,7]
    for _ in range(hauteur_arb):
        z-=1
        C[x][z][y]=14
    Cat[x][y]=7
    # Feuilles bas
    for k in range(1,3):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (random.random()<2/3 or not (i,j) in coin_1) and in_Patron(x+i, y+j, z+k) and (i,j)!=(0,0):
                        C[x+i][z+k][y+j]=13
                        Cat[x+i][y+j]=7


    # Feuilles hauts
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (random.random()<1/4 or not (i,j) in coin_2) and in_Patron(x+i, y+j, z-1) and (i,j)!=(0,0):
                    C[x+i][z][y+j]=13
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i,j) not in coin_2 and in_Patron(x+i, y+j, z-1):
                    C[x+i][z-1][y+j]=13

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
                    11: 80,  # Snow block
                    12: 15,  # Iron
                    13 : 18,  # Leaves
                    14 : 17,  # Wood
                    15 : 78  # Snow
                    }

def CreteMapSchem(grid: list, deltaX: int, deltaY: int, deltaZ: int, graine):
    sf = SchematicFile(shape=(deltaZ, deltaY, deltaX))  # z = hauteur faux mais pas grave
    for x in trange(deltaX):
        for y in range(deltaY):
            for z in range(deltaZ):
                sf.blocks[z, y, x] = correspondanceID[grid[x][-z - 1][y]]  # carte renversé
    sf.save(f'Overworld/Map_Overworld.schematic')

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
    BdP, Cat = Bruit_de_map(graine, taille, pixels, precsision, amplitude)
    print(f"End Bruit Perlin : {time.time() - start:.2f} s")
    print('')

    # Patron
    start = time.time()
    print("Start Patron")
    Map, Liste_sable, Liste_o = Patron_carte(BdP)
    print(f"End Patron : {time.time() - start:.2f} s")
    print('')

    # Minerai
    start = time.time()
    print("Start Minerai")
    plt.close("all")
    ax = plt.axes(projection="3d")
    minerais(Map, ax)
    print(f"End Minerai : {time.time() - start:.2f} s")
    print('')

    # Grotte
    start = time.time()
    plt.close("all")
    print("Start Grotte")
    ax = plt.axes(projection="3d")
    for _ in trange(nbGrotte):
        Grotte(Map, ax)
    Grotte_3D(ax)
    print(f"End Grotte : {time.time() - start:.2f} s")
    print('')

    # Eau
    start = time.time()
    print("Start Eau")
    Eau(Map, Liste_o)
    Robinet = Troue(Map, Liste_sable)
    Percolation(Map, Robinet)
    print(f"End Eau : {time.time() - start:.2f} s")
    print('')

    # Arbre

    start = time.time()
    print("Start Arbre") 
    L_arbre=Liste_arbre()
    Plantation(Map,L_arbre,BdP,Cat)

    print(f"End Arbre : {time.time() - start:.2f} s")
    print('')

    # Frame
    start = time.time()
    print("Start Frame")
    frames(Map)
    print(f"End Frame : {time.time() - start:.2f} s")
    print('')

    # GIF
    start = time.time()
    print("Start Gif")
    gif()
    print(f"End Gif : {time.time() - start:.2f} s")
    print('')

    # Schematic
    start = time.time()
    print("Start Schematic")
    CreteMapSchem(Map, taille, taille, hauteur, graine)
    print(f"End Schematic : {time.time() - start:.2f} s")
    print('')

    finTime = time.time() - startAll
    print(f"Program Finished in {finTime:.2f} s")
    print('')

## Paramètres de la carte

# Seed et Dimensions
graine = randrange(10000)
taille = 512
hauteur = 256
# Neige, Eau, Arbre, Minerai 
Hneige = 60
Heau = 150
Chunks=16
OverFlow=False
# HeightMap
precsision = 5
amplitude = 128
pixels = 3000
# Grotte
NbPt = 4
fr = 128
amplitude_G=128
NdBG=6
nbGrotte = 20

## Création de la carte

Fait_une_Map(graine)
