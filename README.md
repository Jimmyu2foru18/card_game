# Card Game Framework

This repository contains a tiny, well‑documented Python framework for building
card‑game applications.  It ships with a complete, playable implementation
of the classic *War* game, which can be used as a reference implementation
or a starting point for more elaborate games.

## Features

- Immutable :class:`~card_game.card.Card` objects with rank/suit ordering.
- Fully shuffled :class:`~card_game.deck.Deck` with a simple ``draw`` API.
- Minimal :class:`~card_game.player.Player` abstraction.
- A runnable ``WarGame`` that demonstrates how the core classes interact.
- Type‑annotated, PEP‑8 compliant source code.
- A small test suite covering the most important behaviours.

## Getting Started

```bash
# Clone the repo
git clone 
cd card_game

# Install the runtime dependencies
pip install -r requirements.txt

# Run the example War game
python -m card_game.game   # defaults to Alice vs Bob
python -m card_game.game Alice Charlie -q  # quiet mode
```

## Extending the Framework

To create a new game, copy the ``WarGame`` class and replace the ``play``
method with your own rules engine.  Re‑use :class:`Card`, :class:`Deck` and
:class:`Player` – they already provide the low‑level mechanics you’ll need.

## Testing

```bash
pytest
```

The test suite lives in the ``tests`` directory and checks basic deck
behaviour, card ordering, and that a full game finishes without errors.
