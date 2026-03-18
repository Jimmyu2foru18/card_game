"""
A standard 52‑card deck.

The ``Deck`` class creates the 52 unique :class:`~card_game.card.Card`
instances, provides a ``shuffle`` method and lets callers ``draw`` cards
from the top of the stack.
"""

from __future__ import annotations

import random
from typing import List

from .card import Card


class Deck:
    """A mutable collection representing a shuffled deck of cards.

    The deck is initialised in a deterministic order (clubs → diamonds →
    hearts → spades, low rank → high rank) and can be shuffled in‑place.
    ``draw`` removes the top card and returns it; attempting to draw from an
    empty deck raises ``IndexError``.
    """

    _RANKS = Card._RANK_ORDER
    _SUITS = Card._SUIT_ORDER

    def __init__(self) -> None:
        self._cards: List[Card] = [Card(rank, suit) for suit in self._SUITS for rank in self._RANKS]
        self.shuffle()

    # ------------------------------------------------------------------
    # Core deck operations
    # ------------------------------------------------------------------
    def shuffle(self) -> None:
        """Randomly reorder the remaining cards in‑place.
        """
        random.shuffle(self._cards)

    def draw(self) -> Card:
        """Remove and return the top card.

        Raises
        ------
        IndexError
            If the deck is empty.
        """
        if not self._cards:
            raise IndexError("Cannot draw from an empty deck")
        return self._cards.pop()

    # ------------------------------------------------------------------
    # Helpers for introspection / debugging
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._cards)

    def __repr__(self) -> str:
        return f"Deck({len(self)} cards left)"
