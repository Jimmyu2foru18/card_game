import pytest
from card_game.card import Card
from card_game.deck import Deck
from card_game.player import Player
from card_game.game import WarGame


def test_card_equality_and_ordering():
    c1 = Card("A", "♠")
    c2 = Card("K", "♥")
    c3 = Card("A", "♣")
    assert c1 != c2
    assert c1 > c2
    assert c3 < c1  # same rank, suit order decides


def test_deck_draw_and_shuffle():
    deck = Deck()
    original = deck._cards.copy()
    deck.shuffle()
    # After shuffle we should still have 52 unique cards
    assert len(deck) == 52
    assert set(deck._cards) == set(original)
    # Drawing reduces the deck size by one
    top = deck.draw()
    assert isinstance(top, Card)
    assert len(deck) == 51


def test_player_collects_cards():
    p = Player("Test")
    cards = [Card("2", "♣"), Card("3", "♦")]
    p.collect_cards(cards)
    assert len(p.won_cards) == 2


def test_war_game_completes():
    # Run a quick silent game – it should finish without raising.
    game = WarGame(("Alice", "Bob"))
    champion = game.play(verbose=False)
    # One player must have collected all 52 cards
    assert len(champion.won_cards) == 52
    # The other player should have zero won cards
    other = [p for p in game.players if p is not champion][0]
    assert len(other.won_cards) == 0
