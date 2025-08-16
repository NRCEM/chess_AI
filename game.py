from rules import is_valid_move


# Initialize the 8x8 chess board
def init_board():
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],  # black pieces
        ["p", "p", "p", "p", "p", "p", "p", "p"],  # black pawns
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],  # white pawns
        ["R", "N", "B", "Q", "K", "B", "N", "R"],  # white pieces
    ]
    return board


move_history = []


# Print the board
def print_board(board):
    print("--------------------------")
    for row in board:
        print(" ".join(row))
    print("--------------------------")


# Covert string, eg: e2e4
def parse_move(move):
    cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cur_col = cols[move[0]]
    cur_row = 8 - int(move[1])
    next_col = cols[move[2]]
    next_row = 8 - int(move[3])
    return (cur_row, cur_col, next_row, next_col)


# Execute the move
def make_move(board, move):
    cr, cc, nr, nc = parse_move(move)  # cur_row, cur_col, next_row, next_col
    if not is_valid_move(board, cr, cc, nr, nc):
        raise ValueError("Invalid move")

    piece = board[cr][cc]
    captured = board[nr][nc]

    board[nr][nc] = piece
    board[cr][cc] = "."

    move_history.append(
        {"cr": cr, "cc": cc, "nr": nr, "nc": nc, "piece": piece, "captured": captured}
    )
    return board


def undo_move(board):
    if not move_history:
        raise ValueError("No moves to undo")
    rec = move_history.pop()
    board[rec["cr"]][rec["cc"]] = rec["piece"]
    board[rec["nr"]][rec["nc"]] = rec["captured"]
    return board
