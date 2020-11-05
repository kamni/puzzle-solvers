#!/usr/bin/env python3

"""
This is a variation of the sudoku square, where you have numbers 2-10 and the
totals need to add up to 18 in all directions.
"""

import random
from copy import deepcopy

# This is the game's default config for the puzzle
DEFAULT_CONFIG = [
    [0, 0, 0],
    [4, 0, 0],
    [0, 10, 0],
]

NUMBERS = set(range(2, 11))


def solve(starting_config):
    def _check_diagonals(square_config):
        diags = [
            [square_config[0][0], square_config[1][1], square_config[2][2]],
            [square_config[0][2], square_config[1][1], square_config[2][0]],
        ]
        return _check_horizontals(diags)

    def _check_horizontals(square_config):
        return all([
            all(row) and sum(row) == 18
            for row in square_config
        ])

    def _check_verticals(square_config):
        columns = [
            [square_config[row][column] for row, _ in enumerate(square_config)]
            for column in range(len(square_config[0]))
        ]
        return _check_horizontals(columns)

    def _format_number(num):
        if num < 10:
            return " {}".format(num)
        return "{}".format(num)

    def _generate_next_solutions(square_config):
        unused_numbers = _get_unused_numbers(square_config)

        next_solutions = []
        for num in unused_numbers:
            newsol = deepcopy(square_config)

            found = False
            for row, array in enumerate(newsol):
                for col, val in enumerate(array):
                    if val == 0:
                        newsol[row][col] = num
                        next_solutions.append(newsol)
                        found = True
                        break

                if found:
                    break

        return next_solutions

    def _get_unused_numbers(square_config):
        used = set()
        for row in square_config:
            used = used.union(set(row))
        used = used.difference({0})
        return NUMBERS.difference(used)

    def _is_solved(list_of_solutions):
        for potential_solution in list_of_solutions:
            if all([
                _check_horizontals(potential_solution),
                _check_verticals(potential_solution),
                _check_diagonals(potential_solution),
            ]):
                return potential_solution

        return None

    def _print_solution(square_config):
        if not square_config:
            print("No solution was found")
        else:
            print("+--+--+--+")
            for row in square_config:
                line = "|"
                for column in row:
                    line += _format_number(column) + "|"
                print(line)
            print("+--+--+--+")

    queue = [starting_config]
    solution = None

    while not solution and queue:
        unsolved = queue.pop()
        next_solutions = _generate_next_solutions(unsolved)

        solution = _is_solved(next_solutions)
        if not solution:
            queue.extend(next_solutions)

    _print_solution(solution)


if __name__ == '__main__':
   solve(DEFAULT_CONFIG)
