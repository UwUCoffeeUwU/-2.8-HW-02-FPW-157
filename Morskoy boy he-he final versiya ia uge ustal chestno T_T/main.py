import random


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.is_alive = True


class Board:
    def __init__(self, ships):
        self.ships = ships
        self.board = [['O' for _ in range(6)] for _ in range(6)]
        self.populate_board()

    def populate_board(self):
        for ship in self.ships:
            for coord in ship.coordinates:
                self.board[coord.x][coord.y] = '■'

    def display(self, hide_ships=False):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if hide_ships and self.board[i][j] == '■':
                    print('| O', end=' ')
                else:
                    print(f'| {self.board[i][j]}', end=' ')
            print('|')

    def receive_attack(self, coord):
        if self.board[coord.x][coord.y] == 'O':
            self.board[coord.x][coord.y] = 'T'
            return False
        elif self.board[coord.x][coord.y] == '■':
            self.board[coord.x][coord.y] = 'X'
            for ship in self.ships:
                for ship_coord in ship.coordinates:
                    if ship_coord.x == coord.x and ship_coord.y == coord.y:
                        ship.is_alive = False
                        print("Корабль уничтожен!")
                        if all(not s.is_alive for s in self.ships):
                            return 'game_over'
                        else:
                            return True
            return True
        else:
            raise ValueError("Некорректные координаты выстрела!")


def player_turn(board):
    while True:
        try:
            x, y = map(int, input("Введите координаты для выстрела (например, 1 2): ").split())
            if 0 <= x <= 5 and 0 <= y <= 5:
                coord = Coordinate(x, y)
                if board.board[x][y] != 'X' and board.board[x][y] != 'T':
                    return coord
                else:
                    print("Вы уже стреляли в эту клетку. Пожалуйста, выберите другую.")
            else:
                print("Некорректные координаты. Пожалуйста, попробуйте еще раз.")
        except ValueError:
            print("Некорректные координаты. Пожалуйста, попробуйте еще раз.")


def computer_turn(board):
    while True:
        x, y = random.randint(0, 5), random.randint(0, 5)
        coord = Coordinate(x, y)
        if board.board[x][y] != 'X' and board.board[x][y] != 'T':
            return coord


def check_game_over(player_ships, computer_ships):
    if all(not s.is_alive for s in computer_ships if s.is_alive):
        print("Computer ships destroyed. Player wins.")
        return 'player'
    elif all(not s.is_alive for s in player_ships if s.is_alive):
        print("Player ships destroyed. Computer wins.")
        return 'computer'
    else:
        return None


def play_game():
    player_ships = [
        Ship([Coordinate(0, 0), Coordinate(0, 1), Coordinate(0, 2)]),
        Ship([Coordinate(1, 3), Coordinate(1, 4)]),
        Ship([Coordinate(3, 2)]),
        Ship([Coordinate(3, 4), Coordinate(4, 4)]),
        Ship([Coordinate(5, 0)]),
        Ship([Coordinate(5, 2)]),
        Ship([Coordinate(3, 0)])
    ]
    computer_ships = [
        Ship([Coordinate(0, 0), Coordinate(1, 0), Coordinate(2, 0)]),
        Ship([Coordinate(0, 2), Coordinate(1, 2)]),
        Ship([Coordinate(2, 3), Coordinate(2, 4)]),
        Ship([Coordinate(4, 4)]),
        Ship([Coordinate(0, 5)]),
        Ship([Coordinate(4, 0)]),
        Ship([Coordinate(5, 2)])
    ]

    player_board = Board(player_ships)
    computer_board = Board(computer_ships)

    while True:
        print("\n--- Новый ход ---")
        print("Ваша доска:")
        player_board.display()
        print("\nДоска компьютера:")
        computer_board.display()

        print("\nВаш ход:")
        player_coord = player_turn(computer_board)
        result = computer_board.receive_attack(player_coord)
        if result == 'game_over':
            print("Вы победили!")
            break

        game_result = check_game_over(player_ships, computer_ships)
        if game_result == 'player':
            print("Вы победили!")
            break
        elif game_result == 'computer':
            print("Компьютер победил!")
            break

        print("\nХод компьютера:")
        computer_coord = computer_turn(player_board)
        result = player_board.receive_attack(computer_coord)
        if result == 'game_over':
            print("Компьютер победил!")
            break

        game_result = check_game_over(player_ships, computer_ships)
        if game_result == 'player':
            print("Вы победили!")
            break
        elif game_result == 'computer':
            print("Компьютер победил!")
            break


play_game()
