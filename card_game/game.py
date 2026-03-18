"""
A minimal command‑line implementation of the classic *War* card game.

Running ``python -m card_game.game`` will start a two‑player automatic
match that prints each round to ``stdout``.  The implementation is kept
intentionally small so that the repository can serve as a template for any
future card‑game project – developers can replace ``WarGame`` with their own
rules engine while re‑using the ``Card``, ``Deck`` and ``Player`` helpers.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

from .deck import Deck
from .player import Player
from .card import Card


class WarGame:
    """Core game‑loop for the *War* card game.

    The game runs automatically – each player draws one card per round,
    the higher rank wins and takes both cards.  In the event of a tie a
    *war* is declared – each player places three face‑down cards and then
    draws a fourth to resolve the tie.  The winner of the war collects all
    cards that were played.
    """

    def __init__(self, player_names: Tuple[str, str]):
        self.deck = Deck()
        self.players: List[Player] = [Player(name) for name in player_names]
        self.round = 0

    # ------------------------------------------------------------------
    # Helper methods used by ``play``
    # ------------------------------------------------------------------
    def _draw(self) -> List[Tuple[Player, Card]]:
        """Each player draws one card from the shared deck.
        If the deck is empty, recycle the players' won cards back into the deck.
        Returns a list of ``(player, card)`` pairs.
        """
        # Replenish deck if needed before drawing
        if len(self.deck) == 0:
            # Gather all won cards from players
            recycled: List[Card] = []
            for p in self.players:
                recycled.extend(p.won_cards)
                p.won_cards.clear()
            if not recycled:
                # No cards left anywhere – game cannot continue
                raise RuntimeError("No cards left to draw; game cannot continue")
            self.deck._cards = recycled
            self.deck.shuffle()
        draws = []
        for player in self.players:
            draws.append((player, player.play_card(self.deck)))
        return draws

    def _resolve_war(self, spoils: List[Card]) -> Player:
        """Handle a tie ("war").

        The function assumes both players still have enough cards – if a
        player cannot continue the war they lose the game immediately.
        Returns the player who wins the war.
        """
        # Each player puts three face‑down cards (if they have them) and a
        # fourth face‑up card to decide the winner.
        for _ in range(3):
            for player in self.players:
                if len(self.deck) == 0:
                    # Not enough cards to continue – the other player wins.
                    other = [p for p in self.players if p is not player][0]
                    other.collect_cards(spoils + self._draw_remaining())
                    return other
                spoils.append(player.play_card(self.deck))
        # Final decisive card
        final_draw = self._draw()
        for _, card in final_draw:
            spoils.append(card)
        # Determine winner of the war
        winner = max(final_draw, key=lambda pc: pc[1])
        winner[0].collect_cards(spoils)
        return winner[0]

    def _draw_remaining(self) -> List[Card]:
        """Drain the deck – used when a player cannot continue a war.
        """
        remaining = []
        while len(self.deck) > 0:
            remaining.append(self.deck.draw())
        return remaining

    # ------------------------------------------------------------------
    # New: play a single round and report details
    # ------------------------------------------------------------------
    def play_one_round(self, verbose: bool = False) -> dict:
        """Execute a single round of War.

        Returns a dictionary with round information, e.g.::

            {
                "round": 5,
                "draws": [("Alice", "A♠"), ("Bob", "K♥")],
                "war": False,
                "winner": "Alice",
                "game_over": False,
            }
        """
        self.round += 1
        round_spoils: List[Card] = []
        draws = self._draw()
        round_spoils.extend(card for _, card in draws)
        war = False
        winner_name: str | None = None
        if draws[0][1] == draws[1][1]:
            war = True
            if verbose:
                sys.stdout.write(f"Round {self.round}: **War!**\n")
            winner = self._resolve_war(round_spoils)
            winner_name = winner.name
        else:
            winner = max(draws, key=lambda pc: pc[1])[0]
            winner.collect_cards(round_spoils)
            winner_name = winner.name
        # Determine if the game has finished
        game_over = any(len(p.won_cards) == 52 for p in self.players)
        return {
            "round": self.round,
            "draws": [(p.name, str(c)) for p, c in draws],
            "war": war,
            "winner": winner_name,
            "game_over": game_over,
        }

    # ------------------------------------------------------------------
    # Public API – ``play`` runs the whole match using ``play_one_round``
    # ------------------------------------------------------------------
    def play(self, verbose: bool = True) -> Player:
        """Execute the game loop until one player possesses all 52 cards.

        Parameters
        ----------
        verbose:
            If ``True`` each round is printed; set to ``False`` for a silent
            simulation (useful for automated tests).
        """
        while not any(len(p.won_cards) == 52 for p in self.players):
            self.play_one_round(verbose=verbose)
        # Game over – the player with 52 won cards is the champion
        champion = max(self.players, key=lambda p: len(p.won_cards))
        if verbose:
            sys.stdout.write(f"\n{champion.name} wins after {self.round} rounds!\n")
        return champion


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play a quick game of War between two computer players.")
    parser.add_argument("player1", nargs="?", default="Alice", help="Name of the first player")
    parser.add_argument("player2", nargs="?", default="Bob", help="Name of the second player")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress round‑by‑round output")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    game = WarGame((args.player1, args.player2))
    game.play(verbose=not args.quiet)


if __name__ == "__main__":
    main()
