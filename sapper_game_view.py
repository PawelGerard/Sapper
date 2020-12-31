import pygame


class Button:
    def __init__(self, pos_id, pos, color_bg, color_font):
        self.row_id, self.col_id = pos_id
        self.row_pos, self.col_pos = pos
        self.color_bg = color_bg
        self.color_font = color_font
        self.text = ''
        self.icon = False


class Game:
    def __init__(self, controller, board_size):
        self._controller = controller
        self._screen_size, self._buttons = self._create_buttons(board_size)
        pygame.init()
        self._screen = pygame.display.set_mode((self._screen_size,)*2)
        _bomb_icon = pygame.image.load('bomb_icon.png')
        pygame.display.set_caption('Mine Sweeper')
        pygame.display.set_icon(_bomb_icon)

    def main(self):
        run = True
        while run:
            for event in pygame.event.get():
                run = self._controller.action_on_click(event)
            self.draw_rects()
            pygame.display.update()

    def draw_rects(self):
        image = pygame.image.load('bomb.png')
        for button in self._buttons:
            pygame.draw.rect(self._screen, button.color_bg, (button.row_pos, button.col_pos, 25, 25))
            if button.icon:
                self._screen.blit(image, (button.row_pos + 4, button.col_pos + 4))
            elif button.text != '':
                myfont = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
                label = myfont.render(str(button.text), True, button.color_font)
                self._screen.blit(label, (button.row_pos+5, button.col_pos-3))

    def _create_buttons(self, board_size):
        button_list = []
        button_size = 25
        margin = 1
        screen_size = margin + board_size * (button_size + margin)
        for i in range(1, board_size + 1):
            for j in range(1, board_size + 1):
                button_list.append(Button((i, j), (margin + (1 + button_size) * (i - 1),
                                                   margin + (1 + button_size) * (j - 1)), (150, 150, 150), (0, 0, 0)))
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
            if button.row_pos < y < button.row_pos + 25 and button.col_pos < x < button.col_pos + 25:
                return button.row_id, button.col_id
