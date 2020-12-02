import time
from sys import argv, version_info
from queue import PriorityQueue
import numpy as np

from utils import calculate_permutations, check_answer, has_answer, tuplize, REQ_VERSION

MATRIX_SIZE = 3

def find_wanted_position(number, output):
    wanted_position_x, wanted_position_y = np.where(output == number)
    wanted_position_x = wanted_position_x[0]
    wanted_position_y = wanted_position_y[0]

    return [wanted_position_x, wanted_position_y]

def calculate_heuristic(matrix, output, h):
    """
    1) We use the Manhattan Distance between the given piece and where it should be on the board
    2) We use the number of misplaced elements
    """
    cost = 0
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            num = matrix[i][j]
            correct_row = find_wanted_position(num, output)[0]
            correct_col = find_wanted_position(num, output)[1]

            if h == 2:
                cost += int(i != correct_row or j != correct_col)
            elif h == 1:
                cost += abs(i - correct_row) + abs(j - correct_col)
    return cost


def solve(grid, output, heuristic):

    if version_info < REQ_VERSION:
        print("Python version too low! Please use", REQ_VERSION, "or later.")

    test_case = grid


    start = time.time()
    answer = "This puzzle is not solvable."
    queue = PriorityQueue()
    visited = set()

    if not has_answer(test_case):
        print("TIME: "+str(time.time() - start), "   ---   ANSWER: "+str(answer))
        return

    """
    The queue follows the order
        total cost, level, matrix, answer
    for all elements """
    queue.put((0, 0, test_case, ""))
    while not queue.empty():
        _, level, matrix, current_answer = queue.get()

        if level > 50:
            break

        if check_answer(matrix, output):
            answer = current_answer
            break

        permutations = calculate_permutations(matrix)

        for permutation, letter in permutations:
            # A tuple is necessary for storing in a set since it is immutable
            permutation_tuple = tuplize(permutation)
            if permutation_tuple not in visited:
                heuristic_cost = calculate_heuristic(permutation, output, heuristic)
                visited.add(permutation_tuple)
                queue.put((heuristic_cost+level+1,
                            level+1,
                            permutation,
                            (current_answer + letter
                            )))

    print("TIME: "+str(time.time() - start), "   ---   ANSWER: "+str(answer))
    print("Emulating answer ...")
    return answer

if __name__ == "__main__":
    solve()
