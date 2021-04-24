"""

## Setup:

Before you can run the script, you need to configure the ``max_turns``,
``initial``, ``config``, and ``goal`` variables at the top of this script.

### max_turns

The ``max_turns`` variable is the easiest -- it is the number of turns that you
have to solve the puzzle.

### initial and goal

In order to specify the ``initial`` and ``goal``, you need to assign each
pillar a number (you can choose either 0-start or 1-start numbering), and then
you need to specify the value (or desired value) that the pillar should have.
This should be done as a list of tuples, with the number in the first space and
the value in the second space.

### config

Then you need to specify the config. This is a nested list of tuples that
represents the distance to each pillar, from each pillar. For example, if the
pillar is 2 away from pillar 1, then use ``(1, 2)``.

* When representing the pillar to itself, use ``0`` as the distance.

* When representing a directional pillar, where the directional move is not
  possible, use a negative number (e.g., ``(1, -1) if it is not possible to
  move from the current pillar to pillar 1).

The ordering list should match the same order that you configure the ``initial``
and ``goal`` lists.


-----

## Example:

> There are 3 pillars, each with a value of 1 stone. You need to get to a point
> where the last pillar has all three stones, and you have 2 turns to do this.

Here's what the setup will look like:

```python
max_turns = 2

initial = (
    (1, 1),
    (2, 1),
    (3, 1),
)

goal = (
    (1, 0),
    (2, 0),
    (3, 3),
)

config = (
    ( (1, 0), (2, 1), (3, 2) ),
    ( (1, 1), (2, 0), (3, 1) ),
    ( (1, 2), (2, 1), (3, 0) ),
)
```

"""

# Set your solution constraints here.

###############################################################################
from typing import Dict, Tuple, TypedDict


# Iterable of tuples describing the layout of the current board. First number in
# the tuple is the column number; second number is the number of stones sitting
# on the column.
PositionList = Tuple[Tuple[int, int]]

# Iterable of tuples describing distance to each of the pillars relative to another
# pillar. First number of the tuple is the column number to move stones to;
# second number is the distance (number of hops) stones must be moved to reach
# that pillar. If the distance is 0, then the stones are either already at the
# pillar, or the pillar is unreachable.
PillarDistance = Tuple[Tuple[int, int]]

class PuzzleConfig(TypedDict):
    max_turns: int
    initial: PositionList
    goal: PositionList
    config: Tuple[PillarDistance]

# Dictionary of puzzle configurations. The key is the number of the puzzle
MultiplePuzzleConfig = Dict[int, PuzzleConfig]


PUZZLES: MultiplePuzzleConfig = {
    0: {  # test problem
        'max_turns': 2,
        'initial': (
            (1, 1),
            (2, 1),
            (3, 1),
        ),
        'goal': (
            (1, 0),
            (2, 0),
            (3, 3),
        ),
        'config': (
            ( (1, 0), (2, 1), (3, 2) ),
            ( (1, 1), (2, 0), (3, 1) ),
            ( (1, 2), (2, 1), (3, 0) ),
        ),
    },
    22: {
        'max_turns': 4,
        'initial': (
            (1, 8),
            (2, 5),
            (3, 7),
            (4, 9),
            (5, 7),
            (6, 12),
        ),
        'goal': (
            (1, 8),
            (2, 8),
            (3, 8),
            (4, 8),
            (5, 8),
            (6, 8),
        ),
        'config': (
            ( (1, 0), (2, 1), (3, 2), (4, 3), (5, 2), (6, 3) ),
            ( (1, 1), (2, 0), (3, 1), (4, 2), (5, 1), (6, 2) ),
            ( (1, 2), (2, 1), (3, 0), (4, 3), (5, 2), (6, 3) ),
            ( (1, 3), (2, 2), (3, 3), (4, 0), (5, 1), (6, 2) ),
            ( (1, 2), (2, 1), (3, 2), (4, 1), (5, 0), (6, 1) ),
            ( (1, 3), (2, 2), (3, 3), (4, 2), (5, 1), (6, 0) ),
        ),
    },
    29: {
        'max_turns': 5,
        'initial': (
            (1, 2),
            (2, 6),
            (3, 4),
            (4, 8),
            (5, 1),
        ),
        'goal': (
            (1, 3),
            (2, 6),
            (3, 3),
            (4, 3),
            (5, 6),
        ),
        'config': (
            ( (1, 0), (2, 1), (3, 2), (4, 3), (5, 4) ),
            ( (1, 1), (2, 0), (3, 1), (4, 2), (5, 3) ),
            ( (1, 2), (2, 1), (3, 0), (4, 1), (5, 2) ),
            ( (1, 3), (2, 2), (3, 1), (4, 0), (5, 1) ),
            ( (1, 4), (2, 3), (3, 2), (4, 1), (5, 0) ),
        ),
    },
    30: {
        'max_turns': 6,
        'initial': (
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 4),
            (5, 6),
            (6, 0),
            (7, 0),
            (8, 0),
        ),
        'goal': (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 1),
            (5, 0),
            (6, 1),
            (7, 1),
            (8, 1),
        ),
        'config': (
            ( (1,0), (2,1), (3,2), (4,3), (5,1), (6,2), (7,3), (8,4) ),
            ( (1,1), (2,0), (3,1), (4,2), (5,2), (6,1), (7,2), (8,3) ),
            ( (1,2), (2,1), (3,0), (4,1), (5,3), (6,2), (7,3), (8,2) ),
            ( (1,3), (2,2), (3,1), (4,0), (5,4), (6,3), (7,2), (8,1) ),
            ( (1,1), (2,2), (3,3), (4,4), (5,0), (6,1), (7,2), (8,3) ),
            ( (1,2), (2,1), (3,2), (4,3), (5,1), (6,0), (7,1), (8,2) ),
            ( (1,3), (2,2), (3,3), (4,2), (5,2), (6,1), (7,0), (8,1) ),
            ( (1,4), (2,3), (3,3), (4,1), (5,3), (6,2), (7,1), (8,0) ),
        )
    },
    31: {
        'max_turns': 6,
        'initial': (
            (1, 7),
            (2, 8),
            (3, 4),
            (4, 7),
            (5, 9),
            (6, 0),
        ),
        'goal': (
            (1, 6),
            (2, 6),
            (3, 6),
            (4, 6),
            (5, 5),
            (6, 6),
        ),
        'config': (
            ( (1,0), (2,1), (3,2), (4,1), (5,2), (6,3) ),
            ( (1,1), (2,0), (3,1), (4,2), (5,1), (6,2) ),
            ( (1,2), (2,1), (3,0), (4,3), (5,2), (6,1) ),
            ( (1,1), (2,2), (3,3), (4,0), (5,3), (6,4) ),
            ( (1,2), (2,1), (3,2), (4,3), (5,0), (6,3) ),
            ( (1,3), (2,2), (3,1), (4,4), (5,3), (6,0) ),
        ),
    },
    44: {
        'max_turns': 5,
        'initial': (
            (1, 4),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 5),
        ),
        'goal': (
            (1, 0),
            (2, 1),
            (3, 0),
            (4, 3),
            (5, 0),
            (6, 0),
            (7, 5),
            (8, 0),
            (9, 0),
        ),
        'config': (
            ((1, 0), (2, 1), (3, 2), (4, 3), (5, 3), (6, 4), (7, 5), (8, 5), (9, 0)),
            ((1, 0), (2, 0), (3, 1), (4, 2), (5, 2), (6, 3), (7, 4), (8, 4), (9, 0)),
            ((1, 0), (2, 1), (3, 0), (4, 1), (5, 1), (6, 2), (7, 3), (8, 3), (9, 0)),
            ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)),
            ((1, 0), (2, 2), (3, 1), (4, 2), (5, 0), (6, 1), (7, 2), (8, 2), (9, 0)),
            ((1, 0), (2, 3), (3, 2), (4, 3), (5, 1), (6, 0), (7, 1), (8, 1), (9, 0)),
            ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)),
            ((1, 0), (2, 4), (3, 3), (4, 3), (5, 2), (6, 1), (7, 2), (8, 0), (9, 0)),
            ((1, 0), (2, 5), (3, 4), (4, 5), (5, 3), (6, 2), (7, 3), (8, 1), (9, 0)),
        ),
    },
    47: {
        'max_turns': 6,
        'initial': (
            (1, 3),
            (2, 3),
            (3, 2),
            (4, 2),
            (5, 3),
            (6, 3),
            (7, 2),
            (8, 0),
            (9, 2),
        ),
        'goal': (
            (1, 10),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 10),
            (7, 0),
            (8, 0),
            (9, 0),
        ),
        'config': (
            ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)), #1
            ((1, 1), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 3), (8, 2), (9, 1)), #2
            ((1, 2), (2, 1), (3, 0), (4, 1), (5, 2), (6, 3), (7, 3), (8, 3), (9, 2)), #3
            ((1, 3), (2, 2), (3, 1), (4, 0), (5, 1), (6, 2), (7, 2), (8, 3), (9, 3)), #4
            ((1, 5), (2, 4), (3, 5), (4, 6), (5, 0), (6, 1), (7, 1), (8, 2), (9, 3)), #5
            ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)), #6
            ((1, 4), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0), (8, 1), (9, 2)), #7
            ((1, 3), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 1), (8, 0), (9, 1)), #8
            ((1, 2), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 2), (8, 1), (9, 0)), #9
        ),
    },
}
