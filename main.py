from source import *

def main():
    board=create_board()
    game_over=False
    turn=0

    print("connect 4 - player vs player [8x8]")
    print_board(board)

    while not game_over:
        player=turn%2
        piece=PLAYER_SYMBOLS[player]

        try:
            col=int(input(f"player {player+1} ({piece}), choose column (1-{COLUMNS}): "))
        except ValueError:
            print("invalid input... please enter a column number...")
            continue

        if not is_valid_column(board, col-1):
            print("column full or out of range... try again!")
            continue

        row=get_next_open_row(board, col-1)
        drop_piece(board, row, col-1, piece)
        print_board(board)

        if win_condition(board, piece):
            print (piece ,"won")
            break

        turn+=1

if __name__=="__main__":
    main()