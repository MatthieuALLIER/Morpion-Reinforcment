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
        is_signe_diag1 = True if cell in ["a1","b2","c3"] else False
        is_signe_diag2 = True if cell in ["a3","b2","c1"] else False
        board[cell[0]][cell[1]] = signe
        i += 1
        print(board)
    else:
        print("cell already taken !!!!!!!!!!!!!!!!!!")

    if i > 9:
        print("c'est finito")
        break

    if is_signe_diag1:
        if len(set([board["a"]["1"], board["b"]["2"], board["c"]["3"]])) == 1:
            break

    if is_signe_diag2:
        if len(set([board["a"]["3"], board["b"]["2"], board["c"]["1"]])) == 1:
            break

    if board[cell[0]].is_unique() == 1 or board.loc[[cell[1]]].is_unique():
        print(f"le gagnant est '{signe}'")
        break
