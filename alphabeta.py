# Alpha-beta algoritms ar griešanu (optimizēta Minimax versija).
# Meklē labāko iespējamo gājienu dotajam spēles stāvoklim,
# izmantojot alpha-beta apgriešanu, lai optimizētu meklēšanu
# un izvairītos no liekiem aprēķiniem.
# ------------------------------------------------------------
from helper import simulate_move

def alphabeta(state, depth, alpha, beta, maximizing):
    # Ja spēles stāvoklis ir galīgs vai sasniegts maksimālais dziļums, atgriež rezultātu
    if state["number"] >= 1200 or depth == 0:
        return state["player_score"], None

    best_move = None
    if maximizing:
        # Maksimizējošā puse (dators) meklē augstāko iespējamo rezultātu
        max_eval = float('-inf')
        for move in [2, 3, 4]:
            new_state = simulate_move(state, move)
            eval_score, _ = alphabeta(new_state, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        # Minimizējošā puse (pretinieks) meklē zemāko iespējamo rezultātu
        min_eval = float('inf')
        for move in [2, 3, 4]:
            new_state = simulate_move(state, move)
            eval_score, _ = alphabeta(new_state, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move