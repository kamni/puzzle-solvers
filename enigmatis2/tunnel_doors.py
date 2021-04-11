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

from typing import Dict, Final, List, Tuple, TypedDict


class ControlsConfig(TypedDict):
    button: int
    controls: list[int]


BoardConfig = List[ControlsConfig]
TilePosition = Dict[int, int]
TileShifts = Dict[int, List[Tuple[int, int]]]
StepList = List[int]
StepQueue = List[Tuple[StepList, TilePosition]]


# This is the initial setup in Enigmatis 2
DEFAULT_CONFIG: Final[BoardConfig] = [
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
                 config: BoardConfig=DEFAULT_CONFIG):
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
        self.config: Final[BoardConfig] = config
        self.allowed_tile_shifts: TileShifts = self._generate_tile_shifts()

        # This will be set as part of run(), and is displayed by str() upon
        # completion
        self.solution: List[int] = []

        # Internal use during run()
        self._current_layout: TilePosition = None
        self._step_queue: StepQueue = [([], starting_tile_position)]
        self._seen_layouts: List[int] = []

    def __str__(self) -> str:
        tostring = '\n----------\n\n'

        if not (self.solution and self._is_solved(self._current_layout)):
            tostring += 'The puzzle is not solved.\n\n'
            tostring += f'Current layout:\n\t{self._current_layout}'
        else:
            tostring += 'The steps to solve the puzzle:\n\n'
            for step_num, step in enumerate(self.solution):
                tostring += '\t{}. Press button {}\n'.format(
                    self._format_integer(step_num),
                    step,
                )

        tostring += '\n\n---------\n'
        return tostring

    def run(self):
        while (solved := False) and len(self.step_queue) >= 0:
            current_steps, current_tile_position = self.step_queue.pop()
            self._current_layout = current_tile_position

            next_steps = self._generate_next_steps(
                current_steps,
                current_tile_position,
            )
            for steps, tile_position in next_steps:
                if self._is_solved(tile_position):
                    self.solution = steps
                    solved = True
                    break

                if self._is_improvement(tile_position):
                    self.step_queue.insert(0, [steps, tile_position])
                else:
                    # We don't want to waste our time in the future, so let's
                    # stick it in seen_layouts, even though we haven't properly
                    # looked at it
                    self.seen_layouts.append(
                        self._format_seen_layout(tile_position),
                    )

            self.seen_layouts.append(
                self._format_seen_layout(current_tile_position),
            )

        print(self)

    def _calculate_new_position(self, tile_position: TilePosition,
                                button_group: ControlsConfig) -> TilePosition:
        """
        When a button is pressed, calculate the new positions for tiles
        """
        new_position = tile_position.copy()
        shifts = self.allowed_tile_shifts[button_group['button']]

        for old_tile, new_tile in shifts:
            new_position[old_tile] = tile_position[new_tile]

        return new_position

    def _calculate_tile_score(self, tile_position: TilePosition) -> int:
        groups = []

        # We're going to assume a correct tile position and config; failures
        # are the responsibility of the programmer
        for group in self.config:
            pass
        while (slice_start := 0) < len(tmp_tiles):
            slice_start = 10000
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

    def _generate_next_steps(self, step_list: StepList,
                             tile_position: TilePosition) -> StepQueue:
        new_queue = []

        for button_group in self.config:
            new_steps = step_list[:] + [button['button_group']]
            new_position = _calculate_new_position(tile_position, button_group)

            new_queue.append((new_steps, new_position))

        return new_queue

    def _generate_tile_shifts(self) -> TileShifts:
        """
        Used by init to generate the ways tiles can shift at button press
        """
        shifts_dict = {}

        for control_config in self.config:
            button = control_config['button']
            shifts = control_config['controls'][:]

            shifts.insert(0, shifts.pop())
            shifts_dict[button] = shifts

        return shifts_dict

    def _is_improvement(self, tile_position: TilePosition) -> bool:
        # TODO: have we seen this before?
        # TODO: is it a better score?
        return False

    def _is_solved(self, tile_position: TilePosition) -> bool:
        for control, tile in title_position.items():
            if control != tile:
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
