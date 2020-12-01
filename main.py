'''
    Compte Rendu TP1 IA GL4 par Mohamed Taieb SLAMA
'''




import sys
import os
from game.exception import GridSizeNotValidException, MoveException
from game.game import (
    build_grid, movable_tiles, move, is_grid_resolved, shuffle,build_grid_test,move_letter
)
from renderer.renderer import (
    welcome, goodbye, shuffling, starting_turn,
    victory, show_action_not_valid,
    show_grid, show_moves, show_menu_size, show_size_not_valid, ask_move, ask_size
)
from time import sleep
from a_star import solve


def router(action, grid, started_grid, shuffled):
    if action.lower().strip() == "s":
        print(shuffling())
        return [shuffle(grid), started_grid, True,True]
    elif action.lower() == "solve":

        print("Calculating solution...")
        
        answer = solve(np_array_to_matrix(grid))
        if answer != None:
            if answer =="":
                print("Matrix is already solved!")
            else:
                turn_number=1
                print("Solution: "+str(len(answer))+" turns")
                sleep(2)
                os.system('cls')
                print(starting_turn(turn_number))
                print(show_grid(grid))
                print(show_moves())
                for mv in answer:
                    print("Moving: ",mv)
                    sleep(1)
                    grid=move_letter(grid,mv)
                    os.system('cls')
                    print(starting_turn(turn_number))
                    print(show_grid(grid))
                    print(show_moves())
                    turn_number += 1
                print("SOLVED!")
                print("press ENTER to continue")
                input()
                return [grid,started_grid,False,True]
                    
    else:
        return [move_letter(grid, action), started_grid, True,False]


def np_array_to_matrix(grid):
    result=[]
    for l in list(grid):
        result.append(list(l))
    return result


def play_one_turn(grid, started_grid, turn_number, shuffled):
    os.system('cls')
    print(starting_turn(turn_number))
    print(show_grid(grid))
    print(show_moves())

    while True:

        action = input('\n%s' % ask_move("solve", "S"))

        try:
            return router(action, grid, started_grid, shuffled)
        except ValueError as e:
            print(str(e))
            if action == "q":
                print("GoodBye!")
                sys.exit()
            print('=> ' + show_action_not_valid(action))
            return
        except MoveException as error:
            print('=> ' + str(error))
            return


def play(grid_arg, started_grid_arg):
    turn_number = 1
    grid, started_grid, shuffled, just_shuffled = play_one_turn(grid_arg, started_grid_arg, turn_number, False)

    while not shuffled or not is_grid_resolved(grid, started_grid):
        if not shuffled:
            turn_number = 1
        grid, started_grid, shuffled, just_shuffled = play_one_turn(grid, started_grid, turn_number, shuffled)
        if just_shuffled:
            turn_number=0
        turn_number += 1
    return [grid, turn_number]


def init():
    os.system('cls')
    print('%s\n\n' % welcome())
    grid=build_grid_test()
    grid_started=build_grid()

    grid, turn_number = play(grid, grid_started)
    os.system('cls')
    print('\n\n%s' % victory(turn_number))
    print(show_grid(grid))


if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        print('\n' + goodbye())
        sys.exit(0)
