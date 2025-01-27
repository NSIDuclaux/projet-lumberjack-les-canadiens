import pyxel as p
from random import randint
from vlc import *

class Main:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.width = 99
        self.height = 176
        p.init(self.width, self.height, title='LumberJackGame', quit_key=p.KEY_ESCAPE, fps=30)
        p.load("res.pyxres")

        # Initialisation des variables de jeu
        self.score = 0
        self.nb_vies = 3

        self.img = 0
        self.taille_img = 16
        self.trans_font = 6

        self.liste_nuages = [[60, 40, 96], [50, 15, 112], [15, 35, 112], [-10, 20, 96]]
        self.dir = 1
        self.time = 0

        # Position initiale du personnage
        self.x_personnage = self.width // 2 - self.taille_img - self.taille_img // 2
        self.y_personnage = self.height // 2 + self.height // 4

        # Variables d'animation
        self.animation_image = 0
        self.animation_vitesse = 2
        self.animation_timer = 0
        self.animation_direction = None
        self.animation_repos = None


        
        # Variables pour les troncs
        self.tab_y_tronc = [112, 96, 80, 64, 48, 32, 16]
        self.x_origine_tronc = self.width // 2 - self.taille_img // 2
        self.y_origine_tronc = self.y_personnage - self.taille_img // 2 + self.taille_img // 4 + self.taille_img // 8
        # Liste des troncs de départ
        self.file_tronc = list()
        self.file_tronc.append({
            "x": self.x_origine_tronc,
            "y": self.y_origine_tronc,
            "img": self.img,
            "branche": False,
            "droit": False,
            "nb": 0
                                })
        self.file_tronc.append({
            "x": self.x_origine_tronc,
            "y": self.y_origine_tronc - (len(self.file_tronc)) * self.taille_img,
            "img": self.img,
            "branche": False,
            "droit": False,
            "nb": 1
                                })

        # Démarrage du jeu
        p.play(0, 0, loop=True)
        p.run(self.update, self.draw)

    def ajoute_tronc(self):
        """Ajoute un nouveau tronc à la liste des troncs avec une probabilité d'ajouter une branche."""
        nb_tronc = len(self.file_tronc)    
        if self.nb_vies > 0:    
            proba = randint(1, 3)
            if proba != 3:
                self.file_tronc.append({
                    "x": self.x_origine_tronc,
                    "y": self.y_origine_tronc - nb_tronc * self.taille_img,
                    "img": self.img,
                    "branche": self.file_tronc[-1]["nb"] % 2 == 0,
                    "droit": bool(proba - 1),
                    "nb": nb_tronc
                                        })
            else:
                self.file_tronc.append({
                    "x": self.x_origine_tronc,
                    "y": self.y_origine_tronc - nb_tronc * self.taille_img,
                    "img": self.img,
                    "branche": False,
                    "droit": False,
                    "nb": nb_tronc
                                        })
        
        if self.nb_vies > 0 and self.file_tronc[0]["y"] > self.y_origine_tronc - self.taille_img:
            self.file_tronc[0]["branche"] = False

    def affiche_tronc(self):
        """Affiche tous les troncs dans la liste des troncs."""
        for tronc in self.file_tronc:
            y_position = self.tab_y_tronc[tronc["nb"] % len(self.tab_y_tronc)]
            p.blt(tronc["x"], tronc["y"], tronc["img"], 0, y_position, self.taille_img, self.taille_img, self.trans_font)

    def affiche_branches(self):
        """Affiche les branches des troncs en fonction de leur direction."""
        for tronc in self.file_tronc:
            if tronc["branche"]:
                if tronc["droit"]:
                    p.blt(tronc["x"] - self.taille_img * 2, tronc["y"], tronc["img"], 16, 16, self.taille_img * 2, self.taille_img * 2, self.trans_font)
                else:
                    p.blt(tronc["x"] + self.taille_img, tronc["y"], tronc["img"], 16, 64, self.taille_img * 2, self.taille_img * 2, self.trans_font)

    def retirer_tronc(self):
        self.file_tronc.pop(0)
        for tronc in self.file_tronc:
            tronc["y"] += self.taille_img

    def collisions(self):    
        if self.file_tronc[1]["branche"]:
            if (not self.file_tronc[1]["droit"] and not self.animation_direction == "Gauche") or (self.file_tronc[1]["droit"] and not self.animation_direction == "Droite"):
                self.nb_vies -= 1
                if self.animation_repos == "Gauche":
                    for _ in range(15):
                        p.blt(self.x_personnage, self.y_personnage, self.img, 48, 112, self.taille_img, self.taille_img, 6)
                        p.flip()
                elif self.animation_repos == "Droite":
                    for _ in range(15):
                        p.blt(self.x_personnage + self.taille_img * 2, self.y_personnage, self.img, 48, 112, self.taille_img, self.taille_img, 6)
                        p.flip()
            else:
                self.score += 1
        else:
            self.score += 1
        if self.nb_vies == 0:
            self.mort()

    def mort(self):
        """Affiche l'écran de fin de jeu avec les animations et les messages."""
        while True:
            p.cls(self.trans_font)
            p.rect(0, self.height - self.taille_img * 3, self.width, self.taille_img * 3, 11)

            p.rect(0, self.height - self.taille_img * 3 - 48, self.width, self.taille_img * 3, 7)

            for k in range(self.width // 16 + 1):
                p.blt(k * 16, self.height - self.taille_img * 3 - 52, 0, 0, 144, 16, 8)

            for k in range(6):
                p.blt(k * 20 - 5, 100, 0, 38, 128, 25, 32, 6)

            for nuage in self.liste_nuages:
                p.blt(nuage[0], nuage[1], 0, 16, nuage[2], 32, 16, 6)

            p.blt(10, 150, 0, 0, 160, 8, 12, 0)
            p.blt(30, 160, 0, 8, 160, 3, 12, 0)
            p.blt(70, 165, 0, 11, 160, 8, 12, 0)
            p.blt(80, 140, 0, 19, 160, 8, 12, 0)

            p.text(self.x_personnage + self.taille_img // 2, self.height // 2 - self.height // 4 - 10, "GAME OVER", 0)
            p.text(self.x_personnage + self.taille_img // 2, self.height // 2 - self.height // 4 - 10 + self.taille_img, "Score: " + str(self.score), 0)
            p.text(self.x_personnage - self.taille_img // 4, self.height // 2 - self.height // 4 - 10 + self.taille_img * 2, "Press ESC to exit", 0)

            # Affiche le paradis
            p.blt(self.x_origine_tronc - self.taille_img // 2, self.y_origine_tronc + self.taille_img, self.img, 16, 48, self.taille_img * 2, self.taille_img)
            p.blt(self.x_origine_tronc, self.y_origine_tronc, self.img, 0, 128, self.taille_img, self.taille_img, self.trans_font)
            if self.animation_repos == "Gauche":
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 112, self.taille_img, self.taille_img, 6)
            elif self.animation_repos == "Droite":
                p.blt(self.x_personnage + self.taille_img * 2, self.y_personnage, self.img, 48, 112, self.taille_img, self.taille_img, 6)

            self.file_tronc = list()
            p.show()

    def coupe_tronc(self):
        """Gère l'animation du personnage lorsqu'il coupe un tronc."""
        if self.animation_direction is None:
            if p.btn(p.KEY_LEFT):
                self.animation_direction = "Gauche"
                self.animation_image = 0
                self.animation_timer = 0
                self.retirer_tronc()
                self.collisions()
            elif p.btn(p.KEY_RIGHT):
                self.animation_direction = "Droite"
                self.animation_image = 0
                self.animation_timer = 0
                self.retirer_tronc()
                self.collisions()

        if self.animation_direction is not None:
            self.animation_personnage(self.animation_direction)
        else:
            # Affiche le personnage dans la dernière image de l'animation
            if self.animation_repos == "Gauche":
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 16, self.taille_img, self.taille_img, 6)
            elif self.animation_repos == "Droite":
                p.blt(self.x_personnage + self.taille_img * 2, self.y_personnage, self.img, 48, 32, self.taille_img, self.taille_img, 6)

    def animation_personnage(self, direction):
        """Gère les différentes étapes de l'animation du personnage."""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_vitesse:
            self.animation_image += 1
            self.animation_timer = 0

        if direction == "Gauche":
            if self.animation_image == 0:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 48, self.taille_img, self.taille_img, self.trans_font)
            elif self.animation_image == 1:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 80, self.taille_img, self.taille_img, 6)
            elif self.animation_image == 2:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 16, self.taille_img, self.taille_img, 6)
                self.animation_direction = None
                self.animation_image = 0
            self.animation_repos = "Gauche"
        elif direction == "Droite":
            if self.animation_image == 0:
                p.blt(self.x_personnage + self.taille_img * 2, self.y_personnage, self.img, 48, 64, self.taille_img, self.taille_img, 6)
            elif self.animation_image == 1:
                p.blt(self.x_personnage + self.taille_img * 2, self.y_personnage, self.img, 48, 96, self.taille_img, self.taille_img, 6)
            elif self.animation_image == 2:
                p.blt(self.x_personnage + self.taille_img * 2, self.y_personnage, self.img, 48, 32, self.taille_img, self.taille_img, 6)
                self.animation_direction = None
                self.animation_image = 0
            self.animation_repos = "Droite"

    def update(self):
        """Met à jour l'état du jeu (à implémenter)."""
        self.ajoute_tronc()

        self.time += 1

        if self.liste_nuages[0][1] < 30 or self.liste_nuages[0][1] > 60:
            self.dir = - self.dir


        if self.time % 5 == 0:
            for nuage in self.liste_nuages:
                nuage[0] -= 2
                nuage[1] += self.dir
                if nuage[0] < - 25:
                    nuage[0] = 95
        
        if p.btnp(p.KEY_LEFT) or p.btnp(p.KEY_RIGHT):
            son= MediaPlayer(str(randint(1,4))+".mp3")
            son.play()

            


    def draw(self):
        """Dessine tous les éléments du jeu à chaque frame."""
        p.cls(self.trans_font)
        p.rect(0, self.height - self.taille_img * 3 - 48, self.width, self.taille_img * 3, 7)

        for k in range(self.width // 16 + 1):
            p.blt(k * 16, self.height - self.taille_img * 3 - 52, 0, 0, 144, 16, 8)

        p.rect(0, self.height - self.taille_img * 3, self.width, self.taille_img * 3, 11)
        p.blt(self.x_origine_tronc - self.taille_img // 2, self.y_origine_tronc + self.taille_img, self.img, 16, 48, self.taille_img * 2, self.taille_img)
        
        for nuage in self.liste_nuages:
            p.blt(nuage[0], nuage[1], 0, 16, nuage[2], 32, 16, 6)

        for k in range(6):
            p.blt(k * 20 - 5, 100, 0, 38, 128, 25, 32, 6)

        p.blt(10, 150, 0, 0, 160, 8, 12, 0)
        p.blt(30, 160, 0, 8, 160, 3, 12, 0)
        p.blt(70, 165, 0, 11, 160, 8, 12, 0)
        p.blt(80, 140, 0, 19, 160, 8, 12, 0)

        self.affiche_tronc()
        self.affiche_branches()
        self.coupe_tronc()

        # Affichage du score et des vies
        p.blt(0, 1, self.img, 16, 0, self.taille_img * 2 , self.taille_img, self.trans_font)
        p.text(self.width // 9 - self.taille_img // 4, self.taille_img // 2 - self.taille_img // 8, str(self.score), 0)
        for vie in range(self.nb_vies):
            p.blt(self.width - self.taille_img - vie * 14, 1, self.img, 0, 0, self.taille_img, self.taille_img, self.trans_font)


# Démarrage du jeu
Main()