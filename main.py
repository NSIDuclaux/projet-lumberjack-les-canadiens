
import pyxel as p
from random import randint

class Jeu:

    def __init__(self):
        p.init(256, 256, "LumberJackGame")
        p.load("res.pyxres")

        self.score = 0
        self.nb_vies = 3

        self.liste_troncs = list()

        for k in range(12):
            self.ajoute_branche()

        p.run(self.update, self.draw)


    def ajoute_branche(self):
        infos = {
            "branche": bool(randint(0, 1)),
            "droit": bool(randint(0, 1))
        }

        if self.liste_troncs == []:
            self.liste_troncs.append([infos["branche"], infos["droit"], 112, 196])
        else:
            self.liste_troncs.append([infos["branche"], infos["droit"], 112, self.liste_troncs[-1][3] - 16])


    def update(self):
        pass


    def draw(self):
        # Fond
        p.cls(6)
        p.rect(0, 212, 256, 64, 11)

        # Score / Vies
        p.rect(0, 0, 256, 20, 0)
        p.text(7, 7, "Score : " + str(self.score), 7)

        for k in range(self.nb_vies):
            p.blt(238 - k * 16 - 4, 2, 0, 0, 0, 16, 16, 5)

        # Nuages

        # Tronc 
        for tr in self.liste_troncs:
            if tr[0]:
                if tr[1]:
                    #pass
                    p.rect(tr[2], tr[3], 32, 16, 4)
                    #p.blt(tr[2], tr[3], 0, x, y, w, h, 5)
                else:
                    p.rect(tr[2], tr[3], 32, 16, 4)
                    #p.blt(tr[2], tr[3], 0, x, y, w, h, 5)
                    #pass
            else:
                p.rect(tr[2], tr[3], 32, 16, 4)
                #p.blt(tr[2], tr[3], 0, x, y, w, h, 5)
                #pass

        # Cailloux
        p.blt(108, 199, 0, 16, 0, 16, 16, 5)
        p.blt(118, 200, 0, 32, 0, 16, 16, 5)
        p.blt(132, 199, 0, 48, 0, 16, 16, 5)

        # Bucheron

        
Jeu()