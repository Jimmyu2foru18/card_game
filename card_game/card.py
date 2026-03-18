"""
A playing card consisting of a suit and a rank.

The class is deliberately lightweight – it only stores the data and provides a
human‑readable ``__str__`` representation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, List


@dataclass(frozen=True, slots=True)
class Card:
    """Immutable representation of a standard playing card.

    Attributes
    ----------
    rank: str
        One of ``"2"`` … ``"10"``, ``"J"``, ``"Q"``, ``"K"`` or ``"A"``.
    suit: str
        One of ``"♠"``, ``"♥"``, ``"♦"`` or ``"♣"``.
    """

    rank: str
    suit: str

    #: Ordered list of valid ranks – used for comparison operations.
    _RANK_ORDER: ClassVar[List[str]] = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "J",
        "Q",
        "K",
        "A",
    ]

    #: Ordered list of suits – primarily for a stable sort.
    _SUIT_ORDER: ClassVar[List[str]] = ["♣", "♦", "♥", "♠"]

    def __post_init__(self) -> None:
        if self.rank not in self._RANK_ORDER:
            raise ValueError(f"Invalid rank: {self.rank!r}")
        if self.suit not in self._SUIT_ORDER:
            raise ValueError(f"Invalid suit: {self.suit!r}")

    # ---------------------------------------------------------------------
    # Comparison helpers – they are useful for games that need to rank cards.
    # ---------------------------------------------------------------------
    def rank_value(self) -> int:
        """Return an integer representing the card's rank.

        The ``_RANK_ORDER`` list defines the ordering from lowest to highest.
        """
        return self._RANK_ORDER.index(self.rank)

    def suit_value(self) -> int:
        """Return an integer representing the suit's order.

        This is not needed for most games, but it gives a deterministic order
        when two cards have the same rank.
        """
        return self._SUIT_ORDER.index(self.suit)

    # ---------------------------------------------------------------------
    # Human‑readable representation
    # ---------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"Card(rank={self.rank!r}, suit={self.suit!r})"

    # ---------------------------------------------------------------------
    # Equality / ordering based on rank then suit.
    # ---------------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: "Card") -> bool:
        if self.rank_value() == other.rank_value():
            return self.suit_value() < other.suit_value()
        return self.rank_value() < other.rank_value()
