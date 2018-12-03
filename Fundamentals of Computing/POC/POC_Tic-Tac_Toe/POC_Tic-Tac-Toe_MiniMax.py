"""
Mini-max Tic-Tac-Toe Player
"""

# import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
# import codeskulptor
# codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    move_list = []
    score = SCORES[player] #make the minimax to always max
    #try every empty square move
    for empty in board.get_empty_squares():
        temp_board = board.clone()
        temp_board.move(empty[0], empty[1], player)
        #base case
        if temp_board.check_win():
            return SCORES[temp_board.check_win()], empty
        #recursive case
        move = mm_move(temp_board, provided.switch_player(player))
        #if find a winning score (+1 for X or -1 for O), return the move because we can't do better
        if move[0] == score:
            return move[0], empty
        move_list.append((move[0], empty))
    #return the move with max score
    for moving in move_list:
        if moving[0] == 0:
            return moving[0], moving[1]
    return move_list[0][0], move_list[0][1]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.EMPTY, provided.PLAYERO, provided.PLAYERX]]), provided.PLAYERX)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
