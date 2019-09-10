import random
import copy
import numpy as np

class Player(object):
    def __init__(self, player = 1):
        self.states = {}
        self.state_order = []
        self.learning_rate = 0.5
        self.decay = 0.01
        self.discount_factor = 0.01
        self.exploration_rate = 0.9
        self.player = player


    def set_state(self, board, move):
        state_key = board.serialize_board()
        self.state_order.append((state_key, move))


    def select_move(self, board):
        if self.player == 1:
            possible_moves = board.white_possible_moves()
        else:
            possible_moves= board.black_possible_moves()
        
        if random.random() <= self.exploration_rate:
            idx = random.randint(0, abs(len(possible_moves)-1))
            best_move = possible_moves[idx]
        
        else:
            best_score = -99999

            for move in possible_moves:
                nboard = copy.deepcopy(board)

                if self.player == 1:
                    nboard.perform_white_move(move)
                else:
                    nboard.perform_black_move(move)
                
                nboard_key = nboard.serialize_board()
                if nboard_key not in self.states.keys():
                    current_score = 0
                else:
                    current_score = self.states[nboard_key]
                
                if current_score > best_score:
                    best_score = current_score
                    best_move = move
                
        return best_move

    def select_move_n(self, board):
        state_key = board.serialize_board()
        if np.random.random() < self.exploration_rate or state_key not in self.states:
            move = self.explore_board(board)
        else:
            move = self.exploit_board(state_key, board)
        self.set_state(board, move)
        return move


    def learn_by_temporal_difference(self, reward, new_state_key, state_key):
        old_state = self.states.get(state_key, np.zeros((8,8)))
        print(old_state)
        self.exploration_rate = max(self.exploration_rate - self.decay, 0.3)
        return self.learning_rate * ((reward * self.states[new_state_key]) - old_state)


    def on_reward(self, reward):
        if len(self.state_order) == 0:
            return None

        new_state_key, new_action = self.state_order.pop()

        self.states[new_state_key] = np.zeros((8,8))

        self.states[new_state_key].itemset(new_action, reward)

        while self.state_order:
            state_key, action = self.state_order.pop()

            reward *= self.discount_factor

            if state_key in self.states:
                reward += self.learn_by_temporal_difference(reward, new_state_key, state_key).item(new_action)
                self.states[state_key].itemset(action, reward)
            else:
                self.states[state_key] = np.zeros((8,8))
                reward = self.learn_by_temporal_difference(reward, new_state_key, state_key).item(new_action)
                self.states[state_key].itemset(action, reward)
            new_state_key = state_key
            new_action = action


    def explore_board(self, board, depth = 5):
        if self.player == 1:
            possible_moves = board.white_possible_moves()
        else:
            possible_moves = board.black_possible_moves()

        nboard = copy.deepcopy(board)

        selected_move = possible_moves[np.random.choice(len(possible_moves))]

        if self.player == 1:
            nboard.perform_white_move(selected_move)
        else:
            nboard.perform_black_move(selected_move)
        
        state_key = nboard.serialize_board()

        if state_key not in self.states or depth == 0:
            return selected_move

        return self.explore_board(board, depth - 1)


    def exploit_board(self, state_key, board):
        state_values = self.states[state_key]

        if self.player == 1:
            possible_moves = board.white_possible_moves()
        else:
            possible_moves = board.black_possible_moves()
        
        best_scores = {}
        for idx, score in np.ndenumerate(state_values):
            pos = (abs(idx[0] - 8), idx[1]+1)
            if pos in possible_moves:
                best_scores[str(pos)] = score

        best_value_indices = [key
            for m in [max(best_scores.values())]
                for key, val in best_scores.items()
                    if val == m
        ]

        select_index = np.random.choice(len(best_value_indices))
        return best_value_indices[select_index]


    def reset_player(self):
        self.state_order.clear()

    def get_serious(self):
        self.exploration_rate = 0
