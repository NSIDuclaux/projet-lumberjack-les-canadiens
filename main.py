
import pyxel as p
from random import randint

class Jeu:

    def __init__(self):
        self.width = 200
        self.height = 160
        pyxel.init(self.width, self.height, title = 'Snake', quit_key = pyxel.KEY_ESCAPE, fps = 30)
    

        self.score = 120
        self.nb_vies = 3

        self.liste_branches = list()

        self.liste_branches.append({"branche": False, "droit": False, "x": 56, "y": 176, "k": 0})
        self.liste_branches.append({"branche": False, "droit": False, "x": 56, "y": 160, "k": 1})
        
        for k in range(2, 5):
            self.ajoute_branche(k)

        p.run(self.update, self.draw)


    def ajoute_branche(self, k):
        proba = bool(randint(0, 4))
        branche = True

        if proba == 0:
            branche = False

        infos = {
            "branche": branche,
            "droit": bool(randint(0, 1)),
            "x": 56,
            "y": int(self.liste_branches[-1]["y"]) - 32,
            "k": k
        }

        self.liste_branches.append(infos)


    def update(self):
        pass


    def draw(self):
        # Fond
        p.cls(6)
        p.rect(0, 192, 128, 40, 11)

        # Score / Vies
        p.blt(0, 0, 0, 16, 0, 32, 16, 6)
        p.text(10, 6, str(self.score), 0)

        for k in range(self.nb_vies):
            p.blt(110 - k * 14, 2, 0, 0, 0, 16, 16, 6)

        # Nuages

        # Tronc 
        p.blt(48, 192, 0, 16, 48, 32, 16, 6)

        for tr in self.liste_branches:
            p.blt(tr["x"], tr["y"], 0, 0, 112 - tr["k"] * 32, 16, 16, 6)

            if tr["branche"]:
                if tr["droit"]:
                    p.blt()
                else:
                    pass
            else:
                pass
        
Jeu()