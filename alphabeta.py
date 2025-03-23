
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

def simulate_move(state, multiplier):
    new_number = state["number"] * multiplier
    new_player_score = state["player_score"]
    new_bank = state["bank"]
    
    if new_number % 2 == 0:
        new_player_score -= 1
    else:
        new_player_score += 1
    
    if new_number % 10 == 0 or new_number % 10 == 5:
        new_bank += 1
    
    return {"number": new_number, "player_score": new_player_score, "bank": new_bank}
