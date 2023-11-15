import pandas as pd
import numpy as np
import random


pd.set_option("display.max_columns", None)


class Partie:
    """ """

    def __init__(self, Q=dict(), gamma=0):
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
        self.Q = Q
        self.states = []
        self.moves = 0
        self.gamma = gamma

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

    def explore(self, possible):
        return random.choice(possible)
    
    def exploite(self, possible):
        state = self.board.copy().to_string()
        if state in self.Q:
            return Q_model(state, self.Q)
        else:
            return self.explore(possible)
        
    def action(self):
        possible = []
        for y in ["a", "b", "c"]:
            for x in ["1", "2", "3"]:
                if self.board.loc[x, y] == "-":
                    possible.append(y + x)
        i = random.randint(1,3000)
        if self.gamma > i:
            return possible, self.exploite(possible)
        else:
            return possible, self.explore(possible)

    def launch(self):
        while True:
            possible, position = self.action()
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


def update_q_table(results, q):
    ref = {"X": 1, "O": -1, "Draw": 0}
    X_results = [item for item in results["states"] if item.get("player") == "X"]
    for i, rev_state in enumerate(X_results[::-1]):
        if i == 0:
            q[rev_state["state"]][rev_state["action"]] = 0.9 * ref[results["result"]]
        else:
            prev_state = X_results[::-1][i - 1]["state"]
            q[rev_state["state"]][rev_state["action"]] = 0.9 * max(q[f"{prev_state}"].values())

    return q


def fusion_q_Q(q, Q):
    for state in list(q.keys()):
        if state in Q:
            for possible in list(q[state].keys()):
                Q[state][possible] = np.mean([q[state][possible], Q[state][possible]])
                Q[state][possible] = Q[state][possible] + max()
        else:
            Q[state] = q[state]
        next_reward=Q[state]
    return Q



def train_bot(n, Q=dict()):
    win = 0
    draw = 0
    for i in range(n):
        q = dict()
        partie = Partie(Q, i)
        results = partie.launch()
        if results["result"] == "X":
            win += 1
        if results["result"] == "Draw":
            draw += 1
        for state in results["states"]:
            if state["player"] == "X":
                q[state["state"]] = {f"{possible}": 0 for possible in state["possibles"]}

        q = update_q_table(results, q)

        Q = fusion_q_Q(q, Q)

    return Q, win, draw

def play_against_bot(n, Q=dict()):
    win = 0
    draw = 0
    for i in range(n):
        q = dict()
        partie = Partie(Q, n)
        results = partie.launch()
        if results["result"] == "X":
            win += 1
        if results["result"] == "Draw":
            draw += 1
        for state in results["states"]:
            if state["player"] == "X":
                q[state["state"]] = {f"{possible}": 0 for possible in state["possibles"]}

        q = update_q_table(results, q)

        Q = fusion_q_Q(q, Q)

    return Q, win, draw

def Q_model(state, Q):
    return max(Q[state], key=Q[state].get)

if __name__ == "__main__":
    Q, win1, draw = train_bot(3000)
    Qtest, win2, draw2 = play_against_bot(1000, Q)
    print(win2, draw2)
