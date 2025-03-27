import random
from minimax import minimax
from alphabeta import alphabeta  # Importējiet Alfa-beta algoritmu

class AI:
    def __init__(self, algorithm="minimax"):
        self.algorithm = algorithm  # Algoritms, kuru izmantos dators ("minimax" vai "alphabeta")
    # TODO: jāfiksē datora apmeklēto virsotņu skaitu
    def choose_move(self, state):
        # Izvēlas algoritmu atkarībā no iestatījuma
        if self.algorithm == "minimax":
            _, best_move = minimax(state, 3, True)
        elif self.algorithm == "alphabeta":
            _, best_move = alphabeta(state, 3, float('-inf'), float('inf'), True)
        
        return best_move if best_move else random.choice([2, 3, 4])  # Ja nav gājiena, izvēlas nejaušu
