from helper import simulate_move

def alphabeta(state, depth, alpha, beta, maximizing):
    if state["number"] >= 1200 or depth == 0:
        return state["player_score"], None

    best_move = None
    if maximizing:
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