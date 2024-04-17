# Итоговое_задание_9.5.1_(HW-02)."Морской_бой"//PDEVPRO-5_Кушнер_С.В.

from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы выстрелили за пределами игрового поля! Повторите попытку!"


class BoardUsedDotException(BoardException):
    def __str__(self):
        return "Выстрел в использованную клетку! Повторите попытку!"


class BoardErrorShipException(BoardException):
    pass


class Ship:
    def __init__(self, nose_dot, l, direction):
        self.nose_dot = nose_dot  # точка носа
        self.l = l  # длина корабля
        self.direction = direction  # расположение (вертикальное/горизонтальное)
        self.hit_points = l  # неподбитых точек (количество)

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.nose_dot.x
            cur_y = self.nose_dot.y

            if self.direction == 0:
                cur_x += i
            elif self.direction == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shot_in_ship(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size_board=6):
        self.size_board = size_board
        self.hid = hid

        self.count = 0  # кол-во пораженных кораблей

        self.board = [['O'] * size_board for _ in range(size_board)]  # сетка

        self.busy = []  # занятые точки (корабли или точки выстрела)
        self.ships = []  # список кораблей доски

    def add_ship(self, ship):

        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardErrorShipException()
        for dot in ship.dots:
            self.board[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dot_x, dot_y in near:
                cur = Dot(dot.x + dot_x, dot.y + dot_y)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.board[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        print_board = ""
        print_board += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.board):
            print_board += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            print_board = print_board.replace("■", "O")
        return print_board

    def out(self, dot):
        return not ((0 <= dot.x < self.size_board) and (0 <= dot.y < self.size_board))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedDotException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.hit_points -= 1
                self.board[dot.x][dot.y] = "X"
                if ship.hit_points == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль ранен! Ходи еще!")
                    return True

        self.board[dot.x][dot.y] = "."
        print("Мимо")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, game_board, enemy_board):
        self.game_board = game_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f'AI ходит: {dot.x + 1} {dot.y + 1}')
        return dot


class User(Player):
    def ask(self):
        while True:
            cords = input("Вы ходите: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введи числа")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size_board=6):
        self.size_board = size_board
        gamer = self.random_board()
        bot = self.random_board()
        bot.hid = True

        self.ai = AI(bot, gamer)
        self.player = User(gamer, bot)

    def random_board(self):
        game_board = None
        while game_board is None:
            game_board = self.random_place()
        return game_board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        game_board = Board(size_board=self.size_board)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size_board), randint(0, self.size_board)), l, randint(0, 1))
                try:
                    game_board.add_ship(ship)
                    break
                except BoardErrorShipException:
                    pass

        game_board.begin()
        return game_board

    @staticmethod
    def greet():
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Формат ввода координат: X - номер строки, Y - номер столбца (например, 3 5)")

    def loop(self):
        num = 0
        while True:
            print()
            print("Поле игрока: ")
            print(self.player.game_board)
            print()
            print("Поле компьютера: ")
            print(self.ai.game_board)
            print()
            if num % 2 == 0:
                print("Игрок ходит!")
                repeat = self.player.move()
            else:
                print("Компьютер ходит!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.game_board.count == 7:
                print()
                print("Доска пользователя:")
                print(self.player.game_board)
                print()
                print("Доска компьютера:")
                print(self.ai.game_board)
                print()
                print("Пользователь выиграл!")
                break

            if self.player.game_board.count == 7:
                print()
                print("Доска пользователя:")
                print(self.player.game_board)
                print()
                print("Доска компьютера:")
                print(self.ai.game_board)
                print()
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
