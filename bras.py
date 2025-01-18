import pyxel as p
from random import randint

class Main:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        width = 128
        height = 224
        p.init(width, height, title='LumberJackGame', quit_key=p.KEY_ESCAPE, fps=30)
        p.load("res.pyxres")

        # Initialisation des variables de jeu
        self.score = 0
        self.nb_vies = 3

        # Position initiale du personnage
        self.x_personnage = 20
        self.y_personnage = 176

        # Variables d'animation
        self.animation_image = 0
        self.animation_vitesse = 5
        self.animation_timer = 0
        self.animation_direction = None
        self.animation_repos = None

        #Aurtres variables
        self.img = 0
        self.taille_img = 16
        self.trans_font = 6
        
        # Variables pour les troncs
        self.tab_y_tronc = [112, 96, 80, 64, 48, 32, 16]
        self.x_origine_tronc = 48
        self.y_origine_tronc = 192

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
            "y": self.y_origine_tronc + (len(self.file_tronc) + 1) * self.taille_img,
            "img": self.img,
            "branche": False,
            "droit": False,
            "nb": 1
        })

        # Démarrage du jeu
        p.run(self.update, self.draw)

    def ajoute_tronc(self):
        """Ajoute un nouveau tronc à la liste des troncs avec une probabilité d'ajouter une branche."""
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
        """Affiche tous les troncs dans la liste des troncs."""
        for tronc in self.file_tronc:
            y_position = self.tab_y_tronc[tronc["nb"] % len(self.tab_y_tronc)]
            p.blt(tronc["x"], tronc["y"], tronc["img"], 0, y_position, self.taille_img, self.taille_img, self.trans_font)

    def affiche_branches(self):
        """Affiche les branches des troncs en fonction de leur direction."""
        for tronc in self.file_tronc:
            if tronc["branche"]:
                if tronc["droit"]:
                    p.blt(tronc["x"], tronc["y"], tronc["img"], 16, 16, self.taille_img * 2, self.taille_img * 2, self.trans_font)
                else:
                    p.blt(tronc["x"], tronc["y"], tronc["img"], 16, 64, self.taille_img * 2, self.taille_img * 2, self.trans_font)

    def coupe_tronc(self):
        """Gère l'animation du personnage lorsqu'il coupe un tronc."""
        if self.animation_direction is None:
            if p.btnp(p.KEY_LEFT):
                self.animation_direction = "Gauche"
                self.animation_image = 0
                self.animation_timer = 0
            elif p.btnp(p.KEY_RIGHT):
                self.animation_direction = "Droite"
                self.animation_image = 0
                self.animation_timer = 0

        if self.animation_direction is not None:
            self.animation_personnage(self.animation_direction)
        else:
            # Affiche le personnage dans la dernière image de l'animation
            if self.animation_repos == "Gauche":
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 32, self.taille_img, self.taille_img)
            elif self.animation_repos == "Droite":
                p.blt(self.x_personnage, self.y_personnage - 32, self.img, 48, 16, self.taille_img, self)

    def animation_personnage(self, direction):
        """Gère les différentes étapes de l'animation du personnage."""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_vitesse:
            self.animation_image += 1
            self.animation_timer = 0

        if direction == "Gauche":
            if self.animation_image == 0:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 64, self.taille_img, self.taille_img)
            elif self.animation_image == 1:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 96, self.taille_img, self.taille_img)
            elif self.animation_image == 2:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 32, self.taille_img, self.taille_img)
                self.animation_direction = None
                self.animation_image = 0
            self.animation_repos = "Gauche"
        elif direction == "Droite":
            if self.animation_image == 0:
                p.blt(self.x_personnage, self.y_personnage - 32, self.img, 48, 48, self.taille_img, self.taille_img)
            elif self.animation_image == 1:
                p.blt(self.x_personnage, self.y_personnage - 32, self.img, 48, 80, self.taille_img, self.taille_img)
            elif self.animation_image == 2:
                p.blt(self.x_personnage, self.y_personnage - 32, self.img, 48, 16, self.taille_img, self.taille_img)
                self.animation_direction = None
                self.animation_image = 0
            self.animation_repos = "Droite"

    def update(self):
        """Met à jour l'état du jeu (à implémenter)."""
        self.ajoute_tronc()

    def draw(self):
        """Dessine tous les éléments du jeu à chaque frame."""
        p.cls(self.trans_font)
        p.rect(0, 192, 128, 40, 11)
        
        self.coupe_tronc()
        self.affiche_tronc()
        self.affiche_branches()
        
        # Affichage du score et des vies
        p.blt(0, 0, self.img, 16, 0, self.taille_img * 2, self.taille_img, 6)
        p.text(10, 6, str(self.score), 0)
        for k in range(self.nb_vies):
            p.blt(110 - k * 14, 2, self.img, 0, 0, self.taille_img, self.taille_img, 6)

# Démarrage du jeu
Main()