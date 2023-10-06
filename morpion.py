import pandas as pd

def play_morpion():
    board = {
        "a": ["-", "-", "-"],
        "b": ["-", "-", "-"],
        "c": ["-", "-", "-"],
    }

    board = pd.DataFrame(board)
    board.index = ["1","2","3"]

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
                print(f"le gagnant est '{signe}'")
                break

        if is_signe_diag2:
            if len(set([board["a"]["3"], board["b"]["2"], board["c"]["1"]])) == 1:
                print(f"le gagnant est '{signe}'")
                break

        if len(set(board[cell[0]])) == 1 or len(set(board.loc[cell[1]])) == 1:
            print(f"le gagnant est '{signe}'")
            break

if __name__ == "__main__":
    play_morpion()