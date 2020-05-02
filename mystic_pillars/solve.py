# -*- coding: utf-8 -*-

"""
Solver for the Mystic Pillars video game.

## How to use the script:

  1. Set up a goal, an initial_config, and max_turns.
  2. Save, and run the script.
  3. The output shows you how many stones to shift to which pillars.


-----

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

Then you need to specify the config. This is a list of dictionaries that
represents the distance to each pillar, from each pillar. When representing the
pillar to itself, use ``0`` as the distance. This list should match the same
order that you configure the ``initial`` and ``goal`` lists.


-----

## Example:

> There are 3 pillars, each with a value of 1 stone. You need to get to a point
> where the last pillar has all three stones, and you have 2 turns to do this.

Here's what the setup will look like:

```python
max_turns = 2

initial = [
    (1, 1),
    (2, 1),
    (3, 1),
]

goal = [
    (1, 0),
    (2, 0),
    (3, 3),
]

config = [
    { 1:0, 2:1, 3:2 },
    { 1:1, 2:0, 3:1 },
    { 1:2, 2:1, 3:0 },
]
```

"""

# Set your solution constraints here.

max_turns = 5

initial = [
    (1, 2),
    (2, 6),
    (3, 4),
    (4, 8),
    (5, 1),
]

goal = [
    (1, 3),
    (2, 6),
    (3, 3),
    (4, 3),
    (5, 6),
]

config = [
    { 1:0, 2:1, 3:2, 4:3, 5:4 },
    { 1:1, 2:0, 3:1, 4:2, 5:3 },
    { 1:2, 2:1, 3:0, 4:1, 5:2 },
    { 1:3, 2:2, 3:1, 4:0, 5:1 },
    { 1:4, 2:3, 3:2, 4:1, 5:2 },
]

#################### DON'T EDIT BELOW THIS LINE ###############################


def solve(intial, config, goal, max_turns):
    QUEUE = []
    ALREADY_SEEN = []

    while QUEUE:
        tmp_solution = QUEUE.pop()

    return None


def pretty_print(solution):
    divider = '--------'

    print(divider)

    if not solution:
        print('No solution to the constraints provided')
    else:
        print(solution)

    print(divider)


###############################################################################

if __name__ == '__main__':
    solution = solve(initial, config, goal, max_turns)
    pretty_print(solution)
