"""
A very small ``Player`` abstraction.

The class stores the player's name and the cards that the player has won
(e.g. in the *War* card game).  The ``play_card`` method simply draws the top
card from a supplied ``Deck`` instance.
"""

from __future__ import annotations

from typing import List

from .card import Card
from .deck import Deck


class Player:
    """Represents a single participant in a card‑game session.

    Parameters
    ----------
    name:
        Human‑readable identifier used in logs and the UI.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.won_cards: List[Card] = []

    # ------------------------------------------------------------------
    # Gameplay helpers
    # ------------------------------------------------------------------
    def play_card(self, deck: Deck) -> Card:
        """Draw a card from *deck* and return it.
        """
        card = deck.draw()
        return card

    def collect_cards(self, cards: List[Card]) -> None:
        """Add the won *cards* to the player's personal pile.
        """
        self.won_cards.extend(cards)

    def __repr__(self) -> str:
        return f"Player({self.name!r}, {len(self.won_cards)} won cards)"
