# utils.py
FILES = "abcdefgh"  # columns a..h


def from_sq(sq: str) -> tuple[int, int]:
    """
    'e2' -> (row, col) in 0..7
    row 0 = rank 8 (trên cùng), row 7 = rank 1 (dưới cùng)
    """
    sq = sq.strip().lower()
    if len(sq) != 2 or sq[0] not in FILES or not sq[1].isdigit():
        raise ValueError(f"Bad square: {sq}")
    col = FILES.index(sq[0])  # 'e' -> 4
    row = 8 - int(sq[1])  # '2' -> 6
    if not (0 <= row < 8 and 0 <= col < 8):
        raise ValueError(f"Out of bounds: {sq}")
    return row, col


def to_sq(row: int, col: int) -> str:
    """(row, col) -> 'e2'"""
    if not (0 <= row < 8 and 0 <= col < 8):
        raise ValueError(f"Out of bounds: {(row, col)}")
    return f"{FILES[col]}{8 - row}"


def parse_uci(uci: str) -> tuple[int, int, int, int]:
    """'e2e4' -> (cr, cc, nr, nc)"""
    uci = uci.strip().lower()
    if len(uci) != 4:
        raise ValueError(f"Bad UCI: {uci}")
    cr, cc = from_sq(uci[:2])
    nr, nc = from_sq(uci[2:])
    return cr, cc, nr, nc


def format_uci(cr: int, cc: int, nr: int, nc: int) -> str:
    """(cr,cc,nr,nc) -> 'e2e4'"""
    return to_sq(cr, cc) + to_sq(nr, nc)
