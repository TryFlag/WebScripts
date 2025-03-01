import os
from random import randint

board = []

for x in range(0, 5):
    board.append(["O"] * 5)

def print_board(board):
    print("┌───────────┐")
    for i, row in enumerate(board):
        print(f"│ {' '.join(row)} │")
    print("└───────────┘")

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

print(ship_row + 1)
print(ship_col + 1)

for turn in range(10):
    os.system('clear')
    
    print("Turn", turn + 1, '/10')
    print_board(board)
    
    try:
        guess_row = int(input("Guess Row: ")) - 1
        guess_col = int(input("Guess Col: ")) - 1
    except ValueError:
        print("Invalid input. Enter a number.")
        input("\nPress Enter to continue...")
        continue

    if guess_row == ship_row and guess_col == ship_col:
        os.system('clear')
        print("Congratulations on wasting some time")
        print_board(board)
        break
    else:
        if guess_row not in range(5) or guess_col not in range(5):
            print("Oops, look who's a dumbass, that's outside the playing field")
        elif board[guess_row][guess_col] == "X":
            print("You might need some glasses, you guessed that one already")
        else:
            print("Try again buddy")
            board[guess_row][guess_col] = "X"
        if turn == 9:
            print("Game Over")
            print(f"The ship was at Row {ship_row + 1}, Col {ship_col + 1}")

    input("\nPress Enter to continue...")
