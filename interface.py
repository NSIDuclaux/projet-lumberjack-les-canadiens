
import pyxel as p


class Main:

    def __init__(self):
        p.init(99, 176, title='interface', quit_key=p.KEY_ESCAPE, fps=30)

        self.interface = True
        self.login_signup = False
        self.ranking = False

        self.x_log = 5
        self.y_log = 80
        self.log_len = 93

        self.x_rank = 28
        self.y_rank = 100
        self.rank_len = 53
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

            p.rect(self.x_log, self.y_log, self.log_len, 12, 7)
            p.rectb(self.x_log, self.y_log, self.log_len, 12, 0)
            p.text(self.x_log + 3, self.y_log + 4, " Login / Sign-up -> L", 0)

            p.rect(self.x_rank, self.y_rank, self.rank_len, 12, 7)
            p.rectb(self.x_rank, self.y_rank, self.rank_len, 12, 0)
            p.text(30, 104, "Ranking -> R", 0)
        
        elif self.login_signup:
            p.mouse(True)

            p.cls(6)

            p.rectb(16, 30, 70, 12, 0)
            p.text(20, 34, "LumberJack Game", 0)

            p.rect(2, 2, 16, 16, 7)
            p.rectb(2, 2, 16, 16, 0)
            
        elif self.ranking:
            p.mouse(True)

            p.cls(6)

            p.rectb(16, 30, 70, 12, 0)
            p.text(20, 34, "LumberJack Game", 0)

            p.rect(2, 2, 16, 16, 7)
            p.rectb(2, 2, 16, 16, 0)


Main()