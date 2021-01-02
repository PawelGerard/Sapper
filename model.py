"""
class Field represent each square on Board
class Board create particular number of Fields and theirs variables (row, column, is_bomb, number_of_mined_neighbours)
"""

from __future__ import annotations
import random


class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isbomb = False
        self.mined_neighbours = 0
        self.fields_to_reveal = set()

    def is_neighbour(self, other: Field) -> bool:
        if (self.row == other.row - 1 or self.row == other.row or self.row == other.row + 1) \
                and (self.col == other.col - 1 or self.col == other.col or self.col == other.col + 1) \
                and (self is not other):
            return True
        return False

    def __str__(self):
        return 'r: ' + str(self.row) + ' c: ' + str(self.col) + ' mined: ' + str(
            self.isbomb) + ' mined_neighbours: ' + str(self.mined_neighbours)


class Board:
    def __init__(self, board_size, number_of_mines):
        self._fields = []
        self._mined_fields = []
        self._board_size = board_size
        self._number_of_mines = number_of_mines
        self._create_fields()
        self._mine_fields()
        self._define_neighborhood()

    def _create_fields(self):
        for i in range(1, self._board_size + 1):
            for j in range(1, self._board_size + 1):
                self._fields.append(Field(i, j))

    def _mine_fields(self):
        self._mined_fields = random.sample(self._fields, self._number_of_mines)
        for field in self._mined_fields:
            field.isbomb = True

    def _define_neighborhood(self):
        for field in self._fields:
            for neighbour in self._fields:
                if field.is_neighbour(neighbour) and neighbour in self._mined_fields:
                    field.mined_neighbours += 1

    # recursion used to define range which should be revealed
    # mother_field = clicked_field, given_field_list = neighbours, neighbours of neighbours... etc.
    # if there is no more valid neighbours fields_to_reveal will be defined
    def define_what_to_reveal(self, mother_field, given_field_list):
        result = set()
        for field in given_field_list:
            result.add(field)
            for neighbour in self._fields:
                if field.is_neighbour(neighbour) and (field.mined_neighbours == 0) and (not field.isbomb):
                    result.add(neighbour)
        if len(result) != len(given_field_list):
            self.define_what_to_reveal(mother_field, result)
        else:
            mother_field.fields_to_reveal = result

    def _print_board(self):
        for field in self._fields:
            print(field)

    def get_field(self, click):
        row, col = click
        for field in self._fields:
            if field.row == row and field.col == col:
                return field

    def get_number_of_mined_neighbours(self, row, col):
        for field in self._fields:
            if field.row == row and field.col == col:
                return field.mined_neighbours

    def is_mined(self, field):
        return field.isbomb

    def get_associated_fields(self, field):
        self.define_what_to_reveal(field, [field])
        return field.fields_to_reveal
