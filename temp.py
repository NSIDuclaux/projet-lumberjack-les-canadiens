self.x_personnage = 1
self.y_personnage = 1
def coupe_tronc(self):
    if pyxel.btn(pyxel.KEY_LEFT):
        pyxel.blt(self.x_personnage, self.y_personnage, 0, 48, 64, 16, 16, 6)
        wait(0.2)
        pyxel.blt(self.x_personnage, self.y_personnage, 0, 48, 96, 16, 16, 6)
        wait(0.05)
        pyxel.blt(self.x_personnage, self.y_personnage, 0, 48, 32, 16, 16, 6)
    if pyxel.btn(pyxel.KEY_RIGHT):
        pyxel.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 48, 16, 16, 6)
        wait(0.2)
        pyxel.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 80, 16, 16, 6)
        wait(0.05)
        pyxel.blt(self.x_personnage, self.y_personnage - 32, 0, 48, 16, 16, 16, 6)
