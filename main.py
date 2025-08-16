import random
import os
import time


ROWS, COLS = 38, 100 


def glider_gun_state(rows: int, cols: int):
    # Create a new, empty board
    board = dead_state(rows, cols)

    # Coordinates for the Gosper Glider Gun pattern
    live_cells = [
        (1, 25), (2, 23), (2, 25), (3, 13), (3, 14), (3, 21), (3, 22),
        (3, 35), (3, 36), (4, 12), (4, 16), (4, 21), (4, 22), (4, 35),
        (4, 36), (5, 1), (5, 2), (5, 11), (5, 17), (5, 21), (5, 22),
        (6, 1), (6, 2), (6, 11), (6, 15), (6, 17), (6, 18), (6, 23),
        (6, 25), (7, 11), (7, 17), (7, 25), (8, 12), (8, 16), (9, 13),
        (9, 14), (10, 21), (10, 22), (11, 23), (11, 25)
    ]

    # Set the specified cells to be alive (1)
    for r, c in live_cells:
        # Check if the coordinates are within the board bounds
        if 0 <= r < rows and 0 <= c < cols:
            board[r][c] = 1

    return board


def dead_state(rows: int, cols: int):
    board = []

    # create lines
    for row in range(rows):
        # new list for every line
        new_row= []

        # fill every line with seven 0
        for col in range(cols):
            new_row.append(0)
        
        # fill the board with the new line
        board.append(new_row)
    
    return board


def random_state(rows: int, cols: int):
    state = dead_state(rows, cols)
    
    # randomize each element of 'state'
    for r in range(rows):
        for c in range(cols):
            random_number = random.random()

            if random_number >= 0.28:
                state[r][c] = 1
            else:
                state[r][c] = 0

    return state


def count_live_neighbors(board, row, col):
    rows = len(board)
    cols = len(board[0]) # takes the first row and calculate the lenght of it

    live_neighbors: int = 0 

    for i in range(max(0, row-1), min(rows, row+2)):
        for j in range(max(0, col-1), min(cols, col+2)):
            #skip the center cell
            if(i,j) == (row, col): 
                continue
            
            if board[i][j] == 1: live_neighbors += 1

    return live_neighbors


def next_state_board(board):
    rows = len(board)
    cols = len(board[0])

    new_board = dead_state(rows, cols)

    for row in range(rows):
        for col in range(cols):
            live_neighbors = count_live_neighbors(board, row, col)
            current_cell_state = board[row][col]

            if current_cell_state == 1: # current cell is alive
                if live_neighbors == 2 or live_neighbors == 3:
                    new_board[row][col] = 1 # survives

                # otherwise, it dies from underpopulation / overpopulation
                
            else: # if the current cell is dead
                if live_neighbors == 3:
                    new_board[row][col] = 1 # becomes alive

    return new_board

    
def render(board): #with ANSI code implementation
    """
    Print the state of the grid 'board' 
    Live cells '1' are represented by #, dead one with ' '
    """

    # delete the grid and move the cursor on top
    print("\033[H\033[2J", end="")


    for row in board:
        row_str = ''

        for cell in row:
            if cell == 1:
                row_str += '#' # live cell
            else:
                row_str += ' ' # dead cell
        
        print(row_str)
        

def main():
    board = glider_gun_state(ROWS, COLS)

    while True:
        render(board)
        time.sleep(0.08)
        board = next_state_board(board)


if __name__ == '__main__':
    main()
