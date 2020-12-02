
from copy import deepcopy
MATRIX_SIZE=3
REQ_VERSION = (3, 0)


def calculate_permutations(matrix):
    options = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]
    permutations = []
    row = col = -1
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            if matrix[i][j] == 0:
                row = i
                col = j

    for i, j, letter in options:
        if 0 <= row + i < MATRIX_SIZE and 0 <= col + j < MATRIX_SIZE:
            temp = deepcopy(matrix)  # creates a copy of the matrix so we dont change it in place
            temp[row][col], temp[row+i][col+j] = temp[row+i][col+j], temp[row][col]
            permutations.append((temp, letter))

    return permutations


#check if answer matches given output
def check_answer(matrix, output):
    test = True
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            if matrix[i][j] != output[i][j]:
                test = False
                break
    return(test)


def count_inversions(array):
    """Function for counting the amount of inversions in """
    count = 0
    size = MATRIX_SIZE*MATRIX_SIZE

    for i in range(size-1):
        for j in range(i+1, size):
            if array[i] != 0 and array[j] != 0 and array[i] > array[j]:
                count += 1

    return count


def has_answer(matrix):
    """For checking if the puzzle is solvable, we used the following side as a guide:
        http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    Resuming, the puzzle instance is solvable if
        the number of inversions is even (because N=3 is odd).
    """

    inversions = count_inversions([num for row in matrix for num in row])

    return ( inversions % 2 == 0 )


def tuplize(matrix):
    """Returns a linear version of a matrix"""
    return tuple([num for row in matrix for num in row])
