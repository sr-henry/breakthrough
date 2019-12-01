import breakthrough
import random
from math import inf
from sklearn.utils import shuffle
from sklearn.linear_model import SGDRegressor
from joblib import dump, load
from heuristics import *
from copy import deepcopy

def random_player(board, player_type):
    legal_moves = board.possible_moves(player_type)
    if legal_moves:
            idx = random.randint(0, len(legal_moves) - 1)
            return legal_moves[idx]
    else:
        return False

def features(board):
    f1 = fov_evaluation(board)
    f2 = piece_value_evaluation(board)
    f3 = mobility_evaluation(board)
    f4 = number_of_pieces(board)
    return tuple([f1, f2, f3, f4])


def generate_episode(player1, player2, epsilon, model):

    board = breakthrough.Board()

    board.reset()

    episode = [features(board)]

    while True:
        move = player1(board, breakthrough.WHITE, epsilon, model)

        if not board.perform_move(move):
            return episode, -1

        episode.append(features(board))

        if move[1][0] == board.lines:
            return episode, 1

        move = player2(board, breakthrough.BLACK)

        if not board.perform_move(move):
            return episode, 1

        episode.append(features(board))

        if move[1][0] == 1:
            return episode, -1


def exploration_exploitation(board, player_type, epsilon, model):
    legal_moves = board.possible_moves(player_type)

    if random.random() < epsilon:
        if legal_moves:
            idx = random.randint(0, len(legal_moves) - 1)
            return legal_moves[idx]
        else:
            return False    
    else:
        best_move  = None
        best_score = -inf if player_type else inf

        for move in legal_moves:
            next_state = deepcopy(board)
            next_state.perform_move(move)
            next_state_value = model.predict([features(board)])[0]
            if next_state_value > best_score :
                best_score = next_state_value
                best_move  = move

        if best_move == None :
            if legal_moves:
                idx = random.randint(0, len(legal_moves) - 1)
                return legal_moves[idx]
            else:
                return False

        return best_move


def update_state_values_monte_carlo(state_values, state_order, rewards, gamma = .95, alpha = .1):    
    next_state = state_order[-1]
    G = 0

    for state in reversed(state_order[:-1]):
        G = gamma*G + rewards.get(next_state, 0) # testar outros valores :: trocar por func
        state_values[state] = state_values.get(state, 0) + alpha*(G - state_values.get(state, 0))
        next_state = state
    
    return state_values


def learn_breakthrough(num_iterations, max_epsilon):
    model = SGDRegressor(fit_intercept=True, warm_start=True)
    
    model.fit([(0, 0, 0, 0)], [0])

    for i in range(num_iterations):
        state_values = {}
        rewards = {}

        epsilon = max_epsilon*(num_iterations - i)/num_iterations

        state_order, reward = generate_episode(exploration_exploitation, random_player, epsilon, model)

        rewards[state_order[-1]] = reward
        state_values[state_order[-1]] = reward

        state_values = update_state_values_monte_carlo(state_values, state_order, rewards)

        all_states = list(state_values.keys())
        all_values = list(state_values.values())

        training_data, target_data = shuffle(all_states, all_values)

        model.partial_fit(training_data, target_data)

    return model


final_model = learn_breakthrough(5000, .5)

dump(final_model, 'final_model.joblib') 
