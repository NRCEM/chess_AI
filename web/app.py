from flask import Flask, request, jsonify
import os, sys, traceback

# Cho phép import game.py / rules.py / utils.py ở thư mục gốc
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import game, rules

app = Flask(__name__, static_folder="static", static_url_path="/static")

FILES = "abcdefgh"


def to_sq(r, c):
    return f"{FILES[c]}{8 - r}"


def from_sq(s):
    cols = {ch: i for i, ch in enumerate(FILES)}
    return 8 - int(s[1]), cols[s[0].lower()]


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/state")
def state():
    return jsonify({"board": game.board, "turn": game.whose_turn()})


@app.get("/moves")
def moves():
    sq = request.args.get("from", "")
    if len(sq) != 2:
        return jsonify({"ok": False, "error": "from=? like e2"}), 400
    cr, cc = from_sq(sq)
    side = game.whose_turn()
    legal = []
    for nr in range(8):
        for nc in range(8):
            ok = rules.is_valid_move(game.board, cr, cc, nr, nc, side)
            if ok:
                capture = game.board[nr][nc] != "."
                legal.append({"to": to_sq(nr, nc), "capture": capture})
    return jsonify({"ok": True, "moves": legal})


@app.post("/move")
def move():
    data = request.get_json(force=True, silent=True) or {}
    mv = data.get("move", "")
    if len(mv) != 4:
        return jsonify({"ok": False, "error": "move must be UCI like e2e4"}), 400
    try:
        game.make_move(game.board, mv)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.post("/undo")
def undo():
    try:
        game.undo_move(game.board)  # gọi engine
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


if __name__ == "__main__":
    # chạy local
    app.run(host="0.0.0.0", port=5000, debug=True)
