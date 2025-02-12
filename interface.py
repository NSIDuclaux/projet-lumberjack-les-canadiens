
import pyxel as p


class Main:

    def __init__(self):
        p.init(99, 176, title='interface', quit_key=p.KEY_ESCAPE, fps=30)

        self.interface = True
        self.login_signup = False
        self.ranking = False

        p.run(self.update, self.draw)



    def update(self):
        if p.btn(p.KEY_L) and self.interface:
            self.interface = False
            self.login_signup = True
        elif p.btn(p.KEY_R) and self.interface:
            self.interface = False
            self.ranking = True


    def draw(self):
        if self.interface:
            p.mouse(True)

            p.cls(6)

            p.rectb(16, 30, 70, 12, 0)
            p.text(20, 34, "LumberJack Game", 0)

            p.rect(5, 80, 83, 12, 7)
            p.rectb(5, 80, 83, 12, 0)
            p.text(8, 84, " Login / Sign-up -> L", 0)

            p.rect(28, 100, 43, 12, 7)
            p.rectb(28, 100, 43, 12, 0)
            p.text(30, 104, "Ranking -> R", 0)
        
        elif self.login_signup:
            p.mouse(True)

            p.cls(6)

            p.rect(15, 80, 73, 12, 7)
            p.rectb(15, 80, 73, 12, 0)
            p.text(18, 84, " Login / Sign-up -> L", 0)

            p.rect(33, 100, 35, 12, 7)
            p.rectb(33, 100, 35, 12, 0)
            p.text(36, 104, "Ranking -> R", 0)

        elif self.ranking:
            p.mouse(True)

            p.cls(0)

            p.rect(15, 80, 73, 12, 7)
            p.rectb(15, 80, 73, 12, 0)
            p.text(18, 84, " Login / Sign-up -> L", 0)

            p.rect(33, 100, 35, 12, 7)
            p.rectb(33, 100, 35, 12, 0)
            p.text(36, 104, "Ranking -> R", 0)

Main()