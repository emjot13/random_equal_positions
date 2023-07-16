import chess
import chess.svg
import random
import chess.engine

POSITIONS_FILE = "./random_equal_positions.txt"


def generate_random_boards(number_of_boards: int, save_svg: bool):
    for board_number in range(number_of_boards):
        try:
            board = chess.Board()
            play_random_moves(board, 40)
            if save_svg:
                save_board_to_svg(board, board_number)
            equalize_position(board, 50)
            write_fen_notation(board)
            if save_svg:
                save_board_to_svg(board, board_number, equalized=True)
        except:
            pass

def write_fen_notation(board):
    with open(POSITIONS_FILE, "a") as f:
        f.write(f"{board.fen()}\n")


def play_random_moves(board: chess.Board, number_of_moves: int):
    for _ in range(number_of_moves):
        legal_moves = list(board.legal_moves)
        move = random.choice(legal_moves)
        board.push(move)


def save_board_to_svg(board, board_number, equalized=False):
    file_name = "./chess-positions-svg/"
    file_name += f'chess_board_number_{board_number}.svg' if not equalized else f'chess_board_number_{board_number}_equalized.svg'
    with open(file_name, 'w') as f:
        f.write(chess.svg.board(board=board))



def equalize_position(board, centipawn_margin):
    current_eval, moves_eval = get_evaluation(board, centipawn_margin)
    while moves_eval:
        closest_to_zero = min(moves_eval, key=lambda x: abs(moves_eval[x]))
        board.push(closest_to_zero)
        current_eval, moves_eval = get_evaluation(board, centipawn_margin)
    print(current_eval)


def get_evaluation(board, centipawn_margin):
    with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:
        # Get the evaluation of the final board position
        info = engine.analyse(board, chess.engine.Limit(time=4))
        evaluation = info["score"].relative.score()
        if abs(evaluation) < centipawn_margin:
            return evaluation, None

        all_evaluations = {}
        for move in board.legal_moves:
            info = engine.analyse(board, chess.engine.Limit(time=0.3), root_moves=[move])
            all_evaluations[move] = info["score"].relative.score()

    return evaluation, all_evaluations


if __name__ == "__main__":
    generate_random_boards(300, False)
