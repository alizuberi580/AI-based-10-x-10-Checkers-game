from copy import deepcopy
import pygame
import random
from checkers.board import Board

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    all_moves = get_all_moves(position, WHITE if max_player else RED, game)
    random.shuffle(all_moves)  

    if max_player:
        max_eval = float('-inf')
        best_moves = []
        for move in all_moves:
            evaluation = minimax(move, depth-1, False, game, alpha, beta)[0]
            
            if evaluation > max_eval:
                max_eval = evaluation
                best_moves = [move]
            elif evaluation == max_eval:
                best_moves.append(move)
                
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
                
        return max_eval, random.choice(best_moves) if best_moves else None

    else:
        min_eval = float('inf')
        best_moves = []
        for move in all_moves:
            evaluation = minimax(move, depth-1, True, game, alpha, beta)[0]
            
            if evaluation < min_eval:
                min_eval = evaluation
                best_moves = [move]
            elif evaluation == min_eval:
                best_moves.append(move)
                
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
                
        return min_eval, random.choice(best_moves) if best_moves else None

def get_all_moves(board, color, game):
    moves = []
    pieces = list(board.get_all_pieces(color))
    random.shuffle(pieces)  
    
    for piece in pieces:
        valid_moves = board.get_valid_moves(piece)

        move_items = list(valid_moves.items())
        random.shuffle(move_items)
        
        for move, skip in move_items:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board