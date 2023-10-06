import pandas as pd

board = {
    "a": ["-", "-", "-"],
    "b": ["-", "-", "-"],
    "c": ["-", "-", "-"],
}

board = pd.DataFrame(board)
board.index = ["1","2","3"]
# def print_board(board):
#     for key, value in board.items():
#         a, b, c = value
#         print("{:<10} {:<10} {:<10}".format(a, b, c))


print(board)

i = 1

while True:
    cell = input("choose your cell between a1 to c3: ")
    if board[cell[0]][cell[1]] == "-":
        signe = "X" if i % 2 == 1 else "O"
        board[cell[0]][cell[1]] = signe
        i += 1
        print(board)
    else:
        print("cell already taken !!!!!!!!!!!!!!!!!!")

    if i > 9:
        print("c'est finito")
        break

    if len(set(board[cell[0]])) == 1 or len(set(board.loc[[cell[1]]])) == 1:
        print(f"le gagnant est '{signe}'")
        break
