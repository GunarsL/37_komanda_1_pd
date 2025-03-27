import tkinter as tk
from tkinter import messagebox, Toplevel
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ai import AI
from minimax import simulate_move
from alphabeta import simulate_move

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiplication Game")
        
        # Algoritma izvēles sākotnējā iestatīšana (var izvēlēties starp Minimax un Alfa-beta)
        self.algorithm_choice = tk.StringVar(value="minimax")
        
        self.algorithm_label = tk.Label(root, text="Choose Algorithm (Minimax or AlphaBeta):")
        self.algorithm_label.pack()
        
        self.minimax_button = tk.Radiobutton(root, text="Minimax", variable=self.algorithm_choice, value="minimax")
        self.minimax_button.pack()
        
        self.alphabeta_button = tk.Radiobutton(root, text="AlphaBeta", variable=self.algorithm_choice, value="alphabeta")
        self.alphabeta_button.pack()

        self.number = tk.IntVar(value=8)
        self.player_score = 0
        self.computer_score = 0
        self.bank = 0
        # TODO: izvēlēties, kurš uzsāk spēli: cilvēks vai dators
        self.current_turn = "player"
        
        self.starting_player = tk.StringVar(value="player")

        self.starting_label = tk.Label(root, text="Who starts the game?")
        self.starting_label.pack()

        self.player_first_button = tk.Radiobutton(root, text="Player", variable=self.starting_player, value="player")
        self.player_first_button.pack()

        self.computer_first_button = tk.Radiobutton(root, text="Computer", variable=self.starting_player, value="computer")
        self.computer_first_button.pack()

        
        self.label = tk.Label(root, text="Choose a starting number (8-18):")
        self.label.pack()
        
        self.entry = tk.Entry(root, textvariable=self.number)
        self.entry.pack()
        
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()
        
        self.info_label = tk.Label(root, text="")
        self.info_label.pack()
        
        button_frame = tk.Frame(root)
        button_frame.pack()
        self.move_buttons = []
        for mult in [2, 3, 4]:
            button = tk.Button(button_frame, text=f"Multiply by {mult}", command=lambda m=mult: self.player_move(m))
            self.move_buttons.append(button)
            button.pack(side="left", padx=3, pady=2)
        
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack()
        
        self.tree_window = None
        self.ai = AI(self.algorithm_choice.get())
        self.update_ui()

    def start_game(self):
        try:
            num = int(self.entry.get())
            if num < 8 or num > 18:
                raise ValueError
            self.number.set(num)
            self.current_turn = self.starting_player.get()
            if self.current_turn == "computer":
                self.root.after(1000, self.computer_move)
            self.update_ui()
            self.open_tree_window()
        except ValueError:
            messagebox.showerror("Error", "Enter a number between 8 and 18")
    
    def player_move(self, multiplier):
        if self.current_turn == "player":
            self.make_move(multiplier, "player")
            self.current_turn = "computer"
            self.root.after(1000, self.computer_move)
    
    def computer_move(self):
        if self.current_turn == "computer":
            # TODO: jāfiksē datora vidējo laiku gājiena izpildei
            # Dators izvēlas gājienu atbilstoši algoritmam
            best_move = self.ai.choose_move({
                "number": self.number.get(),
                "player_score": self.computer_score,
                "bank": self.bank
            })
            self.make_move(best_move, "computer")
            self.current_turn = "player"
            self.update_ui()
    
    def make_move(self, multiplier, player):
        new_number = self.number.get() * multiplier
        if new_number >= 1200:
            if player == "player":
                self.player_score += self.bank
            else:
                self.computer_score += self.bank
            self.end_game()
            return
        
        if new_number % 2 == 0:
            if player == "player":
                self.player_score -= 1
            else:
                self.computer_score -= 1
        else:
            if player == "player":
                self.player_score += 1
            else:
                self.computer_score += 1
        
        if new_number % 10 == 0 or new_number % 10 == 5:
            self.bank += 1
        
        self.number.set(new_number)
        self.update_ui()
        self.update_tree()
    
    def update_ui(self):
        self.info_label.config(text=f"Number: {self.number.get()} | Player: {self.player_score} | Computer: {self.computer_score} | Bank: {self.bank}")
    
    def open_tree_window(self):
        self.tree_window = Toplevel(self.root)
        self.tree_window.title("Game Tree Visualization")
        self.update_tree()
    
    def update_tree(self):
        if not self.tree_window:
            return

        G = nx.DiGraph()
        levels = {}

        def build_tree(number, depth, level):
            if depth == 0 or number >= 1200:
                return

            node_id = (number, level)
            if node_id not in levels:
                G.add_node(node_id, subset=level)
                levels[node_id] = level

            children = [(number * 2, level + 1), (number * 3, level + 1), (number * 4, level + 1)]

            for child, child_level in children:
                if child < 1200:
                    child_id = (child, child_level)
                    G.add_node(child_id, subset=child_level)
                    levels[child_id] = child_level
                    G.add_edge(node_id, child_id)
                    build_tree(child, depth - 1, child_level)

        root_number = self.number.get()
        levels[(root_number, 0)] = 0
        build_tree(root_number, 3, 1)
        
        nodes_to_remove = [node for node in G.nodes if node[1] == 0]
        G.remove_nodes_from(nodes_to_remove)

    
        for node in G.nodes():
            if "subset" not in G.nodes[node]:
                G.nodes[node]["subset"] = levels[node]

        
        pos = nx.multipartite_layout(G, subset_key="subset")

        fig, ax = plt.subplots(figsize=(8, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, ax=ax)

        for widget in self.tree_window.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.tree_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def end_game(self):
        # TODO: jāfiksē datora un cilvēka uzvaru skaitu
        if self.player_score > self.computer_score:
            winner = "Player wins!"
        elif self.computer_score > self.player_score:
            winner = "Computer wins!"
        else:
            winner = "It's a draw!"
        messagebox.showinfo("Game Over", winner)
    
    def restart_game(self):
        self.number.set(8)
        self.player_score = 0
        self.computer_score = 0
        self.bank = 0
        self.current_turn = "player"
        self.update_ui()
        self.update_tree()