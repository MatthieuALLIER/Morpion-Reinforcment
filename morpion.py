import pandas as pd
import random


pd.set_option("display.max_columns", None)
# def play_morpion():

#     board = pd.DataFrame(
#         {
#             "a": ["-", "-", "-"],
#             "b": ["-", "-", "-"],
#             "c": ["-", "-", "-"],
#         },
#         index=["1", "2", "3"],
#     )

#     print(board)

#     i = 1

#     while True:
#         cell = input("choose your cell between a1 to c3: ")
#         if board[cell[0]][cell[1]] == "-":
#             signe = "X" if i % 2 == 1 else "O"
#             is_signe_diag1 = True if cell in ["a1", "b2", "c3"] else False
#             is_signe_diag2 = True if cell in ["a3", "b2", "c1"] else False
#             board[cell[0]][cell[1]] = signe
#             i += 1
#             print(board)
#         else:
#             print("cell already taken !!!!!!!!!!!!!!!!!!")

#         if i > 9:
#             print("c'est finito")
#             break

#         if is_signe_diag1:
#             if len(set([board["a"]["1"], board["b"]["2"], board["c"]["3"]])) == 1:
#                 print(f"le gagnant est '{signe}'")
#                 break

#         if is_signe_diag2:
#             if len(set([board["a"]["3"], board["b"]["2"], board["c"]["1"]])) == 1:
#                 print(f"le gagnant est '{signe}'")
#                 break

#         if len(set(board[cell[0]])) == 1 or len(set(board.loc[cell[1]])) == 1:
#             print(f"le gagnant est '{signe}'")
#             break


class Partie:
    """ """

    def __init__(self, modele=random.choice):
        self.players = ["X", "O"]
        self.board = pd.DataFrame(
            {
                "a": ["-", "-", "-"],
                "b": ["-", "-", "-"],
                "c": ["-", "-", "-"],
            },
            index=["1", "2", "3"],
        )
        self.end = False
        self.actual_player = "X"
        self.modele = modele
        self.states = []
        self.moves = 0

    def switch_player(self):
        self.actual_player = self.players[0] if self.actual_player == "O" else self.players[1]

    def move(self, position):
        self.board[position[0]][position[1]] = self.actual_player
        self.moves += 1
        self.end = self.check_end(self.actual_player, position)
        self.switch_player()

    def check_end(self, player, position):

        is_player_diag1 = True if position in ["a1", "b2", "c3"] else False
        is_player_diag2 = True if position in ["a3", "b2", "c1"] else False

        if is_player_diag1:
            if (
                len(
                    set(
                        [
                            self.board["a"]["1"],
                            self.board["b"]["2"],
                            self.board["c"]["3"],
                        ]
                    )
                )
                == 1
            ):
                return player

        if is_player_diag2:
            if (
                len(
                    set(
                        [
                            self.board["a"]["3"],
                            self.board["b"]["2"],
                            self.board["c"]["1"],
                        ]
                    )
                )
                == 1
            ):
                return player

        if len(set(self.board[position[0]])) == 1 or len(set(self.board.loc[position[1]])) == 1:
            return player

        if not self.board.isin(["-"]).any().any():
            return "Draw"

        return False

    def explore(self):
        Q_possible = []
        possible = []
        for y in ["a", "b", "c"]:
            for x in ["1", "2", "3"]:
                if self.board.loc[x, y] == "-":
                    Q_possible.append({"action": y + x, "gain": 0})
                    possible.append(y + x)
        return possible, random.choice(possible)

    def launch(self):
        while True:
            if random.random() <= 1:
                possible, position = self.explore()
            else:
                possible, position = self.modele(self.player, self.board)
            state_action = {
                "player": self.actual_player,
                "state": self.board.copy().to_string(),
                "possibles": possible,
                "action": position,
                "move": self.moves,
            }
            self.states.append(state_action)
            self.move(position)
            # self.shob()
            if isinstance(self.end, str):
                return {"states": self.states, "result": self.end}

    def shob(self):
        print(self.board)


def train_bot():
    Q = pd.DataFrame(columns=["board", "possible"])
    ref = {"X": 1, "O": -1, "Draw": 0}

    for i in range(1):
        partie = Partie(random.choice)
        results = partie.launch()
        print(results["result"])
        X_results = [d for d in results["states"] if d.get("player") == "X"]
        for state in X_results:
            Q = pd.concat(
                [
                    Q,
                    pd.DataFrame(
                        {
                            "board": state["state"],
                            "possible": [{f"{item}": 0 for item in state["possibles"]}],
                        }
                    ),
                ]
            ).reset_index(drop=True)

        for st in range(len(Q) - 1, -1, -1):
            r = ref[results["result"]] if st == len(Q) - 1 else Q.iloc[st + 1, 1][X_results[st + 1]["action"]]
            Q.iloc[st, 1][X_results[st]["action"]] = 0.9 * r

    return Q


if __name__ == "__main__":
    Q = train_bot()
    print(Q)
