import PySimpleGUI as sg
import time
import copy


# Defines what could possibly fill the sudoku board
class filler:
    value = 0
    possible_values = []

    # Constructor
    def __init__(self):
        # No value
        self.value = 0

        # All values possible 
        self.possible_values = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    # Function returns whether the square has a value
    def has_value(self):

        if self.value != 0:
            return 1
        else:
            return 0

    # Function returns whether there are any possible moves and what the first one is
    def return_first_possibility(self):

        for i in range(0, 9):

            if self.possible_values[i] == 1:
                # Returns first possibility
                return i + 1
        # If it has tried all 9 possibilities, nothing is possible
        return 0

    def self_check_one_left(self, puzzle, k, l ):

        if self.has_value() == 0:
            counter = 0
            test_value = 0

            for i in range(9):

                if self.possible_values[i] == 1:
                    counter += 1
                    test_value = i+1

            if counter == 1:
                # print('ONLY OPTION LEFT AT ', k, ', ', l, ' is ', test_value)
                self.value = test_value
                update_box( puzzle, k, l, test_value )

        return



def input_puzzle():
    layout = [[sg.Text('Please enter sudoku below:')],
              [[sg.InputText(size=(2, 1)) for i in range(9)] for j in range(9)],
              [sg.Button('Done', size=(4, 2))]]

    window = sg.Window('Sudoku Solver', layout)
    event, values = window.read()

    return values


def build_puzzle(values):
    puzzle = [[filler() for i in range(9)] for j in range(9)]

    value_counter = 0

    for i in range(9):
        for j in range(9):
            if values[value_counter] != '': # values[value_counter] > 0:
                puzzle[i][j].value = int(values[value_counter])
            else:
                puzzle[i][j].value = 0
            value_counter += 1

    for i in range(9):
        for j in range(9):
            if puzzle[i][j].has_value() != 0:
                puzzle = update_box(puzzle, i, j, puzzle[i][j].value)

    return puzzle


def print_puzzle(puzzle):
    for i in range(9):
        for j in range(9):
            print(puzzle[i][j].value, end=' ')
        print()
    print()


def update_box(puzzle, i, j, number):
    bottom_left_corner_i = i - (i % 3)
    bottom_left_corner_j = j - (j % 3)

    for k in range(3):
        for l in range(3):
            if puzzle[bottom_left_corner_i+k][bottom_left_corner_j+l].has_value() == 0:
                # print( '1Eliminating ', number, ' at ', bottom_left_corner_i + k, ', ', bottom_left_corner_j+l )
                puzzle[bottom_left_corner_i+k][bottom_left_corner_j+l].possible_values[number - 1] = 0
                #puzzle[bottom_left_corner_i + k][bottom_left_corner_j + l].self_check_one_left(puzzle, bottom_left_corner_i+k,bottom_left_corner_j+l)

    for k in range(9):
        if puzzle[i][k].has_value() == 0:
            # print('2Eliminating ', number, ' at ', i, ', ', k)
            puzzle[i][k].possible_values[number-1] = 0
            #puzzle[i][k].self_check_one_left(puzzle, i, k)

    for k in range(9):
        if puzzle[k][j].has_value() == 0:
            # print('3Eliminating ', number, ' at ', k, ', ', j)
            puzzle[k][j].possible_values[number - 1] = 0
            #puzzle[k][j].self_check_one_left(puzzle, k, j)

    for k in range(9):
        for l in range(9):
            puzzle[k][l].self_check_one_left(puzzle, k, l)

    return puzzle


def solve_puzzle(puzzle):
    for i in range(9):
        for j in range(9):
            # puzzle[i][j].self_check_one_left(puzzle, i, j)
            if puzzle[i][j].has_value() == 0:
                for k in range(9):
                    if( puzzle[i][j].possible_values[k] == 1 ):
                        temp = copy.deepcopy(puzzle)

                        # print('Plugging in ', k+1, ' to ', i, ', ', j )

                        temp[i][j].value = k+1
                        temp = update_box(temp, i, j, k+1 )
                        result = solve_puzzle(temp)

                        if(result != 0 ):
                            return result
                # print('Reached end, no solutions on this path')
                return 0
    return puzzle


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting')

    # Test puzzle for debugging
    # values = [0,0,0,6,0,4,1,0,2,
    #           4,0,0,0,0,3,7,5,0,
    #           0,9,0,2,0,0,0,0,0,
    #           1,0,2,4,3,0,8,7,6,
    #           0,6,0,7,1,0,0,0,0,
    #           9,7,4,8,5,0,2,0,3,
    #           0,0,0,0,0,7,0,0,5,
    #           2,0,5,3,0,0,0,0,0,
    #           0,3,9,0,0,0,6,2,0]

    # values = [0,0,0,8,0,0,0,0,0,
    #           8,0,0,0,0,0,6,0,0,
    #           4,0,0,2,5,0,0,0,8,
    #           0,6,8,0,2,0,3,0,0,
    #           3,0,0,9,0,0,7,8,0,
    #           1,0,7,0,0,0,0,5,0,
    #           0,8,0,0,3,0,0,7,0,
    #           2,0,9,7,6,4,0,0,0,
    #           0,0,4,5,0,0,2,6,0]

    # values = [8,0,0,0,0,0,0,0,0,
    #           0,0,3,6,0,0,0,0,0,
    #           0,7,0,0,9,0,2,0,0,
    #           0,5,0,0,0,7,0,0,0,
    #           0,0,0,0,4,5,7,0,0,
    #           0,0,0,1,0,0,0,3,0,
    #           0,0,1,0,0,0,0,6,8,
    #           0,0,8,5,0,0,0,1,0,
    #           0,9,0,0,0,0,4,0,0]
    values = input_puzzle()
    start = time.time()
    puzzle = build_puzzle(values)
    print('\nSOLVING\n')
    puzzle = solve_puzzle(puzzle)
    end = time.time()
    print_puzzle(puzzle)
    print('Done: ', (end - start), ' elapsed')


