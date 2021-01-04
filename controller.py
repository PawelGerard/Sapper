"""
Controller connects two modules: view and model
"""

from model import Board
from sapper_game_view import Game
import pygame


class Controller:
    def __init__(self, board_size, number_of_mines):
        self._game_view = Game(self, board_size, number_of_mines)
        self._model = Board(board_size, number_of_mines)

    def main(self):
        self._game_view.main()

    def action_on_click(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = self._game_view.point_button(pygame.mouse.get_pos())
            if click == (0, 0):  # emoticon clicked
                self._game_view.reset_game()
                self._model.reset_model()
            elif click is not None:
                field = self._model.get_field(click)
                if event.button == 1:  # 1 is left button
                    if self._model.is_mined(field):
                        self.change_buttons_to_icon(field, 'bomb')
                    else:
                        self.change_buttons_to_numbers(self._model.get_associated_fields(field), field)
                elif event.button == 3:  # 3 is right button
                    self.change_buttons_to_icon(field, 'flag')
        return True

    def change_buttons_to_numbers(self, fields, mother_field):
        if self._game_view.is_button_active((mother_field.row, mother_field.col)):
            color_font = (0, 0, 0)
            for field in fields:
                row_id, col_id = field.row, field.col
                number_of_mined_neighbours = self._model.get_number_of_mined_neighbours(row_id, col_id)
                if number_of_mined_neighbours == 0:
                    number_of_mined_neighbours = ''
                elif number_of_mined_neighbours > 2:
                    color_font = (160, 0, 0)  # red
                elif number_of_mined_neighbours == 2:
                    color_font = (0, 100, 0)  # green
                elif number_of_mined_neighbours == 1:
                    color_font = (0, 0, 120)  # blue
                self._game_view.edit_button((row_id, col_id), color_bg=(128, 128, 128), color_font=color_font,
                                            text=number_of_mined_neighbours)
                if self._game_view.check_win():
                    self._game_view.status = 'win'
                    self._game_view.change_mines_to_flags()

    def change_buttons_to_icon(self, field, icon):
        row_id, col_id = field.row, field.col
        if icon == 'bomb':
            if self._game_view.edit_button((row_id, col_id), color_bg=(250, 0, 0), icon='bomb'):
                mined_fields = self._model.get_all_mined_fields()
                for mine in mined_fields:
                    if mine is not field:
                        row_id, col_id = mine.row, mine.col
                        self._game_view.edit_button((row_id, col_id), icon='bomb', reveal_mines=True)
                self._game_view.change_icon_of_wrong_guesses()
                if self._game_view.status != 'win':
                    self._game_view.status = 'loss'
        elif icon == 'flag':
            self._game_view.edit_button((row_id, col_id), icon='flag')


if __name__ == '__main__':
    c = Controller(15, 20)  # Board size and number of mines can be change here. Board is always a square
    c.main()
