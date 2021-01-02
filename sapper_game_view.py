import pygame


class Button:
    def __init__(self, pos_id, pos, color_bg, color_font):
        self.row_id, self.col_id = pos_id
        self.row_pos, self.col_pos = pos
        self.color_bg = color_bg
        self.color_font = color_font
        self.text = ''
        self.icon = False

    def __str__(self):
        return 'r: ' + str(self.row_pos) + ' c: ' + str(self.col_pos) + ' r_id: ' + str(self.row_id) + ' c_id: '\
               + str(self.col_id)


class Game:
    def __init__(self, controller, board_size):
        self._controller = controller
        self._panel_size = 50
        self._board_size, self._buttons = self._create_buttons(board_size, self._panel_size)
        pygame.init()
        self._clock = pygame.time.Clock()
        self._start_time = pygame.time.get_ticks()
        self._screen = pygame.display.set_mode((self._board_size, self._board_size + self._panel_size))
        _bomb_icon = pygame.image.load('bomb_icon.png')
        pygame.display.set_caption('Mine Sweeper')
        pygame.display.set_icon(_bomb_icon)

    def main(self):
        run = True
        while run:
            for event in pygame.event.get():
                run = self._controller.action_on_click(event)
            self._screen.fill(pygame.Color("black"))
            self.draw_rects()
            time = pygame.time.get_ticks()
            self.print_clock(time)
            pygame.display.update()
            self._clock.tick(20)


    def print_clock(self, time):
        t = int((time-self._start_time)/1000)
        sec_val = t % 60
        sec = str(sec_val) if sec_val >= 10 else '0' + str(sec_val)
        min_val = t // 60
        min = str(min_val) if min_val >= 10 else '0' + str(min_val)
        myfont = pygame.font.SysFont("Times New Roman", 24, bold=True)
        label = myfont.render('Time ' + str(min) + ':' + sec, False, (0, 0, 100))
        self._screen.blit(label, (100, 10))

    def draw_rects(self):
        image = pygame.image.load('bomb.png')
        for button in self._buttons:
            pygame.draw.rect(self._screen, button.color_bg, (button.col_pos, button.row_pos, 25, 25))
            if button.icon:
                self._screen.blit(image, (button.col_pos + 4, button.row_pos + 4))
            elif button.text != '':
                myfont = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
                label = myfont.render(str(button.text), True, button.color_font)
                self._screen.blit(label, (button.col_pos+5, button.row_pos-3))

    def _create_buttons(self, board_size, panel_size):
        button_list = []
        button_size = 25
        margin = 1
        screen_size = margin + board_size * (button_size + margin)
        for i in range(1, board_size + 1):
            for j in range(1, board_size + 1):
                button_list.append(Button((i, j), (panel_size + margin + (1 + button_size) * (i - 1), margin +
                                                   (1 + button_size) * (j - 1)), (150, 150, 150), (0, 0, 0)))
        return screen_size, button_list

    def edit_button(self, position, color_bg=(0, 0, 25), color_font=(0, 0, 0), icon=False, text=''):
        col_id, row_id = position
        for button in self._buttons:
            if button.col_id == col_id and button.row_id == row_id:
                if color_bg != (0, 0, 25):
                    button.color_bg = color_bg
                if color_font != (0, 0, 0):
                    button.color_font = color_font
                if icon:
                    button.icon = True
                if text != '':
                    button.text = text

    def point_button(self, position):
        x, y = position
        for button in self._buttons:
            if button.row_pos < y < button.row_pos + 25 and button.col_pos < x < button.col_pos + 25: #25 is button size
                return button.col_id, button.row_id
