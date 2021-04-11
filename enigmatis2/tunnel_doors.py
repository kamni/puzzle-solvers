#!/usr/bin/env python3

# REQUIRES PYTHON >= 3.8

"""
This is a partial solution for the doors with the tiles, located near where
the bodies in barrels were found. This door leads to the tunnels below the
manor house.

The game is a rotational tile game. Tiles are grouped into sets of 4 around a
central button. When the button is pressed, the tiles in the group of 4 shift
counter-clockwise. Each button shares two of its tiles with the buttons below
it and above it, respectively (e.g., in an array of 6 tiles, button 1 controls
the top 2 and the middle 2; button 2 controls the middle 2 and bottom 2).

The standard board looks as follows, where each number represents a
symbol that has been etched on the board:

    c1                c6
          button 1
    c2                c7
          button 2
    c3                c8
          button 3
    c4                c9
          button 4
    c5                c10

For example, button 1 controls spaces 1, 2, 7, and 6 (listed counter-clockwise
starting with the top left). When combined with the tiles sitting in the slots
to the outside, the board looks something like:

    t8:c1              t7:c6
            button 1
    t2:c2              t3:c7
            button 2
    t10:c3             t4:c8
            button 3
    t5:c4              t9:c9
            button 4
    t6:c5              t1:c10

When button 1 is pushed, the board will look like this:

    t7:c1              t3:c6
            button 1
    t8:c2              t2:c7
            button 2
    t10:c3             t4:c8
            button 3
    t5:c4              t9:c9
            button 4
    t6:c5              t1:c10

If we then pushed button 2, the board will look like:

    t7:c1              t3:c6
            button 1
    t2:c2              t4:c7
            button 2
    t8:c3              t10:c8
            button 3
    t5:c4              t9:c9
            button 4
    t6:c5              t1:c10

The purpose of the game is to rotate the tiles until the symbols on the tiles
(represented by numbers here) match the control symbols next to their
respective slots:

    t1:c1              t6:c6
            button 1
    t2:c2              t7:c7
            button 2
    t3:c3              t8:c8
            button 3
    t4:c4              t9:c9
            button 4
    t5:c5              t10:c10

There are 10 tiles in the original game, with 4 buttons to rotate the groups
of tiles.
"""

from typing import Dict, List, TypedDict


class ControlsConfig(TypedDict):
    button: int
    controls: list[int]


BoardConfig = List[ControlsConfig]
TilePosition = Dict[int, int]


STANDARD_CONFIG: BoardConfig = [
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
    def __init__(self, starting_tile_position: TilePosition,
                 config: BoardConfig=STANDARD_CONFIG):
        """
        NOTE: this init does not check for correct starting positions and
        configurations. You should be using some configuration from Enigmatis
        2:

            1. An even number of tile positions, more than 4, but less than 10
            2. The tile positions should match the numbers in the config
               controls

        :param dict starting_tile_position: describes the starting position of
            the tiles relative to the control positions where they belong. For
            example, if you have a circle tile in control position 1, and a
            triangle tile in control position 2, but their positions should be
            reversed, your dictionary should look like:

                {
                    1: 2,
                    2: 1,
                }

        :param list config: describes the layout of the puzzle, showing which
            buttons map rotate which control positions. The STANDARD_CONFIG
            assumes numbering the control positions down the left side first
            (1-5), then down the right side (6-10). The buttons that control
            the positions are numbered top-to-bottom; the controls groups are
            listed in counter-clockwise order, starting from the top left.
        """
        self.config = config
        self.current_layout = starting_tile_position

        self.steps = []
        self.step_queue = [starting_tile_position]
        self.seen_layouts = [self._format_seen_layout(starting_tile_position)]

    def __str__(self):
        tostring = ''

        if self._is_solved():
            if not self.steps:
                return 'Puzzle already solved! No changes needed.'

            tostring += 'The steps to solve the puzzle:\n'
        else:
            tostring += 'The puzzle is not yet solved.\n'

        for step_num, step in enumerate(self.steps):
            tostring += '\t{}. Press button {}'.format(
                self._format_integer(step_num),
                step,
            )

        if not self._is_solved():
            tostring += '\nCurrent layout:\n'
            tostring += str(self.current_layout)

        return tostring

    def run(self):
        # TODO: type hints
        print(self)

    def _calculate_tile_score(self, tile_position: TilePosition) -> int:
        groups = []

        # We're going to assume a correct tile position and config; failures
        # are the responsibility of the programmer
        #while (slice_start := 0) < len(tile_position):
        return 0

    def _format_integer(self, num: int) -> str:
        """
        Pad out integers less than 10 with a leading 0
        """
        return str(num).zfill(2)

    def _format_seen_layout(self, tile_position: TilePosition) -> int:
        """
        Converts a dictionary into an integer for self.seen_layouts.

        This is to minimize comparison times when checking "Have we seen this
        layout before?"
        """
        pos_list = list(tile_position.items())
        pos_list.sort()
        return int( '1' + ''.join([
            self._format_integer(num)
            for tup in pos_list
                for num in tup
        ]))

    def _is_solved(self) -> bool:
        for key in self.current_layout:
            if key != self.current_layout[key]:
                return False
        return True


if __name__ == '__main__':
    # Don't run this unless the appropriate version of python is being used
    import sys
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
        print("You must have at least python version 3.8 to run this.")
        sys.exit(1)

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
