import copy
import random

# Constants for the Minimax scoring system
WINDOW_LENGTH = 4
EMPTY = ' '
AI_PIECE = 'O'
PLAYER_PIECE = 'X'

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score

def score_position(board, piece):
    score = 0
    center_array = board[len(board)//2]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score Horizontal
    for r in range(6):
        row_array = [board[c][r] for c in range(7)]
        for c in range(7 - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(7):
        col_array = board[c]
        for r in range(6 - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Diagonals Up
    for c in range(7 - 3):
        for r in range(6 - 3):
            window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score Diagonals Down
    for c in range(7 - 3):
        for r in range(3, 6):
            window = [board[c+i][r-i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def minimax(board, depth, alpha, beta, maximizingPlayer, gl):
    valid_locations = gl.available_moves(board)
    is_terminal = gl.game_is_over(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if gl.has_won(board, AI_PIECE):
                return (None, 10000000)
            elif gl.has_won(board, PLAYER_PIECE):
                return (None, -10000000)
            else: 
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            gl.select_space(b_copy, col, AI_PIECE)
        
            # Alpha-Beta Pruning 
            new_score = minimax(b_copy, depth-1, alpha, beta, False, gl)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta: 
                break
        return column, value

    else: # Minimizing player (The Human)
        value = float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            gl.select_space(b_copy, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True, gl)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta: 
                break
        return column, value

def get_ai_move(board, gl):
    col, score = minimax(board, 4, -float('inf'), float('inf'), True, gl)
    return col