#both players (minimax and minimax prob) are tested with depth = 2

from Board import BoardUtility
import random


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth
        
    def play(self, board):
        print('playOfMinimax')
        # Todo: implement minimax algorithm
        result = []
        maximum = -1
        for i in range(6):
            for j in range(6):
                if board[i][j] != 0:
                    continue
                board[i][j] = self.piece
                skip_value = self.minimax(True, self.depth - 1, board, -500, 500)
                if skip_value > maximum:
                    result = [[i, j], 1, "skip"]
                    maximum = skip_value
                for region in range(1, 5):
                    BoardUtility.rotate_region(board, region, "clockwise")
                    clockwise_value = self.minimax(True, self.depth - 1, board, float('-INF'), float('INF'))
                    if clockwise_value > maximum:
                        result = [[i, j], region, "clockwise"]
                        maximum = clockwise_value
                    BoardUtility.rotate_region(board, region, "anticlockwise")
                    BoardUtility.rotate_region(board, region, "anticlockwise")
                    anticlockwise_value = self.minimax(True, self.depth - 1, board, float('-INF'), float('INF'))
                    if anticlockwise_value > maximum:
                        result = [[i, j], region, "anticlockwise"]
                        maximum = anticlockwise_value
                    BoardUtility.rotate_region(board, region, "clockwise")
                board[i][j] = 0
        return result

    def minimax(self, my_turn, depth, board, alpha, beta):
        if depth == 0 or BoardUtility.is_terminal_state(board):
            if BoardUtility.has_player_won(board, self.piece) or depth == 0:
                return self.eval(board)
            return float('-INF')
        next_states = self.next_states_generator(board)
        if my_turn: #maximize
            max_value = float('-INF')
            for state in random.sample(next_states, min(20, len(next_states))):
                minimax = self.minimax(False, depth - 1, state, alpha, beta)
                max_value = max(minimax, max_value)
                alpha = max(alpha, minimax)
                if beta <= alpha:
                    break
            return minimax
        else: #minimize
            min_value = float('INF')
            for state in random.sample(next_states, min(20, len(next_states))):
                minimax = self.minimax(True, depth - 1, state, alpha, beta)
                min_value = min(minimax, min_value)
                beta = min(beta, minimax)
                if beta <= alpha:
                    break
            return minimax

    def next_states_generator(self, board):
        next_states = []
        for i in range(6):
            for j in range(6):
                if board[i][j] != 0:
                    continue
                board[i][j] = self.piece
                next_states.append(board)
                for region in range(1, 5):
                    BoardUtility.rotate_region(board, region, "clockwise")
                    next_states.append(board)
                    BoardUtility.rotate_region(board, region, "anticlockwise")
                    BoardUtility.rotate_region(board, region, "anticlockwise")
                    next_states.append(board)
                    BoardUtility.rotate_region(board, region, "clockwise")
                board[i][j] = 0
        #print(f'len of neighbors = {len(next_states)}')
        return next_states

    def eval(self, board):
        sum = 0
        for i in range(6):
            h_max = 0
            h_count = 0
            v_max = 0
            v_count = 0
            for j in range(6):
                if board[i][j] == self.piece:
                    h_count += 1
                else:
                    if h_count > h_max and board[i][j] == 0:
                        h_max = h_count
                    h_count = 0

                if board[j][j] == self.piece:
                    v_count += 1
                else:
                    if v_count > v_max and board[i][j] == 0:
                        v_max = v_count
                    v_count = 0
            if h_max == 5 or v_count == 5:
                return float('INF')
            sum += h_count ** 3
            sum += v_count ** 3

        d_count = 0
        d_max = 0
        for i in range(6):
            if board[i][i] == self.piece:
                d_count += 1
            else:
                if d_count > d_max and board[i][i] == 0:
                    d_max = d_count
        sum += d_max ** 2

        d_count = 0
        d_max = 0
        for i in range(5):
            if board[i][i + 1] == self.piece:
                d_count += 1
            else:
                if d_count > d_max and board[i][i + 1] == 0:
                    d_max = d_count
        sum += d_max ** 2

        d_count = 0
        d_max = 0
        for i in range(5):
            if board[i + 1][i] == self.piece:
                d_count += 1
            else:
                if d_count > d_max and board[i + 1][i] == 0:
                    d_max = d_count
        sum += d_max ** 2

        return sum

class MiniMaxProbPlayer(MiniMaxPlayer):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def play(self, board):
        # Todo: implement minimaxProb algorithm
        if random.random() < self.prob_stochastic:
            return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]
        result = []
        maximum = -1
        for i in range(6):
            for j in range(6):
                if board[i][j] != 0:
                    continue
                board[i][j] = self.piece
                skip_value = self.minimax(True, self.depth - 1, board, -500, 500)
                if skip_value > maximum:
                    result = [[i, j], 1, "skip"]
                    maximum = max(skip_value, maximum)
                for region in range(1, 5):
                    BoardUtility.rotate_region(board, region, "clockwise")
                    clockwise_value = self.minimax(True, self.depth - 1, board, float('-INF'), float('INF'))
                    if clockwise_value > maximum:
                        result = [[i, j], region, "clockwise"]
                        maximum = clockwise_value
                    BoardUtility.rotate_region(board, region, "anticlockwise")
                    BoardUtility.rotate_region(board, region, "anticlockwise")
                    anticlockwise_value = self.minimax(True, self.depth - 1, board, float('-INF'), float('INF'))
                    if anticlockwise_value > maximum:
                        result = [[i, j], region, "anticlockwise"]
                        maximum = anticlockwise_value
                    BoardUtility.rotate_region(board, region, "clockwise")
                board[i][j] = 0
        return result