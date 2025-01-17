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
            
        self.affiche_tronc()

        p.run(self.update, self.draw)
    
    def ajoute_tronc(self):
        proba = randint(1, 3)
        if proba != 3:
            self.file_tronc.append({"x" : self.x_origine_tronc, 
                                    "y" : self.y_origine_tronc + (len(self.file_tronc) + 1)* self.taille_img, 
                                    "img" : self.img, 
                                    "branche" : True, 
                                    "droit" : int(proba), 
                                    "nb" : len(self.file_tronc)})
        else:
            self.file_tronc.append({"x" : self.x_origine_tronc, 
                                    "y" : self.y_origine_tronc + (len(self.file_tronc) + 1)* self.taille_img, 
                                    "img" : self.img, 
                                    "branche" : False, 
                                    "droit" : False, 
                                    "nb" : len(self.file_tronc)})
    
    def affiche_tronc(self):
        for i in range(len(self.file_tronc)):
            p.blt(self.file_tronc[i]["x"], self.file_tronc[i]["y"], self.file_tronc[i]["img"], 0, self.tab_y_tronc[self.file_tronc[i]["nb"] % len(self.tab_y_tronc)], self.taille_img, self.taille_img, self.trans_font)
    
    def affiche_branche(self):
        for tronc in self.file_tronc:
            if tronc["branche"]:
                if tronc["droit"]:
                    p.blt(tronc["x"], tronc["y"], tronc["img"], 16, 16, self.taille_img * 2, self.taille_img * 2, self.trans_font)
                else:
                    p.blt(tronc["x"], tronc["y"], tronc["img"], 16, 64, self.taille_img * 2, self.taille_img * 2, self.trans_font)
    
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

    def update(self):
        self.ajoute_tronc()
        self.affiche_tronc()
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
