import tkinter as tk

class TemplateHelper:
    @staticmethod
    def algorithm_choice_radio_buttons(root):
        algorithm_frame = tk.Frame(root)
        algorithm_choice = tk.StringVar(value="minimax")
        
        algorithm_label = tk.Label(root, text="Choose Algorithm (Minimax or AlphaBeta):")
        algorithm_label.pack()
        
        minimax_button = tk.Radiobutton(algorithm_frame, text="Minimax", variable=algorithm_choice, value="minimax")
        minimax_button.pack(side="left")
        
        
        alphabeta_button = tk.Radiobutton(algorithm_frame, text="AlphaBeta", variable=algorithm_choice, value="alphabeta")
        alphabeta_button.pack(side="left")

        algorithm_frame.pack()

        return algorithm_choice
    
    @staticmethod
    def starting_player_radio_buttons(root):
        starting_player_frame = tk.Frame(root)
        starting_player = tk.StringVar(value="player")

        starting_label = tk.Label(root, text="Who starts the game?")
        starting_label.pack()

        player_first_button = tk.Radiobutton(starting_player_frame, text="Player", variable=starting_player, value="player")
        player_first_button.pack(side="left")

        computer_first_button = tk.Radiobutton(starting_player_frame, text="Computer", variable=starting_player, value="computer")
        computer_first_button.pack(side="left")

        starting_player_frame.pack()

        return starting_player
    
    @staticmethod
    def starting_number(root, number, start_game_function):
        label = tk.Label(root, text="Choose a starting number (8-18):")
        label.pack()
        
        entry = tk.Entry(root, textvariable=number)
        entry.pack()
        
        start_button = tk.Button(root, text="Start Game", command=start_game_function)
        start_button.pack()

        return entry, start_button
    
    @staticmethod
    def multiply_buttons(root, player_move):
        button_frame = tk.Frame(root)
        button_frame.pack()
        multiply_buttons = []
        for mult in [2, 3, 4]:
            button = tk.Button(button_frame, text=f"Multiply by {mult}", command=lambda m=mult: player_move(m))
            multiply_buttons.append(button)
            button.pack(side="left", padx=3, pady=2)

        def set_button_state(button, state): button["state"] = state
        enable_multiply_buttons = lambda multiply_buttons=multiply_buttons: [set_button_state(multiply_button, "normal") for multiply_button in multiply_buttons]
        disable_multiply_buttons = lambda multiply_buttons=multiply_buttons: [set_button_state(multiply_button, "disabled") for multiply_button in multiply_buttons]

        return enable_multiply_buttons, disable_multiply_buttons




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