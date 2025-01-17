import pyxel as p
from random import randint
from time import sleep

class Main:
    def __init__(self):
        width = 128
        height = 224
        p.init(width, height, title = 'LumberJackGame', quit_key = p.KEY_ESCAPE, fps = 30)
        p.load("res.pyxres")

        self.score = 0
        self.nb_vies = 3

        self.x_personnage = 20
        self.y_personnage = 176

        self.img = 0
        self.taille_img = 16
        self.trans_font = 6

        self.liste_branches = list()
        for _ in range(2):
           self.liste_branches.append(None)
        for _ in range(6):
            self.ajoute_branche()

        self.file_tronc = [{"x":48, "y":192, "img": 0, "branche":False, "droit":False, "nb": 0},
{"x":48, "y":192, "img": 0, "branche":False, "droit":False, "nb":1}]
        self.tab_y_tronc = [112, 96, 80, 64, 48, 32, 16]
        for i in range(7):
            self.file_tronc.append(self.tab_y_tronc[i])
        self.x_origine_tronc = 48
        self.y_origine_tronc = 192
        for _ in range(len(self.file_tronc)):
            self.affiche_tronc()
        self.nb_tronc = 7

        p.run(self.update, self.draw)
    
    def ajoute_tronc(self):
        if self.nb_tronc <= 7:
            self.file_tronc.append(None)
    
    def affiche_tronc(self):
        for _ in self.file_tronc:
            p.blt(self.x_origine_tronc, self.y_origine_tronc, self.img, 0, self.file_tronc.pop(0), self.taille_img, self.taille_img, self.trans_font)
            self.nb_tronc += 1

    def ajoute_branche(self):
        proba = randint(1, 3)
        if proba != 3:
            self.liste_branches.append(self.tab_y_tronc[len(self.liste_branches)])
        else:
            self.liste_branches.append(None)
    
    def affiche_branche(self):
        p.blt(self.x_origine_tronc, self.y_origine_tronc, self.img, 0, self.file_tronc.pop(0), self.taille_img, self.taille_img, self.trans_font)

    def coupe_tronc(self):
        if p.btn(p.KEY_LEFT):
            self.nb_tronc -= 1
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 64, 16, 16, 6)
            sleep(0.2)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 96, 16, 16, 6)
            sleep(0.05)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 32, 16, 16, 6)
        
        if p.btn(p.KEY_RIGHT):
            self.nb_tronc -= 1
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 48, 16, 16, 6)
            sleep(0.2)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 80, 16, 16, 6)
            sleep(0.05)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 16, 16, 16, 6)

    def update(self):
        self.ajoute_tronc()
        self.affiche_tronc()
        self.ajoute_branche()
        self.affiche_branche()# A finir
        self.coupe_tronc()
        

    def draw(self):
        p.cls(6)
        p.rect(0, 192, 128, 40, 11)

        p.blt(0, 0, 0, 16, 0, 32, 16, 6)
        p.text(10, 6, str(self.score), 0)
        for k in range(self.nb_vies):
            p.blt(110 - k * 14, 2, 0, 0, 0, 16, 16, 6)

Main()