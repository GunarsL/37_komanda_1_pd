import random
from minimax import minimax

class AI:
    def choose_move(self, state):
        # TODO: izvēlēties, kuru algoritmu izmantos dators: Minimaksa algoritmu vai Alfa-beta algoritmu
        # TODO: jāfiksē datora apmeklēto virsotņu skaitu
        _, best_move = minimax(state, 3, True)
        return best_move if best_move else random.choice([2, 3, 4])