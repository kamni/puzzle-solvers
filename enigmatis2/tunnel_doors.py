#!/usr/bin/env python3

"""
This is a partial solution for the doors with the tiles, located near where
the bodies in barrels were found. This door leads to the tunnels below the
manor house.

The game is a rotational tile game. Tiles are grouped into sets of 4 around a
central button. When the button is pressed, the tiles in the group of 4 shift
counter-clockwise. Each button shares two of its tiles with the buttons below
it and above it, respectively (e.g., in an array of 6 tiles, button 1 controls
the top 2 and the middle 2; button 2 controls the middle 2 and bottom 2).

The purpose of the game is to rotate the tiles until the symbols on the tiles
match the symbols next to their respective slots.

There are 10 tiles in the original game, with 4 buttons to rotate the groups
of tiles.
"""

STANDARD_CONFIG = [
    {
        "button": 1,
        "controls": [1, 2, 7, 6],
    },
    {
        "button": 2,
        "controls": [2, 3, 8, 7],
    },
    {
        "button": 3,
        "controls": [3, 4, 9, 8],
    },
    {
        "button": 4,
        "controls": [4, 5, 10, 9],
    },
]


class Solver:
    def __init__(self, starting_tile_position, config=STANDARD_CONFIG):
        self.config = config
        self.current_layout = starting_tile_position

        self.steps = []

    def __str__(self):
        tostring = ''

        if self._is_solved():
            if not self.steps:
                return 'Puzzle already solved! No changes needed.'

            tostring += 'The steps to solve the puzzle:\n'
        else:
            tostring += 'The puzzle is not yet solved.\n'

        for step_num, step in enumerate(self.steps):
            tostring += '\t{}. Press button {}', step_num, step

        if not self._is_solved():
            tostring += '\nCurrent layout:\n'
            tostring += str(self.current_layout)

        return tostring

    def run(self):
        print(self)

    def _is_solved(self):
        for key in self.current_layout:
            if key != self.current_layout[key]:
                return False
        return True


if __name__ == '__main__':
    # I've already manually solved the top 4 tiles; I'm going to do a smaller
    # config where I just solve the bottom 6 tiles
    custom_config = [
        {
            "button": 3,
            "controls": [3, 4, 9, 8],
        },
        {
            "button": 4,
            "controls": [4, 5, 10, 9],
        },
    ]
    starting_tiles = {
        3: 8,
        4: 4,
        5: 9,
        8: 10,
        9: 3,
        10: 5,
    }

    Solver(starting_tiles, custom_config).run()
