from random import randint

class Cell:
    def __init__(self):
        self.__is_mine = False
        self.__number = 0
        self.__is_open = False

    def __bool__(self):
        return not self.__is_open

    @property
    def is_mine(self):
        return self.__is_mine

    @is_mine.setter
    def is_mine(self, value):
        if type(value) != bool:
            raise ValueError("недопустимое значение атрибута")
        self.__is_mine = value

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if type(value) != int and value < 0 or value > 8:
            raise ValueError("недопустимое значение атрибута")
        self.__number = value

    @property
    def is_open(self):
        return self.__is_open

    @is_open.setter
    def is_open(self, value):
        if type(value) != bool:
            raise ValueError("недопустимое значение атрибута")
        self.__is_open = value

class GamePole:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __del__(self):
        GamePole._instance = None

    def __init__(self, N, M, total_mines):
        self._n = N
        self._m = M
        self._total_mines = total_mines
        self.__pole_cells = tuple(tuple(Cell() for j in range(M)) for i in range(M))
        self.init_pole()

    @property
    def pole(self):
        return self.__pole_cells

    def init_pole(self):
        for row in self.__pole_cells:
            for x in row:
                x.is_mine = False
                x.is_open = False

        count = 0
        while count < self._total_mines:
            i = randint(0, self._n - 1)
            j = randint(0, self._m - 1)
            if self.__pole_cells[i][j].is_mine is False:
                self.__pole_cells[i][j].is_mine = True
                count += 1

        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)

        for x in range(self._n):
            for y in range(self._m):
                if not self.__pole_cells[x][y].is_mine:
                    mines = sum((self.pole[x + i][y + j].is_mine for i, j in indx if 0 <= x + i < self._n and 0 <= y + j < self._m))
                    self.pole[x][y].number = mines

    def open_cell(self, i, j):
        if not 0 <= i < self._n and not 0 <= j < self._m:
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        self.__pole_cells[i][j].is_open = True

    def show_pole(self):
        for row in self.__pole_cells:
            print(*map(lambda x: "#" if not x.is_open else x.around_mines if not x.mine else "*", row))