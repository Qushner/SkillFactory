def print_board(board):
    print("  0   1   2")
    for i, row in enumerate(board):
        print(f"{i} {'   '.join(row)}")


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def tic_tac_toe():
    board = [['-' for _ in range(3)] for _ in range(3)]
    players = ['Х', 'O']
    current_player = 0

    while True:
        print_board(board)
        print(f"Игрок ({players[current_player]}) ходит")

        row = int(input("Введите номер строки (0-2): "))
        col = int(input("Введите номер столбца (0-2): "))

        if 0 > row or row >= 3 or col >= 3 or 0 > col:
            print("Вы выбрази значение вне поля. Попробуй еще раз")

        elif board[row][col] == '-':
            board[row][col] = players[current_player]

            if check_winner(board, players[current_player]):
                print_board(board)
                print(f"Игрок {players[current_player]} выиграл!")
                break

            current_player = (current_player + 1) % 2
        else:
            print("Эта ячейка занята. Попробуй еще раз")


tic_tac_toe()
