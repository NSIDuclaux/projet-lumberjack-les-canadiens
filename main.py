
import pyxel as p
from random import randint

class Jeu:

    def __init__(self):
        p.init(128, 224, "LumberJackGame")
        p.load("res.pyxres")

        self.score = 120
        self.nb_vies = 3

        self.x_personnage = 1
        self.y_personnage = 1

        self.liste_branches = list()
        self.liste_branches.append(None)
        self.liste_branches.append(None)

        p.run(self.update, self.draw)


    def ajoute_branche(self):
        proba = randint(1, 3)
        if proba != 3:
            self.liste_branches.append("""Branche()""")
        else:
            self.liste_branches.append(None)


    def coupe_tronc(self):
        if p.btn(p.KEY_LEFT):
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 64, 16, 16, 6)
            p.wait(0.2)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 96, 16, 16, 6)
            p.wait(0.05)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 32, 16, 16, 6)
        if p.btn(p.KEY_RIGHT):
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 48, 16, 16, 6)
            p.wait(0.2)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 80, 16, 16, 6)
            p.wait(0.05)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 16, 16, 16, 6)



    def update(self):
        pass


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
                p.blt(br.x, br.y, 0, 16, br.x, 32, 32, 6)


        # Score / Vies
        p.blt(0, 0, 0, 16, 0, 32, 16, 6)
        p.text(10, 6, str(self.score), 0)

        for k in range(self.nb_vies):
            p.blt(110 - k * 14, 2, 0, 0, 0, 16, 16, 6)
        
        
Jeu()