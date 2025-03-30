import random
from minimax import minimax
from alphabeta import alphabeta

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

    def choose_move(self, state):
        _, best_move, visited_nodes = self.calculate_best_move(state)
        print(f"Visited {len(visited_nodes)} nodes")
        return best_move if best_move else random.choice([2, 3, 4])  # Ja nav gājiena, izvēlas nejaušu
