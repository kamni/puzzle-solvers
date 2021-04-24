# -*- coding: utf-8 -*-

# REQUIRES PYTHON >= 3.8

"""
Solver for the Mystic Pillars video game.

## How to use the script:

  1. Set up a goal, an initial_config, and max_turns in puzzle_config.py.
  2. Save, and run the script.
  3. The output shows you how many stones to shift to which pillars.

"""

from puzzle_config import PositionList, PillarDistance, PUZZLES, PuzzleConfig


def solve(initial, config, goal, max_turns):
    QUEUE = []
    ALREADY_SEEN = set()
    DEBUG_LIST = []

    # This is a little bit of optimization magic
    def _minimum_number_of_turns(initial, goal):
        filled_initial_pillars = sum([1 for pillar in initial if pillar[1] > 0])
        filled_solved_pillars = sum([1 for pillar in goal if pillar[1] > 0])
        return abs(filled_initial_pillars - filled_solved_pillars)

    ONLY_MOVE_A_PILLAR_ONCE = max_turns == _minimum_number_of_turns(initial, goal)

    # Helper methods
    def _hash_state(position_list: PositionList):
        return hash(position_list)


    def _seed_queue(current_state):
        # Helper methods

        def _get_new_pillars(from_pillar, from_idx, to_pillar, to_idx, value_offset):
            new_pillars = list(pillars)

            new_from = (from_pillar[0], from_pillar[1] - value_offset)
            new_to = (to_pillar[0], to_pillar[1] + value_offset)
            new_pillars[from_idx] = new_from
            new_pillars[to_idx] = new_to

            return tuple(new_pillars)

        def _get_new_steps(from_pillar, to_pillar):
            new_steps = steps[:]
            new_steps.append((from_pillar[0], to_pillar[0]))
            return new_steps

        def _get_pillar_offset(pillar1_index, pillar2_index):
            return config[pillar1_index][pillar2_index][1]

        def _is_illegal_move(pillar, offset_from_pillar):
            value_for_pillar = pillar[1]

            return (
                offset_from_pillar <= 0 or
                offset_from_pillar > value_for_pillar
            )

        def _number_of_steps_exceeded(step_list):
            return len(step_list) >= max_turns


        # Begin main function execution

        pillars, steps, already_seen_in_run = current_state
        if _number_of_steps_exceeded(steps):
            DEBUG_LIST.append(current_state)
            return

        for idx, current_pillar in enumerate(pillars):
            current_config = config[idx]

            for jdx, other_pillar in enumerate(pillars):
                value_offset = _get_pillar_offset(idx, jdx)

                if _is_illegal_move(current_pillar, value_offset):
                    continue

                new_pillars = _get_new_pillars(
                    current_pillar,
                    idx,
                    other_pillar,
                    jdx,
                    value_offset,
                )
                new_steps = _get_new_steps(
                    current_pillar,
                    other_pillar,
                )

                new_state_hash = _hash_state(new_pillars)
                if new_state_hash in already_seen_in_run:
                    continue

                already_seen_hash = f'{new_state_hash}_{len(new_steps)}'
                if already_seen_hash in ALREADY_SEEN:
                    continue

                new_already_seen = set(already_seen_in_run)
                if ONLY_MOVE_A_PILLAR_ONCE:
                    new_already_seen.add(jdx)
                else:
                    new_already_seen.add(new_state_hash)

                QUEUE.append((new_pillars, new_steps, already_seen_in_run))
                ALREADY_SEEN.add(already_seen_hash)


    def _is_not_solvable(initial, goal):
        min_turns = _minimum_number_of_turns(initial, goal)
        total_initial_value = sum(pillar[1] for pillar in initial)
        total_goal_value = sum(pillar[1] for pillar in goal)
        return (
            min_turns > max_turns or
            total_initial_value != total_goal_value
        )

    def _is_solved(possible_solution):
        return possible_solution[0] == goal


    # Begin main function execution

    if _is_not_solvable(initial, goal):
        return (None, [])

    QUEUE.append((initial, [], set()))
    while QUEUE:
        tmp_solution = QUEUE.pop()
        if _is_solved(tmp_solution):
            return tmp_solution
        else:
            _seed_queue(tmp_solution)

    return (None, DEBUG_LIST, None)


def pretty_print(initial, solution):
    DIVIDER = '--------'

    # Helper functions

    def _is_close_to_goal(solution, max_value_difference=2):
        # NOTE: max_value_difference should always be a multiple of 2,
        # because if one pillar is off by 1 stone, then the stone is added
        # somewhere else
        off_by = sum([
            abs(solution[idx][1] - goal[idx][1])
            for idx in range(len(goal))
        ])
        return off_by <= max_value_difference

    def _print_formatted_list(step_list):
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

    pillars, steps, _ = solution
    if not pillars:
        print('No solution to the constraints provided')
        print('Close results (off by 2)')
        print(DIVIDER)

        steps.sort()
        for idx, (result, step_list) in enumerate(steps):
            if _is_close_to_goal(result):
                print(f'Attempted Solution #{idx}:\n')
                _print_formatted_list(step_list)
                print(DIVIDER)

    else:
        print('Solved!\n')
        _print_formatted_list(steps)
        print(DIVIDER)


###############################################################################

if __name__ == '__main__':
    from timeit import timeit

    def runme():
        puzzle = PUZZLES[47]
        solution = solve(
            puzzle['initial'],
            puzzle['config'],
            puzzle['goal'],
            puzzle['max_turns'],
        )
        pretty_print(puzzle['initial'], solution)

    print(timeit(runme, number=1))
