from chess_game import init_board, print_board, make_move, undo_move


def main():
    print(
        "--------------------------\nWelcome to my chess game! In your turn, you can make a move (e2s4), 'undo', or 'end'\nEnjoy!"
    )
    board = init_board()
    print_board(board)
    while True:
        cmd = input("Your turn: ")
        if cmd == "end":
            print("GG, game ended!")
            break
        if cmd == "undo":
            try:
                print_board(undo_move(board))
                continue
            except Exception as e:
                print("Cannot undo:", e, "\n--------------------------")
                continue
        if len(cmd) != 4:
            print("Use format like e2e4.\n--------------------------")
            continue
        try:
            board = make_move(board, cmd)
            print_board(board)
        except Exception as e:
            print(
                "Invalid move:",
                e,
                "\n--------------------------",
            )


if __name__ == "__main__":
    main()
