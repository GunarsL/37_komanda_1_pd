# Šeit tiek inicializēts tkinter grafiskais logs un palaista spēles klase.
import tkinter as tk
from game import Game

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()