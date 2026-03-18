"""
Simple Tkinter GUI for the War card game.

The UI shows each round's draws, indicates when a war occurs, and reports the
final winner.  It steps through the game automatically with a short pause so
that the user can follow the action.
"""

from __future__ import annotations

import threading
import time
import tkinter as tk
from tkinter import scrolledtext

from .game import WarGame


def _run_game(game: WarGame, log_widget: scrolledtext.ScrolledText, delay: float = 0.5) -> None:
    """Execute the game, appending round information to *log_widget*.

    This runs in a background thread so the GUI stays responsive.
    """
    while True:
        info = game.play_one_round(verbose=False)
        # Build a readable line
        draws_str = ", ".join(f"{player}: {card}" for player, card in info["draws"])
        line = f"Round {info['round']}: {draws_str}"
        if info["war"]:
            line += "  **War!**"
        line += f"  → {info['winner']} wins the round"
        # Insert into the text widget in a thread‑safe way
        log_widget.after(0, lambda l=line: log_widget.insert(tk.END, l + "\n"))
        log_widget.after(0, log_widget.see, tk.END)
        if info["game_over"]:
            log_widget.after(0, lambda w=info["winner"]: log_widget.insert(tk.END, f"\n***** {w} wins the game! *****\n"))
            break
        time.sleep(delay)


def run_gui() -> None:
    """Launch the Tkinter window and start the War game simulation."""
    root = tk.Tk()
    root.title("War Card Game")

    # Text area for log output
    log = scrolledtext.ScrolledText(root, width=80, height=25, state="normal")
    log.pack(padx=10, pady=10)

    # Start button – disabled while a game is running
    start_btn = tk.Button(root, text="Start Game", width=20)
    start_btn.pack(pady=(0, 10))

    def on_start() -> None:
        start_btn.config(state="disabled")
        log.delete("1.0", tk.END)
        game = WarGame(("Alice", "Bob"))
        thread = threading.Thread(target=_run_game, args=(game, log), daemon=True)
        thread.start()

    start_btn.config(command=on_start)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
