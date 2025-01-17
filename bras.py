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
        
        self.tab_y_tronc = [112, 96, 80, 64, 48, 32, 16]
        self.x_origine_tronc = 48
        self.y_origine_tronc = 192
        
        self.file_tronc = list()
        self.file_tronc.append({"x" : self.x_origine_tronc, 
                                "y" : self.y_origine_tronc, 
                                "img" : self.img, 
                                "branche" : False, 
                                "droit" : False, 
                                "nb" : 0})
        
        self.file_tronc.append({"x" : self.x_origine_tronc, 
                                "y" : self.y_origine_tronc + (len(self.file_tronc) + 1)* self.taille_img, 
                                "img" : self.img, 
                                "branche" : False, 
                                "droit" : False, 
                                "nb" : 1})

        p.run(self.update, self.draw)
    
    def ajoute_tronc(self):
        proba = randint(1, 3)
        nb_tronc = len(self.file_tronc)
        if proba != 3:
            self.file_tronc.append({
                "x": self.x_origine_tronc,
                "y": self.y_origine_tronc + nb_tronc * self.taille_img,
                "img": self.img,
                "branche": True,
                "droit": int(proba),
                "nb": nb_tronc
            })
        else:
            self.file_tronc.append({
                "x": self.x_origine_tronc,
                "y": self.y_origine_tronc + nb_tronc * self.taille_img,
                "img": self.img,
                "branche": False,
                "droit": False,
                "nb": nb_tronc
            })
    def affiche_tronc(self):
        for tronc in self.file_tronc:
            y_position = self.tab_y_tronc[tronc["nb"] % len(self.tab_y_tronc)]
            p.blt(tronc["x"], tronc["y"], tronc["img"], 0, y_position, self.taille_img, self.taille_img, self.trans_font)
            
    def affiche_branches(self):
        for tronc in self.file_tronc:
            if tronc["branche"]:
                if tronc["droit"]:
                    p.blt(tronc["x"], tronc["y"], tronc["img"], 16, 16, self.taille_img * 2, self.taille_img * 2, self.trans_font)
                else:
                    p.blt(tronc["x"], tronc["y"], tronc["img"], 16, 64, self.taille_img * 2, self.taille_img * 2, self.trans_font)
    
    def coupe_tronc(self):
        if p.btn(p.KEY_LEFT):
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 64, 16, 16)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 96, 16, 16)
            p.blt(self.x_personnage, self.y_personnage, 0, 48, 32, 16, 16)
        
        if p.btn(p.KEY_RIGHT):
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 48, 16, 16)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 80, 16, 16)
            p.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 16, 16, 16)

    def update(self):
        pass
        
    def draw(self):
        p.cls(self.trans_font)
        p.rect(0, 192, 128, 40, 11)
        
        self.coupe_tronc()
        self.affiche_tronc()
        self.affiche_branches()
        
        # Affichage du score et des vies
        p.blt(0, 0, 0, 16, 0, 32, 16, 6)
        p.text(10, 6, str(self.score), 0)
        for k in range(self.nb_vies):
            p.blt(110 - k * 14, 2, 0, 0, 0, 16, 16, 6)

Main()
