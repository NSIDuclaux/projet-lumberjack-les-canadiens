import pyxel as p
from random import randint
from nava import play
import string
from tkinter import *
import sqlite3

class Nuage:

    def __init__(self, x, y, y_max, y_min, n_type, dire):
        self.x = x
        self.y = y
        self.y_min = y_min
        self.y_max = y_max
        self.type = n_type
        self.dir = dire
        self.time = 0

    def avancer(self):
        self.time += 1
        if self.time % 5 == 0:
            if self.x < - 25:
                self.x = 95
            else:
                self.x -= 2

            if (self.dir < 0 and self.y < self.y_min) or (self.dir > 0 and self.y > self.y_max):
                self.dir = - self.dir
            self.y += self.dir


class Main:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.width = 99
        self.height = 176
        p.init(self.width, self.height, title='LumberJackGame', quit_key=p.KEY_ESCAPE, fps=30)
        p.load("res.pyxres", False, False, False, False)

        # Initialisation des variables de jeu

        self.res = []
        self.curseur = 1
        self.pseudo = ""
        self.password = ""
        self.dictionnaire = {f"KEY_{lettre}": lettre for lettre in string.ascii_uppercase}

        self.interface = True
        self.login_signup = False
        self.ranking = False

        self.x_log = 3
        self.y_log = 80
        self.log_len = 93

        self.x_rank = 22
        self.y_rank = 100
        self.rank_len = 53

        self.see_password = False
        self.num_ranking = 0

        self.score = 0
        self.nb_vies = 3
        self.start_perso_point_d_interogation = True

        self.img = 0
        self.taille_img = 16
        self.trans_font = 6

        self.liste_nuages = list()
        for k in range(4):
            self.nouveau_nuage()
            
        self.dir = 1
        self.time = 0
        self.start_page = False
        self.state_sound = False

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
        if self.state_sound:
            p.play(0, 0, loop=True)
        p.run(self.update, self.draw)


    def trie_classement(self, liste):
        res_liste = list()
        while liste != []:
            maxi = liste[0]
            for ele in liste:
                if ele[1] > maxi[1]:
                    maxi = ele
            res_liste.append(maxi)
            liste.remove(maxi)

        return res_liste


    def pseudo_valide(self, pseudo, password):
        connexion = sqlite3.connect('ranking.db')
        c = connexion.cursor()

        data = (pseudo, )
        c.execute('''SELECT Pseudo, Password FROM LumberJackGame WHERE Pseudo = ?''', data)
        res = c.fetchall()

        connexion.commit()
        connexion.close()

        if len(res) == 0:
            return [True, True]
        
        return [res[0][1] == password, False]


    def nouveau_nuage(self):
        x = randint(-1, 8) * 10
        y = randint(1, 5) * 10
        y_max = randint(4, 6) * 10
        y_min = randint(1, 3) * 10

        n_type = 112
        dire = 1
        if randint(0, 1):
            n_type = 96
            dire = - dire

        self.liste_nuages.append(Nuage(x, y, y_max, y_min, n_type, dire))


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
                if self.state_sound:
                    play("Ouille.wav",async_mode=True)
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
        if self.pseudo != "":

            connexion = sqlite3.connect('ranking.db')
            c = connexion.cursor()
            data = (self.pseudo, )
            c.execute('''SELECT Score FROM "LumberJackGame" WHERE Pseudo = ?''', data)
            res = c.fetchall() 

            if res[0][0] <= self.score:
                data = (self.score, self.pseudo, )
                c.execute('''UPDATE "LumberJackGame" set Score = ? WHERE Pseudo = ?''', data)
            connexion.commit()
            connexion.close()

        while True:
            p.cls(12)
            p.rect(0, self.height - self.taille_img * 3, self.width, self.taille_img * 3, 11)

            p.rect(0, self.height - self.taille_img * 3 - 48, self.width, self.taille_img * 3, 6)
            p.blt(- 4,self.height - self.taille_img * 3 - 45, 0, 0, 184, 105, 45, 6)

            for k in range(self.width // 16 + 1):
                p.blt(k * 16, self.height - self.taille_img * 3 - 52, 0, 0, 144, 16, 8, 5, 180)

            for k in range(6):
                p.blt(k * 20 - 5, 100, 0, 38, 128, 25, 32, 6)

            for nuage in self.liste_nuages:
                p.blt(nuage.x, nuage.y, 0, 16, nuage.type, 32, 16, 6)

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

            if self.state_sound:
                p.blt(80, 160, 0, 0, 240, 16, 16, 6)
            else:
                p.blt(80, 160, 0, 16, 240, 16, 16, 6)

            self.file_tronc = list()
            p.show()

        update_score()

    def coupe_tronc(self):
        """Gère l'animation du personnage lorsqu'il coupe un tronc."""
        if self.animation_direction is None:
            if p.btnp(p.KEY_LEFT):
                self.animation_direction = "Gauche"
                self.animation_image = 0
                self.animation_timer = 0
                self.retirer_tronc()
                self.collisions()
                self.start_perso_point_d_interogation = False

            elif p.btnp(p.KEY_RIGHT):
                self.animation_direction = "Droite"
                self.animation_image = 0
                self.animation_timer = 0
                self.retirer_tronc()
                self.collisions()
                self.start_perso_point_d_interogation = False

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

        for nuage in self.liste_nuages:
            nuage.avancer()

        if p.btn(p.MOUSE_BUTTON_LEFT):
            self.start_page = False

        if self.state_sound:
            if p.btnp(p.KEY_LEFT) or p.btnp(p.KEY_RIGHT):
                play((str(randint(1,4))+".wav"),async_mode=True)

        if p.btnp(p.KEY_M) and not self.ranking and not self.login_signup and not self.interface:
            if self.state_sound:
                self.posi_sound = p.play_pos(1)
                p.stop(self.posi_sound)
            else:
                p.play(0, 0, loop=True)
            self.state_sound = not self.state_sound

        if self.interface:
            if p.btnp(p.KEY_J):
                self.interface = False
                self.login_signup = False
                self.ranking = False
                self.start_page = True

        if self.interface or self.login_signup or self.ranking:
            
            if p.btnp(p.KEY_L) and self.interface:
                self.pseudo = ""
                self.interface = False
                self.login_signup = True

            elif p.btn(p.KEY_R) and self.interface:
                self.interface = False
                self.ranking = True

            if self.login_signup and p.btnp(p.KEY_DELETE):
                self.login_signup = False
                self.interface = True
                self.password = ""
                self.pseudo = ""

            elif self.ranking and p.btnp(p.KEY_DELETE):
                self.ranking = False
                self.interface = True
                self.num_ranking = 0

            if self.login_signup and not p.btnp(p.KEY_DELETE):

                if p.btnp(p.KEY_KP_MULTIPLY):
                    self.see_password = not self.see_password

                for (key, val) in self.dictionnaire.items():
                    if p.btnp(eval("p." + key)):
                        if len(self.pseudo) < 16 and self.curseur == 1:
                            self.pseudo += val
                        elif len(self.password) < 16 and self.curseur == 2:
                            self.password += val

                if len(self.pseudo) < 16 and self.curseur == 1 and p.btnp(p.KEY_SPACE):
                    self.pseudo += "_"
                elif len(self.password) < 16 and self.curseur == 2 and p.btnp(p.KEY_SPACE):
                    self.password += "_"

                if len(self.pseudo) < 16 and self.curseur == 1 and p.btnp(p.KEY_BACKSPACE):
                    self.pseudo = self.pseudo[:-1]
                elif len(self.password) < 16 and self.curseur == 2 and p.btnp(p.KEY_BACKSPACE):
                    self.password = self.password[:-1]

                if p.btnp(p.KEY_KP_1):
                    self.curseur = 1
                elif p.btnp(p.KEY_KP_2):
                    self.curseur = 2

                res = self.pseudo_valide(self.pseudo, self.password)

                if p.btnp(p.KEY_RETURN) and self.password != "" and self.pseudo != "" and res[0]:
                    if res[1]:
                        connexion = sqlite3.connect('ranking.db')

                        c = connexion.cursor()  
                        data = (self.pseudo, self.password, 0, )
                        c.execute('''INSERT INTO LumberJackGame VALUES (?, ?, ?)''', data)

                        connexion.commit()
                        connexion.close()

                    self.interface = False
                    self.login_signup = False
                    self.ranking = False
                    self.start_page = True



    def draw(self):
        """Dessine tous les éléments du jeu à chaque frame."""
        p.cls(12)

        if self.interface:
            p.mouse(True)

            p.cls(6)

            p.rectb(16, 30, 70, 12, 0)
            p.text(20, 34, "LumberJack Game", 0)

            p.rect(self.x_log, self.y_log, self.log_len, 12, 7)
            p.rectb(self.x_log, self.y_log, self.log_len, 12, 0)
            p.text(self.x_log + 2, self.y_log + 4, " Login / Sign-up -> L", 0)

            p.rect(self.x_rank, self.y_rank, self.rank_len, 12, 7)
            p.rectb(self.x_rank, self.y_rank, self.rank_len, 12, 0)
            p.text(25, 104, "Ranking -> R", 0)

            p.rect(15, 150, 70, 12, 8)
            p.rectb(15, 150, 70, 12, 0)
            p.text(33, 154, "PLAY -> J", 0)

        
        elif self.login_signup:
            p.mouse(True)

            p.cls(6)

            p.rectb(16, 30, 70, 12, 0)
            p.text(20, 34, "LumberJack Game", 0)

            p.rect(2, 2, 16, 16, 7)
            p.rectb(2, 2, 16, 16, 0)
            p.blt(2, 2, 0, 64, 16, 16, 16, 6)
            p.text(16, 9, " -> Suppr", 0)

            p.text(15, 60, "Current cursor : " + str(self.curseur), 7)

            p.text(28, 80, "Pseudo -> 1", 0)
            p.rect(15, 90, 70, 12, 7)
            p.rectb(15, 90, 70, 12, 0)
            p.text(17, 94, self.pseudo, 0)

            p.text(24, 110, "Password -> 2", 0)
            p.rect(15, 120, 70, 12, 7)
            p.rectb(15, 120, 70, 12, 0)
            p.blt(40, 133, 0, 64, 0, 8, 8, 6)
            p.text(50, 135, "*", 7)
            

            password = "*" * len(self.password)
            if self.see_password:
                password = self.password

            p.text(17, 124, password, 0)

            p.rect(15, 150, 70, 12, 8)
            p.rectb(15, 150, 70, 12, 0)
            p.text(28, 154, "Press ENTER", 0)
        

        elif self.ranking:
            self.num_ranking += 1
            p.mouse(True)

            p.cls(6)

            p.rectb(16, 30, 70, 12, 0)
            p.text(20, 34, "LumberJack Game", 0)

            p.rect(2, 2, 16, 16, 7)
            p.rectb(2, 2, 16, 16, 0)
            p.blt(2, 2, 0, 64, 16, 16, 16, 6)
            p.text(16, 9, " -> Suppr", 0)

            if self.num_ranking == 1:
                connexion = sqlite3.connect('ranking.db')
                c = connexion.cursor()

                c.execute('''SELECT Pseudo, Score FROM LumberJackGame''')
                self.res = c.fetchall()
                self.res = self.trie_classement(self.res)
                connexion.commit()
                connexion.close()

            for k in range(len(self.res)):
                if k > 2 and k < 6:
                    p.text(10, 66 + 16 * k, str(k) + ". " + self.res[k][0] + " / " + str(self.res[k][1]), 0)  
                else:
                    p.blt(5, 60 + 16 * k, 0, 80 + 16 * k, 0, 16, 16, 6)
                    p.text(22, 66 + 16 * k, self.res[k][0] + " / " + str(self.res[k][1]), 0)  


        elif self.start_page:
            p.mouse(True)
            p.rect(0, self.height - self.taille_img * 3 - 48, self.width, self.taille_img * 3, 6)

            for k in range(self.width // 16 + 1):
                p.blt(k * 16, self.height - self.taille_img * 3 - 52, 0, 0, 144, 16, 8, 5, 180)

            p.rect(0, self.height - self.taille_img * 3, self.width, self.taille_img * 3, 11)
            p.blt(self.x_origine_tronc - self.taille_img // 2, self.y_origine_tronc + self.taille_img, self.img, 16, 48, self.taille_img * 2, self.taille_img)
            p.blt(self.x_origine_tronc - self.taille_img // 2 + 8, self.y_origine_tronc + self.taille_img - 16, 0, 32, 160, 16, 16, 6)

            for nuage in self.liste_nuages:
                p.blt(nuage.x, nuage.y, 0, 16, nuage.type, 32, 16, 6)

            p.blt(- 4,self.height - self.taille_img * 3 - 45, 0, 0, 184, 105, 45, 6)

            for k in range(6):
                p.blt(k * 20 - 5, 100, 0, 38, 128, 25, 32, 6)

            p.blt(10, 150, 0, 0, 160, 8, 12, 0)
            p.blt(30, 160, 0, 8, 160, 3, 12, 0)
            p.blt(70, 165, 0, 11, 160, 8, 12, 0)
            p.blt(80, 140, 0, 19, 160, 8, 12, 0)

            c = 8
            t = self.time % 90

            if t <= 30:
                c = 5
            elif t >= 60:
                c = 3


            p.text(self.x_personnage + self.taille_img // 2 - 13, self.height // 2 - 40, "LUMBERJACK GAME", 0)
            p.rectb(self.x_personnage + self.taille_img // 2 - 17, self.height // 2 - 46, 67, 17, 0)
            p.text(self.x_personnage + self.taille_img // 2 - 10, self.height // 2 - 20, "CLICK TO START", c)

            if self.state_sound:
                p.blt(80, 160, 0, 0, 240, 16, 16, 6)
            else:
                p.blt(80, 160, 0, 16, 240, 16, 16, 6)

        else:
            p.mouse(False)
            p.rect(0, self.height - self.taille_img * 3 - 48, self.width, self.taille_img * 3, 6)

            for k in range(self.width // 16 + 1):
                p.blt(k * 16, self.height - self.taille_img * 3 - 52, 0, 0, 144, 16, 8, 5, 180)

            p.rect(0, self.height - self.taille_img * 3, self.width, self.taille_img * 3, 11)
            p.blt(self.x_origine_tronc - self.taille_img // 2, self.y_origine_tronc + self.taille_img, self.img, 16, 48, self.taille_img * 2, self.taille_img)
        
            for nuage in self.liste_nuages:
                p.blt(nuage.x, nuage.y, 0, 16, nuage.type, 32, 16, 6)

            p.blt(- 4,self.height - self.taille_img * 3 - 45, 0, 0, 184, 105, 45, 6)

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

            if self.start_perso_point_d_interogation:
                p.blt(self.x_personnage, self.y_personnage, self.img, 48, 48, self.taille_img, self.taille_img, self.trans_font)

            if self.state_sound:
                p.blt(80, 160, 0, 0, 240, 16, 16, 6)
            else:
                p.blt(80, 160, 0, 16, 240, 16, 16, 6)

# Démarrage du jeu
Main()