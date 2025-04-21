# Mākslīgā intelekta loģika spēles vajadzībām.
# Šī klase atbild par gājienu izvēli, izmantojot vienu no diviem algoritmiem:
# - Minimax (meklē vislabāko rezultātu, pārbaudot visus variantus)
# - Alpha-Beta (uzlabota Minimax versija ar griešanas optimizāciju)
# ------------------------------------------------------------
import random
from minimax import minimax
from alphabeta import alphabeta
# ------------------------------------------------------------
# Mākslīgā intelekta klase (AI).
# Konstruktorā tiek iestatīts, kuru algoritmu izmantot, un
# metode `choose_move()` izvēlas labāko gājienu dotajā situācijā.
# ------------------------------------------------------------
class AI:
    def __init__(self, algorithm="minimax"):
        self.algorithm = algorithm  # Algoritms, kuru izmantos dators ("minimax" vai "alphabeta")

        # Izvēlas algoritmu atkarībā no iestatījuma
        if self.algorithm == "minimax":
            self.calculate_best_move = lambda state: minimax(state, 3, True)
        elif self.algorithm == "alphabeta":
            self.calculate_best_move = lambda state: alphabeta(state, 3, float('-inf'), float('inf'), True)
        else:
            raise ValueError("Incorrect algorithm argument")
 # --------------------------------------------------------
    # Atkarībā no izvēlētā algoritma izsauc Minimax vai Alpha-Beta.
    # Ja neizdodas atrast gājienu, izvēlas nejaušu no pieejamajiem (2, 3, 4).
    # --------------------------------------------------------
    def choose_move(self, state):
        _, best_move = self.calculate_best_move(state)
        return best_move if best_move else random.choice([2, 3, 4])  # Ja nav gājiena, izvēlas nejaušu
