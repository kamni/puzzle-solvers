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
DEFAULT_BOARD_CONFIG: Final[BoardConfig] = [
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
DEFAULT_TILE_POSITION: Final[TilePosition] = {
    1: 10,
    2: 2,
    3: 9,
    4: 5,
    5: 3,
    6: 1,
    7: 6,
    8: 7,
    9: 4,
    10: 8,
}


class Solver:
    def __init__(self, config: BoardConfig=DEFAULT_BOARD_CONFIG,
                 starting_tile_position: TilePosition=DEFAULT_TILE_POSITION):
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
                    1: 2,  # control position: tile position
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

        # This will be set as part of run(), and is displayed by str() upon
        # completion
        self.solution: List[int] = []

        # Internal use during run()
        self._allowed_tile_shifts: TileShifts = self._generate_tile_shifts()
        self._current_layout: TilePosition = None
        self._step_queue: StepQueue = [([], starting_tile_position)]
        self._seen_layouts: Set[int] = set()

    def __str__(self) -> str:
        tostring = '\n----------\n\n'

        if not self.solution:
            tostring += 'The puzzle is not solved.\n\n'
            tostring += f'Current layout:\n\t{self._current_layout}'
        else:
            tostring += 'The steps to solve the puzzle:\n\n'
            for step_num, step in enumerate(self.solution):
                tostring += '\t{}. Press button {}\n'.format(
                    self._format_integer(step_num + 1),
                    step,
                )

        tostring += '\n\n---------\n'
        return tostring

    def run(self):
        while not self.solution and len(self._step_queue) > 0:
            current_steps, current_tile_position = self._step_queue.pop()
            self._current_layout = current_tile_position

            next_steps = self._generate_next_steps(
                current_steps,
                current_tile_position,
            )
            for steps, tile_position in next_steps:
                if self._is_solved(tile_position):
                    self.solution = steps
                    self._current_layout = tile_position
                    break

                if self._is_improvement(tile_position):
                    self._step_queue.insert(0, [steps, tile_position])
                else:
                    # We don't want to waste our time in the future, so let's
                    # stick it in seen_layouts, even though we haven't properly
                    # looked at it
                    self._seen_layouts.add(
                        self._format_seen_layout(tile_position),
                    )

            self._seen_layouts.add(
                self._format_seen_layout(current_tile_position),
            )

        print(self)

    def _calculate_new_position(self, tile_position: TilePosition,
                                button_group: ControlsConfig) -> TilePosition:
        """
        When a button is pressed, calculate the new positions for tiles
        """
        new_position = tile_position.copy()
        shifts = self._allowed_tile_shifts[button_group['button']]

        for old_tile, new_tile in shifts:
            new_position[old_tile] = tile_position[new_tile]

        return new_position

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
            new_steps = step_list[:] + [button_group['button']]
            new_position = self._calculate_new_position(
                tile_position,
                button_group,
            )

            new_queue.append((new_steps, new_position))

        return new_queue

    def _generate_tile_shifts(self) -> TileShifts:
        """
        Used by init to generate the ways tiles can shift at button press
        """
        shifts_dict = {}

        for control_config in self.config:
            button = control_config['button']
            old_position = control_config['controls']

            new_position = old_position[:]
            new_position.insert(0, new_position.pop())
            shifts_dict[button] = list(zip(old_position, new_position))

        return shifts_dict

    def _is_improvement(self, tile_position: TilePosition) -> bool:
        if self._format_seen_layout(tile_position) in self._seen_layouts:
            return False

        # TODO: I was originally going to play around with a genetic algorithm
        # that calculated the distance to the tile's final location, and then
        # prune any options that were a significant decrease in score (i.e., it
        # gets farther from the desired final outcome; however, the Solver
        # already returns a result relatively quickly, and a genetic algorithm
        # is a bit of an overkill if this solver isn't taking a long time.
        # Perhaps I'll play with genetic algorithms later?
        return True

    def _is_solved(self, tile_position: TilePosition) -> bool:
        for control, tile in tile_position.items():
            if control != tile:
                return False
        return True


if __name__ == '__main__':
    # Don't run this unless the appropriate version of python is being used
    import sys
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
        print("You must have at least python version 3.8 to run this.")
        sys.exit(1)

    Solver().run()
