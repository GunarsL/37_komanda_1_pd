import tkinter as tk
from tkinter import messagebox, Toplevel
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ai import AI
from helper import TemplateHelper

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiplication Game")
        self.tree_window = None

        self.number = tk.IntVar()
        
        self.algorithm_choice = TemplateHelper.algorithm_choice_radio_buttons(root) # Algoritma izvēles sākotnējā iestatīšana (var izvēlēties starp Minimax un Alfa-beta)
        self.starting_player = TemplateHelper.starting_player_radio_buttons(root) # Lietotāja izvēles sākotnējā iestatīšana
        self.entry, self.start_button = TemplateHelper.starting_number(root, self.number, self.start_game) # Input ar numuru un buttoniem
        
        self.info_label = tk.Label(root, text="")
        self.info_label.pack()
        
        self.enable_multiply_buttons, self.disable_multiply_buttons = TemplateHelper.multiply_buttons(root, self.player_move)
        
        self.reset_button = tk.Button(root, text="Play again", command=self.reset_game)
        self.reset_button.pack_forget()
        
        self.reset_game()

    def start_game(self):
        self.ai = AI(self.algorithm_choice.get())
        try:
            num = int(self.entry.get())
            if num < 8 or num > 18:
                raise ValueError
            self.number.set(num)
            self.current_turn = self.starting_player.get()

            if self.current_turn == "computer":
                self.disable_multiply_buttons()
                self.root.after(1000, self.computer_move)
            else:
                self.enable_multiply_buttons()

            self.start_button["state"] = "disabled"
            self.entry["state"] ="disabled"
            self.update_info_label()
            self.open_tree_window()
        except ValueError:
            messagebox.showerror("Error", "Enter a number between 8 and 18")
    
    def player_move(self, multiplier):
        if self.current_turn == "player":
            self.make_move(multiplier, "player")
            self.current_turn = "computer"
            self.disable_multiply_buttons()
            self.root.after(1000, self.computer_move)
    
    def computer_move(self):
        if self.current_turn == "computer":
            # Dators izvēlas gājienu atbilstoši algoritmam
            best_move = self.ai.choose_move({
                "number": self.number.get(),
                "player_score": self.computer_score,
                "bank": self.bank
            })
            is_game_finished = self.make_move(best_move, "computer")
            if (not is_game_finished):
                self.enable_multiply_buttons()
            self.current_turn = "player"
            self.update_info_label()
    
    def make_move(self, multiplier, player):
        new_number = self.number.get() * multiplier
        if new_number >= 1200:
            if player == "player":
                self.player_score += self.bank
            else:
                self.computer_score += self.bank
            self.end_game()
            return True
        
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
        self.update_info_label()
        self.update_tree()
    
    def update_info_label(self):
        self.info_label.config(text=f"Number: {self.number.get()} | Player: {self.player_score} | Computer: {self.computer_score} | Bank: {self.bank}")
    
    def open_tree_window(self):
        if self.tree_window is not None: return
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
        labels = {node: node[0] for node in G.nodes()}

        fig, ax = plt.subplots(figsize=(8, 8))
        nx.draw(G, pos, labels=labels, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, ax=ax)

        for widget in self.tree_window.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.tree_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def end_game(self):
        if self.player_score > self.computer_score:
            winner = "Player wins!"
        elif self.computer_score > self.player_score:
            winner = "Computer wins!"
        else:
            winner = "It's a draw!"
        messagebox.showinfo("Game Over", winner)
        self.entry["state"] = "normal"
        self.reset_button.pack()
    
    def reset_game(self):
        self.start_button["state"] = "normal"

        self.number.set(8)
        self.player_score = 0
        self.computer_score = 0
        self.bank = 0
        self.current_turn = "player"

        self.update_info_label()

        self.reset_button.forget()
        self.disable_multiply_buttons()

        if self.tree_window is not None:
            self.tree_window.destroy()
            self.tree_window.update()
            self.tree_window = None
         