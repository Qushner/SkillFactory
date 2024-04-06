
def print_matrix(x):
    print('  0   1   2')
    for counter, value in enumerate(x):
        print(f"{counter} {'   '.join(value)}")
    return


def check_winner(board):
    victories = [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8],
                 [0, 3, 6],
                 [1, 4, 7],
                 [2, 5, 8],
                 [0, 4, 8],
                 [2, 4, 6]]
    win = ""

    new_board = []
    for group in board:
        new_board.extend(group)

    for i in victories:
        if new_board[i[0]] == 'X' and new_board[i[1]] == 'X' and new_board[i[2]] == 'X':
            win = "X"
        if new_board[i[0]] == "O" and new_board[i[1]] == "O" and new_board[i[2]] == "O":
            win = "O"

    return win


def check_board(gamer, board):
    while True:
        index_one, index_two = int(input(f'Игрок {gamer}: Введите позицию ')), int(input(f'Игрок {gamer}: Введите позицию: '))
        try:
            if index_one < 0 or index_two < 0:
                print('Введите целое число!')
                raise False
            if board[index_one][index_two] == '-':
                return index_one, index_two
            else:
                raise False
        except IndexError:
            print("Вы ввели неправильное значение! повторите попытку")
        except ValueError:
            print('Следует вводить числовые значения')
        except TypeError:
            print('Возникла ошибка! Повторите попытку')


def row_tic_tac():
    board = [["-" for _ in range(3)] for _ in range(3)]
    print_matrix(board)
    players = ['X', '0']
    print()
    while True:
        x, y = check_board(players[0], board)[:]
        board[x][y] = 'X'
        print_matrix(board)
        if check_winner(board):
            print(f'Победитель! {check_winner(board)}')
            break

        a, b = check_board(players[1], board)[:]
        board[a][b] = '0'
        print_matrix(board)
        if check_winner(board):
            print(f'Победитель! {check_winner(board)}')
            break


row_tic_tac()
