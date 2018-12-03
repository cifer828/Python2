"""
Monte Carlo Tic-Tac-Toe Player
"""
#################################
# Just for saving. Some modules can be only used in CodeSkulptor.
import random
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# my_board = provided.TTTBoard(3)
# print my_board
# print my_board.get_dim()
# print my_board.square(1, 2)
# print my_board.get_empty_squares()
# my_board.move(1, 0, provided.PLAYERX)
# my_board.move(1, 1, provided.PLAYERX)
# my_board.move(1, 2, provided.PLAYERX)
# print my_board
# print my_board.check_win()


# Add your functions here.
def mc_trial(board, player):
    """
    board: a current board
    player: the next player to move
    This function makes random moves alternating between players till the game is over.
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        move_num = random.randrange(len(empty_squares))
        rand_move = empty_squares [move_num]
        board.move(rand_move[0], rand_move[1], player)
        player = provided.switch_player(player)

# my_board = provided.TTTBoard(3)
# mc_trial(my_board, provided.PLAYERX)
# print my_board

def mc_update_scores(scores, board, player):
    """
    scores: a grid of scores(a list of lists)
    board: a board from a completed game
    player: which player the machine player is
    The function scores the completed board and update the scores grid.
    """
    # Square matching the winner get a positive score.
    # Square mathcing the loser get a positive score.
    # No score for each square in a tied game.
    if board.check_win() == player:
        current_score = SCORE_CURRENT
        other_score = -SCORE_OTHER
    elif board.check_win() == provided.switch_player(player):
        current_score = -SCORE_CURRENT
        other_score = +SCORE_OTHER
    else:
        return
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] += current_score
            elif board.square(row, col) == provided.switch_player(player):
                scores[row][col] += other_score

def get_best_move(board, scores):
    """
    board: a current board.
    scores: a grid of scores.
    The function finds all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.
    """
    empty_squares = board.get_empty_squares()
    max_pos = empty_squares[0]
    for empty in empty_squares:
        if scores[empty[0]][empty[1]] > scores[max_pos[0]][max_pos[1]]:
            max_pos = empty
    max_list = [max_pos]
    for max_nums in empty_squares:
        if scores[max_nums[0]][max_nums[1]] > scores[max_pos[0]][max_pos[1]]:
            max_list.append(max_nums)
    return random.choice(max_list)

def mc_move(board, player, trials):
    """
    :param board: a current board.
    :param player: which player the machine player is
    :param trials: numbers of iteration
    :return: best move (row, col)
    """
    dim = board.get_dim()
    scores = [[0 for _ in range(dim)] for _ in range(dim)]
    for _ in range(trials):
        temp_board = board.clone()
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
#        print temp_board
    return get_best_move(board, scores)

#print get_best_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), [[3, 2, 5], [8, 2, 8], [4, 0, 2]])
#print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERO, NTRIALS)
#print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX, NTRIALS)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
