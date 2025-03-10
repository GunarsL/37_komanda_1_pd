import random
from minimax import minimax

class AI:
    def choose_move(self, state):
        _, best_move = minimax(state, 3, True)
        return best_move if best_move else random.choice([2, 3, 4])