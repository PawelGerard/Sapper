import pygame


class Button:
    def __init__(self, pos_id, pos):
        self.row_id, self.col_id = pos_id
        self.row_pos, self.col_pos = pos
        self.color_bg = (150, 150, 150)
        self.color_font = (0, 0, 0)
        self.text = ''
        self.icon = ''
        self.active = True

    def __str__(self):
        return 'r: ' + str(self.row_pos) + ' c: ' + str(self.col_pos) + ' r_id: ' + str(self.row_id) + ' c_id: ' \
               + str(self.col_id)


class Game:
    def __init__(self, controller, board_size, number_of_mines):
        self._controller = controller  # way to connect with control module
        self._number_of_mines = number_of_mines
        self._panel_size = 50  # panel = top part of view with mines, emoticon and timer
        self.status = 'running'
        self._board_size, self._buttons = self._create_buttons(board_size, self._panel_size)
        pygame.init()
        self._clock = pygame.time.Clock()
        self._time = 0
        self._start_time = pygame.time.get_ticks()
        self._screen = pygame.display.set_mode((self._board_size, self._board_size + self._panel_size))
        _bomb_icon = pygame.image.load('bomb_icon.png')
        pygame.display.set_caption('Mine Sweeper')
        pygame.display.set_icon(_bomb_icon)

    # main pygame loop
    def main(self):
        run = True
        while run:
            for event in pygame.event.get():
                run = self._controller.action_on_click(event)
            self._screen.fill((0, 0, 0))
            pygame.draw.rect(self._screen, (50, 50, 50), (1, 2, self._board_size - 2, 47))  # border of the panel
            self._draw_rects()
            self._draw_face()
            self._draw_number_of_mines()
            if self.status == 'running':
                self._time = pygame.time.get_ticks()
            self._print_clock()
            pygame.display.update()
            self._clock.tick(20)  # 20 fps

    # format of clock MM:SS
    def _print_clock(self):
        t = int((self._time - self._start_time) / 1000)
        sec_val = t % 60
        sec = str(sec_val) if sec_val >= 10 else '0' + str(sec_val)
        min_val = t // 60
        min = str(min_val) if min_val >= 10 else '0' + str(min_val)
        myfont = pygame.font.SysFont("comicsansms", 26, bold=True)
        label = myfont.render(str(min) + ':' + sec, False, (80, 0, 0))
        self._screen.blit(label, (self._board_size - 82, 5))

    # rects = buttons
    def _draw_rects(self):
        image_bomb = pygame.image.load('bomb.png')
        image_flag = pygame.image.load('flag.png')
        image_wrong_flag = pygame.image.load('false_bomb.png')
        for button in self._buttons:
            pygame.draw.rect(self._screen, button.color_bg, (button.col_pos, button.row_pos, 25, 25))
            if button.icon == 'bomb':
                self._screen.blit(image_bomb, (button.col_pos + 4, button.row_pos + 4))
            elif button.icon == 'flag':
                self._screen.blit(image_flag, (button.col_pos + 4, button.row_pos + 4))
            elif button.icon == 'false_bomb':
                self._screen.blit(image_wrong_flag, (button.col_pos + 4, button.row_pos + 4))
            elif button.text != '':
                myfont = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
                label = myfont.render(str(button.text), True, button.color_font)
                self._screen.blit(label, (button.col_pos + 5, button.row_pos - 3))

    def _draw_face(self):
        img_sad = pygame.image.load('sad.png')
        img_smile = pygame.image.load('smile.png')
        img_happy = pygame.image.load('happy.png')
        pygame.draw.rect(self._screen, (0, 0, 0), ((self._board_size - 40) / 2, 5, 40, 40))  # border
        pygame.draw.rect(self._screen, (30, 30, 30), ((self._board_size - 38) / 2, 6, 38, 38))
        if self.status == 'running':
            self._screen.blit(img_smile, ((self._board_size - 32) / 2, 9))
        elif self.status == 'loss':
            self._screen.blit(img_sad, ((self._board_size - 32) / 2, 9))
        elif self.status == 'win':
            self._screen.blit(img_happy, ((self._board_size - 32) / 2, 9))

    def _draw_number_of_mines(self):
        number = 0
        for button in self._buttons:
            if button.icon == 'flag':
                number += 1
        myfont = pygame.font.SysFont("comicsansms", 26, bold=True)
        label = myfont.render(str(self._number_of_mines - number), False, (80, 0, 0))
        self._screen.blit(label, (10, 5))

    def _create_buttons(self, board_size, panel_size):
        button_list = []
        button_size = 25
        margin = 1
        screen_size = margin + board_size * (button_size + margin)
        for i in range(1, board_size + 1):
            for j in range(1, board_size + 1):
                button_list.append(Button((i, j), (panel_size + margin + (1 + button_size) * (i - 1), margin +
                                                   (1 + button_size) * (j - 1))))
        return screen_size, button_list

    def edit_button(self, position, color_bg=(150, 150, 150), color_font=(0, 0, 0), icon='', text='',
                    reveal_mines=False):
        if self.status == 'running':
            col_id, row_id = position
            for button in self._buttons:
                if button.col_id == col_id and button.row_id == row_id:
                    if button.icon == 'flag' and icon == 'flag':
                        button.icon = ''
                        button.active = True  # to remove flag there is need to click right button again
                        return True  # if button changed
                    elif button.active:
                        button.color_bg = color_bg
                        button.color_font = color_font
                        button.icon = icon
                        button.text = text
                        button.active = False
                        return True  # if button changed
                    elif reveal_mines:
                        button.icon = icon
        return False  # if button not changed

    def is_button_active(self, position):
        col_id, row_id = position
        for button in self._buttons:
            if button.col_id == col_id and button.row_id == row_id:
                return button.active

    def point_button(self, position):
        x, y = position
        if 5 < y < 45 and (self._board_size - 40) / 2 < x < (self._board_size - 40) / 2 + 40:
            return 0, 0  # smile button
        for button in self._buttons:
            if button.row_pos < y < button.row_pos + 25 and button.col_pos < x < button.col_pos + 25:  # 25 is button size
                return button.col_id, button.row_id

    def reset_game(self):
        self.status = 'running'
        self._start_time = pygame.time.get_ticks()
        for button in self._buttons:
            button.color_bg = (150, 150, 150)
            button.color_font = (0, 0, 0)
            button.text = ''
            button.icon = ''
            button.active = True

    def check_win(self):
        revealed_fields = 0
        all_fields = len(self._buttons)
        for button in self._buttons:
            if not button.active and button.icon != 'flag':
                revealed_fields += 1
        if all_fields == revealed_fields + self._number_of_mines:
            return True
        return False

    def change_icon_of_wrong_guesses(self):
        for button in self._buttons:
            if button.icon == 'flag':
                button.icon = 'false_bomb'

    def change_mines_to_flags(self):
        for button in self._buttons:
            if button.active:
                button.icon = 'flag'

    def print_board(self):
        for button in self._buttons:
            print(' r: ' + str(button.row_id) + ' c: ' + str(button.col_id) + ' a: ' + str(button.active))
