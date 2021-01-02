from model import Board
from sapper_game_view import Game
import pygame


class Controller:
    def __init__(self, board_size, number_of_mines):
        self.game_view = Game(self, board_size)
        self.model = Board(board_size, number_of_mines)

    def main(self):
        self.game_view.main()

    def action_on_click(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = self.game_view.point_button(pygame.mouse.get_pos())
            if click is not None:
                field = self.model.get_field(click)
                if event.button == 1:  # 1 is left button
                    if self.model.is_mined(field):
                        self.change_buttons_to_icon(field, 'bomb')
                    else:
                        self.change_buttons_to_numbers(self.model.get_associated_fields(field), field)
                elif event.button == 3:  # 3 is right button
                    self.change_buttons_to_icon(field, 'flag')
        return True

    def change_buttons_to_numbers(self, fields, mother_field):
        if self.game_view.is_button_active((mother_field.row, mother_field.col)):
            color_font = (0, 0, 0)
            for field in fields:
                row_id, col_id = field.row, field.col
                number_of_mined_neighbours = self.model.get_number_of_mined_neighbours(row_id, col_id)
                if number_of_mined_neighbours == 0:
                    number_of_mined_neighbours = ''
                elif number_of_mined_neighbours > 2:
                    color_font = (160, 0, 0)  # red
                elif number_of_mined_neighbours == 2:
                    color_font = (0, 100, 0)  # green
                elif number_of_mined_neighbours == 1:
                    color_font = (0, 0, 120)  # blue
                self.game_view.edit_button((row_id, col_id), color_bg=(128, 128, 128), color_font=color_font,
                                           text=number_of_mined_neighbours)

    def change_buttons_to_icon(self, field, icon):
        row_id, col_id = field.row, field.col
        if icon == 'bomb':
            self.game_view.edit_button((row_id, col_id), color_bg=(250, 0, 0), icon='bomb')
        elif icon == 'flag':
            self.game_view.edit_button((row_id, col_id), icon='flag')


if __name__ == '__main__':
    c = Controller(15, 20)
    c.main()
