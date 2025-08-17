# ============
# Basic utils
# ============

white_pieces = {"P", "R", "N", "B", "Q", "K"}
black_pieces = {"p", "r", "n", "b", "q", "k"}


def in_bounds(r, c):
    """True if (r, c) is on the 8x8 board."""
    return 0 <= r < 8 and 0 <= c < 8


def same_color(a, b):
    """True if a and b are both non-empty and belong to the same side."""
    if a == "." or b == ".":
        return False
    return (a in white_pieces and b in white_pieces) or (
        a in black_pieces and b in black_pieces
    )


def is_opponent(a, b):
    """True if b is a non-empty opponent of a."""
    if a == "." or b == ".":
        return False
    return (a in white_pieces and b in black_pieces) or (
        a in black_pieces and b in white_pieces
    )


def is_path_clear(board, cr, cc, nr, nc):
    """For sliding pieces (rook/bishop/queen):"""
    dr = nr - cr
    dc = nc - cc
    step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
    step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

    r, c = cr + step_r, cc + step_c
    while (r, c) != (nr, nc):
        if board[r][c] != ".":
            return False
        r += step_r
        c += step_c
    return True


# =========================
# Piece-specific validators
# =========================
def is_valid_pawn(board, cr, cc, nr, nc):
    """Basic pawn rules (no en passant, no promotion)"""
    piece = board[cr][cc]
    target = board[nr][nc]

    # Cannot capture own piece
    if same_color(piece, target):
        return False

    if piece in white_pieces:
        # single step forward
        if nr == cr - 1 and nc == cc and target == ".":
            return True
        # double step from starting rank
        if cr == 6 and nr == 4 and nc == cc and board[5][cc] == "." and target == ".":
            return True
        # diagonal capture
        if nr == cr - 1 and abs(nc - cc) == 1 and target in black_pieces:
            return True
        return False

    if piece in black_pieces:
        # single step forward
        if nr == cr + 1 and nc == cc and target == ".":
            return True
        # double step from starting rank
        if cr == 1 and nr == 3 and nc == cc and board[2][cc] == "." and target == ".":
            return True
        # diagonal capture
        if nr == cr + 1 and abs(nc - cc) == 1 and target in white_pieces:
            return True
        return False

    return False


def is_valid_knight(board, cr, cc, nr, nc):
    piece = board[cr][cc]
    target = board[nr][nc]

    # Cannot capture own piece
    if same_color(piece, target):
        return False
    dr, dc = abs(nr - cr), abs(nc - cc)
    return (dr, dc) in {(2, 1), (1, 2)}


def is_valid_rook(board, cr, cc, nr, nc):
    piece = board[cr][cc]
    target = board[nr][nc]

    # Cannot capture own piece
    if same_color(piece, target):
        return False
    if cr != nr and cc != nc:
        return False
    return is_path_clear(board, cr, cc, nr, nc)


def is_valid_bishop(board, cr, cc, nr, nc):
    piece = board[cr][cc]
    target = board[nr][nc]

    # Cannot capture own piece
    if same_color(piece, target):
        return False
    if abs(nr - cr) != abs(nc - cc):
        return False
    return is_path_clear(board, cr, cc, nr, nc)


def is_valid_queen(board, cr, cc, nr, nc):
    piece = board[cr][cc]
    target = board[nr][nc]

    # Cannot capture own piece
    if same_color(piece, target):
        return False
    straight = cr == nr or cc == nc
    diagonal = abs(nr - cr) == abs(nc - cc)
    if not (straight or diagonal):
        return False
    return is_path_clear(board, cr, cc, nr, nc)


def is_valid_king(board, cr, cc, nr, nc):
    """Basic King rules (no castling)."""
    piece = board[cr][cc]
    target = board[nr][nc]

    # Cannot capture own piece
    if same_color(piece, target):
        return False
    return max(abs(nr - cr), abs(nc - cc)) == 1


# =========================
# Dispatcher and wrapper
# =========================
def is_valid_move(board, cr, cc, nr, nc, side):
    """Dispatch validator based on the piece at (cr, cc)."""
    if not (in_bounds(cr, cc) and in_bounds(nr, nc)):
        return False
    piece = board[cr][cc]
    if piece == ".":
        return False  # no piece to move

    validators = {
        "P": is_valid_pawn,
        "p": is_valid_pawn,
        "N": is_valid_knight,
        "n": is_valid_knight,
        "R": is_valid_rook,
        "r": is_valid_rook,
        "B": is_valid_bishop,
        "b": is_valid_bishop,
        "Q": is_valid_queen,
        "q": is_valid_queen,
        "K": is_valid_king,
        "k": is_valid_king,
    }
    if (piece in white_pieces and side == "white") or (
        piece in black_pieces and side == "black"
    ):

        if piece in validators:
            return validators[piece](board, cr, cc, nr, nc)
        else:
            return False
