# -*- coding: utf-8 -*-

# REQUIRES PYTHON >= 3.8

"""
Solver for the Mystic Pillars video game.

## How to use the script:

  1. Set up a goal, an initial_config, and max_turns in puzzle_config.py.
  2. Save, and run the script.
  3. The output shows you how many stones to shift to which pillars.

"""

from typing import Dict, List, Optional, Set, Tuple, TypedDict

from puzzle_config import PUZZLES


###############################################################################

# TYPE DEFINITIONS

# Iterable of tuples describing the layout of the current board. First number in
# the tuple is the column number; second number is the number of stones sitting
# on the column.
Pillar = Tuple[int, int]
BoardPositions = Tuple[Pillar]

# Iterable of tuples describing distance to each of the pillars relative to another
# pillar. First number of the tuple is the column number to move stones to;
# second number is the distance (number of hops) stones must be moved to reach
# that pillar. If the distance is 0, then the stones are either already at the
# pillar, or the pillar is unreachable.
PillarDistance = Tuple[Tuple[int, int]]

# Tuple representing a move in the game. First number of the tuple is the
# number of the pillar to move from; second is the number of the pillar to move
# to
GameMove = Tuple[int, int]

class PuzzleConfig(TypedDict):
    max_turns: int
    initial: BoardPositions
    goal: BoardPositions
    config: Tuple[PillarDistance]

# Dictionary of puzzle configurations. The key is the number of the puzzle
MultiplePuzzleConfig = Dict[int, PuzzleConfig]

AlreadySeenMoves = Set[int]
BoardState = Tuple[BoardPositions, List[GameMove]]
BoardQueue = Tuple[List[BoardState], AlreadySeenMoves]

class Solution(TypedDict):
    status: str  # solved, unsolved
    steps: List[GameMove]
    debug: Optional[List[List[GameMove]]]

###############################################################################

# SOLVER

def solve(puzzle_config: PuzzleConfig) -> Solution:
    NO_SOLUTION = {
        'status': 'no_solution',
        'steps': [],
        'debug': [],
    }
    FAILURE_SOLUTION = {
        'status': 'failed',
        'steps': [],
        'debug': [],
    }

    max_turns: int = puzzle_config['max_turns']
    initial: BoardPositions = puzzle_config['initial']
    goal: BoardPositions = puzzle_config['goal']
    config: PillarDistance = puzzle_config['config']

    # Optimization magic -- we can cut down on how much searching we do if we
    # can guess that the number of filled goal pillars matches the number of
    # initially-filled pillars, implying each pillar only needs to be moved
    # once
    min_turns: int = abs(
        sum([1 for pillar in initial if pillar[1] > 0]) -
        sum([1 for pillar in goal if pillar[1] > 0])
    )
    total_initial_value: int = sum(pillar[1] for pillar in initial)
    total_goal_value: int = sum(pillar[1] for pillar in goal)
    IS_NOT_SOLVEABLE: bool = (
        min_turns > max_turns or
        total_initial_value != total_goal_value
    )

    if IS_NOT_SOLVEABLE:
        return NO_SOLUTION

    ########################### HELPER METHODS ################################

    def _hash_state(position_list: BoardPositions) -> int:
        return hash(position_list)

    def _seed_queue(
        current_state: BoardState,
        solutions_already_seen: AlreadySeenMoves,
    ) -> BoardQueue:

        # Helper methods
        def _find_new_state(
                current_pillar_info: Tuple[int, Pillar],
                target_pillar_info: Tuple[int, Pillar],
                already_seen_in_run: AlreadySeenMoves,
                already_seen_global: AlreadySeenMoves,
                old_pillars: BoardPositions,
                old_steps: List[GameMove],
        ) -> Tuple[BoardState, int]:

            current_pillar_idx, current_pillar = current_pillar_info
            target_pillar_idx, target_pillar = target_pillar_info

            value_offset: int = _get_pillar_offset(
                current_pillar_idx,
                target_pillar_idx,
            )
            if _is_illegal_move(current_pillar, value_offset):
                empty_response: Tuple[BoardState, int] = ((None, []), 0)
                return empty_response

            new_pillars: BoardPositions = _get_new_pillars(
                current_pillar,
                current_pillar_idx,
                target_pillar,
                target_pillar_idx,
                value_offset,
                old_pillars,
            )
            new_steps: List[GameMove] = _get_new_steps(
                current_pillar,
                target_pillar,
                old_steps,
            )

            new_state_hash: int = _hash_state(new_pillars)
            if (
                new_state_hash in already_seen_in_run or
                new_state_hash in already_seen_global
            ):
                invalid_response: Tuple[BoardState, int] = (
                    (None, []),
                    new_state_hash,
                )
                return invalid_response

            valid_response: Tuple[BoardState, int] = (
                (new_pillars, new_steps),
                new_state_hash,
            )
            return valid_response

        def _get_new_pillars(
                from_pillar: Pillar,
                from_idx: int,
                to_pillar: Pillar,
                to_idx: int,
                value_offset: int,
                old_pillars: BoardPositions,
        ) -> BoardPositions:

            new_pillars = list(old_pillars)

            new_from = (from_pillar[0], from_pillar[1] - value_offset)
            new_to = (to_pillar[0], to_pillar[1] + value_offset)
            new_pillars[from_idx] = new_from
            new_pillars[to_idx] = new_to

            return tuple(new_pillars)

        def _get_new_steps(
                from_pillar: Pillar,
                to_pillar: Pillar,
                steps: List[GameMove],
        ) -> List[GameMove]:
            new_steps = steps[:]
            new_steps.append((from_pillar[0], to_pillar[0]))
            return new_steps

        def _get_pillar_offset(
                pillar1_index: int,
                pillar2_index: int,
        ) -> int:
            return config[pillar1_index][pillar2_index][1]

        def _is_illegal_move(
                pillar: Pillar,
                offset_from_pillar: int,
        ) -> bool:
            value_for_pillar = pillar[1]

            return (
                offset_from_pillar <= 0 or
                offset_from_pillar > value_for_pillar
            )

        #################### BEGIN MAIN FUNCTION EXECUTION ####################

        queue: List[BoardState] = []
        pillars, steps = current_state
        already_seen_in_run: AlreadySeenMoves = set()

        for current_pillar in enumerate(pillars):
            for target_pillar in enumerate(pillars):
                new_state, seen_state = _find_new_state(
                    current_pillar,
                    target_pillar,
                    already_seen_in_run,
                    solutions_already_seen,
                    pillars,
                    steps,
                )
                if new_state[0] is not None:
                    queue.append(new_state)
                already_seen_in_run.add(seen_state)

        next_queue: BoardQueue = (queue, already_seen_in_run)
        return next_queue

    def _is_close_to_goal(
            current_position: BoardPositions,
            goal: BoardPositions,
            max_value_difference: int=2,
    ) -> bool:
        # NOTE: max_value_difference should always be a multiple of 2,
        # because if a pillar has one too many stones, there should be
        # a corresponding pillar that has one too few stones.
        off_by = sum([
            abs(current_position[idx][1] - goal[idx][1])
            for idx in range(len(goal))
        ])
        return off_by <= max_value_difference

    def _is_solved(
            current_position: BoardPositions,
            goal_position: BoardPositions,
    ) -> bool:
        return current_position == goal_position

    # This is a ridiculously ugly function. It's got a runtime of approximately:
    #
    #    O(n) = E(i->k) (n^2)^i
    #
    # where n is the number of pillars, k is the number of moves, and E is
    # the summation function.
    #
    # We don't have to explore all of these, so we speed up the function by
    # tracking what we've already seen and trying to parallelize some of the
    # operations
    def main(
            queue: List[BoardState],
            goal: BoardPositions,
    ) -> Tuple[Optional[Solution], Optional[List[BoardState]]]:
        solutions_already_seen: AlreadySeenMoves = set()

        debugging_queue: List[BoardState] = []
        while queue:
            current_position, steps = queue.pop()

            if _is_solved(current_position, goal):
                solution: Solution = {
                    'status': 'solved',
                    'steps': steps,
                    'debug': [],
                }
                return (solution, [])

            if _is_close_to_goal(current_position, goal):
                close_state: BoardState = (current_position, steps)
                debugging_queue.append(close_state)

            if len(steps) >= max_turns:
                    continue
            else:
                new_states, seen_states = _seed_queue(
                    (current_position, steps),
                    solutions_already_seen,
                )
                solutions_already_seen.update(seen_states)
                queue.extend(new_states)

        return (None, debugging_queue)

    # Begin main function execution

    queue: List[BoardState] = [(initial, [])]
    solution, debugging_queue = main(queue, goal)

    if not solution:
        solution = FAILURE_SOLUTION.copy()
        solution['debug'] = debugging_queue

    return solution


def pretty_print(solution: Solution, puzzle_number: int):
    DIVIDER = '--------'

    def _print_formatted_list(step_list: List[GameMove]):
        for idx, step in enumerate(step_list):
            print(
                '  {num}. Move stones from pillar {p1} to {p2}'.format(
                    num=idx + 1,
                    p1=step[0],
                    p2=step[1],
                ),
            )

    # Begin main function execution
    print(DIVIDER)

    if solution['status'] == 'solved':
        print(f'Solved puzzle #{puzzle_number}!\n')
        _print_formatted_list(solution['steps'])
    elif solution['status'] == 'no_solution':
        print(f'No solution to puzzle #{puzzle_number} for the constraints provided')
    else:
        print(f'Several close solutions were almost found for puzzle #{puzzle_number}:\n')
        debug_queue = solution['debug'][:5]
        for _, steps in debug_queue:
            _print_formatted_list(steps)
            print('****')

    print(DIVIDER)




###############################################################################

if __name__ == '__main__':
    from timeit import timeit

    def runme():
        for puzzle_number, config in PUZZLES.items():
            solution = solve(config)
            pretty_print(solution, puzzle_number)

    print(timeit(runme, number=1))
