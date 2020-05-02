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

Then you need to specify the config. This is a nested list of tuples that
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
    [ (1, 0), (2, 1), (3, 2) ],
    [ (1, 1), (2, 0), (3, 1) ],
    [ (1, 2), (2, 1), (3, 0) ],
]
```

"""

# Set your solution constraints here.

###############################################################################

# Problem 29

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
    [ (1, 0), (2, 1), (3, 2), (4, 3), (5, 4) ],
    [ (1, 1), (2, 0), (3, 1), (4, 2), (5, 3) ],
    [ (1, 2), (2, 1), (3, 0), (4, 1), (5, 2) ],
    [ (1, 3), (2, 2), (3, 1), (4, 0), (5, 1) ],
    [ (1, 4), (2, 3), (3, 2), (4, 1), (5, 0) ],
]

###############################################################################

# Test example
#max_turns = 2
#
#initial = [
#    (1, 1),
#    (2, 1),
#    (3, 1),
#]
#
#goal = [
#    (1, 0),
#    (2, 0),
#    (3, 3),
#]
#
#config = [
#    [ (1, 0), (2, 1), (3, 2) ],
#    [ (1, 1), (2, 0), (3, 1) ],
#    [ (1, 2), (2, 1), (3, 0) ],
#]

#################### DON'T EDIT BELOW THIS LINE ###############################

def hash_state(pillar_list):
    return '-'.join([
        ':'.join([
            str(value)
            for value in pillar
        ])
        for pillar in pillar_list
    ])


def solve(intial, config, goal, max_turns):
    QUEUE = []
    ALREADY_SEEN = []
    DEBUG_LIST = []

    # Helper methods

    def _seed_queue(current_state):
        # Helper methods

        def _get_new_pillars(from_pillar, from_idx, to_pillar, to_idx, value_offset):
            new_pillars = pillars[:]

            new_from = (from_pillar[0], from_pillar[1] - value_offset)
            new_to = (to_pillar[0], to_pillar[1] + value_offset)
            new_pillars[from_idx] = new_from
            new_pillars[to_idx] = new_to

            return new_pillars

        def _get_new_steps(from_pillar, to_pillar):
            new_steps = steps[:]
            new_steps.append((from_pillar[0], to_pillar[0]))
            return new_steps

        def _get_pillar_offset(pillar1_index, pillar2_index):
            return config[pillar1_index][pillar2_index][1]

        def _is_illegal_move(pillar, offset_from_pillar):
            value_for_pillar = pillar[1]
            return offset_from_pillar > value_for_pillar

        def _number_of_steps_exceeded(step_list):
            return len(step_list) >= max_turns


        # Begin main function execution

        pillars, steps = current_state
        if _number_of_steps_exceeded(steps):
            DEBUG_LIST.append(current_state)
            return

        for idx, current_pillar in enumerate(pillars):
            current_config = config[idx]

            for jdx, other_pillar in enumerate(pillars):
                if other_pillar == current_pillar:
                    continue

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

                already_seen_hash = (
                    hash_state(new_pillars) + '_' + str(len(new_steps))
                )
                if already_seen_hash in ALREADY_SEEN:
                    continue
                else:
                    QUEUE.append((new_pillars, new_steps))
                    ALREADY_SEEN.append(already_seen_hash)


    def _is_not_solvable(initial, goal):
        total_initial_value = sum(pillar[1] for pillar in initial)
        total_goal_value = sum(pillar[1] for pillar in goal)
        return total_initial_value != total_goal_value

    def _is_solved(possible_solution):
        return possible_solution[0] == goal


    # Begin main function execution

    if _is_not_solvable(initial, goal):
        return (None, [])

    QUEUE.append((initial, []))
    while QUEUE:
        tmp_solution = QUEUE.pop()
        if _is_solved(tmp_solution):
            return tmp_solution
        else:
            _seed_queue(tmp_solution)

    return (None, DEBUG_LIST)


def pretty_print(solution):
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

    pillars, steps = solution
    if not pillars:
        print('No solution to the constraints provided')
        print('Close results (off by 2)')
        print(DIVIDER)

        steps.sort()
        for idx, (result, step_list) in enumerate(steps):
            if _is_close_to_goal(result):
                state = hash_state(result)

                print(f'Attempted Solution #{idx}:\n')
                _print_formatted_list(step_list)
                print(f'\nFinal State: {state}\n')
                print(DIVIDER)

    else:
        initial_state = hash_state(initial)
        final_state = hash_state(pillars)

        print('Solved!\n')
        print(f'Initial State: {initial_state}\n')
        _print_formatted_list(steps)
        print(f'\nFinal State: {final_state}\n')
        print(DIVIDER)


###############################################################################

if __name__ == '__main__':
    solution = solve(initial, config, goal, max_turns)
    pretty_print(solution)
