// ----- config -----
const STATIC = "/static";  // vì app.py dùng static_url_path="/static"

// Map quân cờ -> đường dẫn ảnh
const pieceImg = {
    "P": `${STATIC}/img/wP.svg`, "R": `${STATIC}/img/wR.svg`, "N": `${STATIC}/img/wN.svg`,
    "B": `${STATIC}/img/wB.svg`, "Q": `${STATIC}/img/wQ.svg`, "K": `${STATIC}/img/wK.svg`,
    "p": `${STATIC}/img/bP.svg`, "r": `${STATIC}/img/bR.svg`, "n": `${STATIC}/img/bN.svg`,
    "b": `${STATIC}/img/bB.svg`, "q": `${STATIC}/img/bQ.svg`, "k": `${STATIC}/img/bK.svg`,
};

// Emoji fallback nếu chưa có ảnh
const fallbackEmoji = {
    "P": "♙", "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔",
    "p": "♟︎", "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚"
};

// ----- DOM refs -----
const boardEl = document.getElementById("board");
const msgEl = document.getElementById("msg");

// ----- state -----
const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
let state = { board: [], turn: "white" };
let selected = null;        // "e2"
let legal = [];             // [{to:"e4", capture:true}, ...]
let lastMoveTo = null;      // để chớp nhẹ ô mới di chuyển

// Helpers
function sq(r, c) { return files[c] + (8 - r); }
function rc(s) { return [8 - parseInt(s[1], 10), files.indexOf(s[0])] }

// Load state và vẽ
async function loadState() {
    try {
        const r = await fetch("/state");
        if (!r.ok) throw new Error(`/state ${r.status}`);
        state = await r.json();
        draw();
    } catch (e) {
        msgEl.textContent = "Cannot load /state. Is server running?";
        console.error(e);
    }
}

function draw() {
    boardEl.innerHTML = "";
    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            const div = document.createElement("div");
            div.className = "square " + ((r + c) % 2 ? "dark" : "light");
            const name = sq(r, c);
            div.dataset.square = name;

            if (selected === name) div.classList.add("highlight");
            const mv = legal.find(m => m.to === name);
            if (mv) div.classList.add(mv.capture ? "capture" : "move");
            if (lastMoveTo === name) {
                div.classList.add("just-moved");
                // remove after animation to avoid piling up classes
                setTimeout(() => div.classList.remove("just-moved"), 300);
            }

            const p = state.board[r][c];
            if (p !== ".") {
                const img = document.createElement("img");
                img.className = "piece";
                img.alt = p;
                img.src = pieceImg[p] || "";
                // Fallback emoji nếu ảnh fail hoặc chưa có file
                img.onerror = () => {
                    const e = document.createElement("div");
                    e.className = "emoji";
                    e.textContent = fallbackEmoji[p] || "?";
                    img.replaceWith(e);
                };
                div.appendChild(img);
            }

            div.addEventListener("click", () => onClick(name));
            boardEl.appendChild(div);
        }
    }
}

async function onClick(name) {
    msgEl.textContent = "";
    // Nếu đang chọn và ô click là đích hợp lệ -> đi luôn
    const mv = legal.find(m => m.to === name);
    if (selected && mv) {
        const uci = selected + name;
        const ok = await doMove(uci);
        if (ok) {
            lastMoveTo = name;
            selected = null; legal = [];
            await loadState();
        }
        return;
    }
    // Bỏ chọn nếu bấm lại ô cũ
    if (selected === name) {
        selected = null; legal = [];
        draw();
        return;
    }
    // Chọn quân mới: phải đúng màu đang tới lượt
    const [r, c] = rc(name);
    const p = state.board[r][c];
    if (p === ".") { selected = null; legal = []; draw(); return; }
    const isWhite = (p === p.toUpperCase());
    if ((state.turn === "white" && !isWhite) || (state.turn === "black" && isWhite)) {
        selected = null; legal = []; draw(); return;
    }
    selected = name;
    legal = await fetchMoves(name);
    draw();
}

async function fetchMoves(fromSq) {
    try {
        const r = await fetch(`/moves?from=${fromSq}`);
        const s = await r.json();
        if (!s.ok) { msgEl.textContent = s.error || "move-gen error"; return []; }
        return s.moves || [];
    } catch (e) {
        msgEl.textContent = "Network error (moves)";
        console.error(e);
        return [];
    }
}

async function doMove(uci) {
    try {
        const r = await fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ move: uci })
        });
        const s = await r.json();
        if (!s.ok) {
            msgEl.textContent = s.error || "Illegal move";
            return false;
        }
        return true;
    } catch (e) {
        msgEl.textContent = "Network error (move)";
        console.error(e);
        return false;
    }
}

// Thêm nút undo
const undoBtn = document.getElementById("undo");
if (undoBtn) {
    undoBtn.onclick = async () => {
        msgEl.textContent = "";
        try {
            const r = await fetch("/undo", { method: "POST" });
            const s = await r.json();
            if (!s.ok) { msgEl.textContent = s.error || "Cannot undo"; return; }
            selected = null; legal = []; lastMoveTo = null;
            await loadState();
        } catch {
            msgEl.textContent = "Network error (undo)";
        }
    };
}
loadState();
