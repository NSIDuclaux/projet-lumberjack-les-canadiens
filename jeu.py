
import pyxel as p
from random import randint

class Branche:

    def __init__(self, x, y):
        self.existe = bool(randint(0, 1))
        self.cote = ["gauche", "droite"][randint(0,1)]
        self.x = x
        self.y = y



class Jeu:

    def __init__(self):
        p.init(128, 224, "LumberJack Game")
        p.load("res.pyxres")

        self.score = 0
        self.nb_vies = 3

        p.run(self.update, self.draw)


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


Jeu()