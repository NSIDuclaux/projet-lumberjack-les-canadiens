
import pyxel as p
from random import randint
from time import *

class Branche:

    def __init__(self, y):
        self.y = y
        position = randint(0,1)
        if position == 0:
            self.x = 16
        else :
            self.x = 64

class Jeu:

    def __init__(self):
        self.width = 128
        self.height = 224
        p.init(self.width, self.height, title = 'LumberJackGame', quit_key = p.KEY_ESCAPE, fps = 30)
        p.load("res.pyxres")
    
        self.carre_state = False

        self.score = 0
        self.nb_vies = 3

        self.x_personnage = 20
        self.y_personnage = 176


        self.hauteur_branche = 96
        self.liste_branches = list()

        self.liste_branches.append(None)
        self.liste_branches.append(None)
        

        for k in range(6):
            self.ajoute_branche()
            
        p.run(self.update, self.draw)


    def ajoute_branche(self):
        proba = randint(1, 3)
        if proba != 3:
            self.liste_branches.append(Branche(self.hauteur_branche))
            self.hauteur_branche -= 64
        else:
            self.liste_branches.append(None)


    def coupe_tronc(self):
        if p.btn(p.KEY_LEFT):
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 64, 16, 16, 6)
            sleep(0.2)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 96, 16, 16, 6)
            sleep(0.05)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 32, 16, 16, 6)
        if p.btn(p.KEY_RIGHT):
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 48, 16, 16, 6)
            sleep(0.2)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 80, 16, 16, 6)
            sleep(0.05)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 16, 16, 16, 6)


    def collisions(self):
        if p.btnp(p.KEY_LEFT):
            self.cycle_branche("gauche")
        if p.btnp(p.KEY_RIGHT):
            self.cycle_branche("droite")


    def cycle_branche(self, cote):
        if self.liste_branches[0] is not None:
            if (cote == "droite" and self.liste_branches[0].x == 64) or (cote == "gauche" and self.liste_branches[0].x == 16):
                self.nb_vies -= 1
            else:
                self.score += 1

        self.hauteur_branche += 32 

        for br in self.liste_branches :
            if br is not None:
                br.y += 32
                
        self.liste_branches.pop(0)
        self.ajoute_branche()

        while len(self.liste_branches) < 8:
            self.ajoute_branche()


    def test_branches(self):
        for br in self.liste_branches:
            if br is not None:
                if br.y >= 192:
                    self.liste_branches.remove(br)


    def update(self):
        self.collisions()
        self.test_branches()


    def draw(self):
        # Fond
        p.cls(6)
        p.rect(0, 192, 128, 40, 11)

        # Tronc 
        p.blt(48, 192, 0, 16, 48, 32, 16, 6)        
        p.blt(56, 80, 0, 0, 16, 16, 112, 6)
        p.blt(56, 0, 0, 0, 16, 16, 80, 6)

        # Branches
        for br in self.liste_branches:
            if br is not None:
                p.blt(br.x + 8, br.y, 0, 16, br.x, 32, 32, 6)

        # Score / Vies
        p.blt(0, 0, 0, 16, 0, 32, 16, 6)
        p.text(10, 6, str(self.score), 0)

        for k in range(self.nb_vies):
            p.blt(110 - k * 14, 2, 0, 0, 0, 16, 16, 6)

        if self.carre_state:
            p.rect(0, 0, 50, 50, 0)
        
        
Jeu()