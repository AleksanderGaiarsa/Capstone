from curses import KEY_DOWN
import pygame, sys
import pygame_gui

pygame.font.init()
FONT = pygame.font.Font("./Game/assets/font.ttf", 26)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class Menu_Button():
    def __init__(self, image, bg_size:list, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.img_size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.img_size[0]*bg_size[0]), int(self.img_size[1]*bg_size[1])))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class NameBox:
    def __init__(self, x, y, w, h,):
        self.x = x
        self.y = y

        self.surface = pygame.Surface((w, h))
        self.surf_rect = self.surface.get_rect(center=(self.x, self.y))
        self.surface.fill((255,255,255))
        self.surface.set_colorkey((255,0,255))
        self.surface.set_alpha(225)

        self.font = pygame.font.Font("./Game/assets/font.ttf", 26)
        self.enter_n_txt = self.font.render('Enter Your Name', False, (0, 0, 0))
        self.enter_n_rect = self.enter_n_txt.get_rect(center=(self.surf_rect.centerx, self.surf_rect.centery-80))

        self.input_box = InputBox(x = self.surf_rect.centerx,
                                y = self.surf_rect.centery,
                                w = 475,
                                h = 50)

        self.enter_button = Menu_Button(image=None,
                                    bg_size=(1,1),
                                    pos=(self.surf_rect.centerx-80, self.surf_rect.centery+80), 
                                    text_input="Enter",
                                    font=self.font,
                                    base_color="Black",
                                    hovering_color="Green")

        self.back_button = Menu_Button(image=None,
                                    bg_size=(1,1),
                                    pos=(self.surf_rect.centerx+80, self.surf_rect.centery+80), 
                                    text_input="Back",
                                    font=self.font,
                                    base_color="Black",
                                    hovering_color="Green")

    def draw(self, screen, mouse_pos):
        screen.blit(self.surface, self.surf_rect)
        screen.blit(self.enter_n_txt, self.enter_n_rect)
        self.input_box.draw(screen)
        self.enter_button.changeColor(mouse_pos)
        self.enter_button.update(screen)
        self.back_button.changeColor(mouse_pos)
        self.back_button.update(screen)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.center = [x,y]
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.txt_surface_rect = self.txt_surface.get_rect(center=(x,y))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                self.txt_surface_rect = self.txt_surface.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, self.txt_surface_rect)
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class menu():
    def __init__(self):
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('./Game/assets/Dance_of_the_Decorous.mp3')
            pygame.mixer.music.play(100, start=10)

        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        pygame.display.set_caption("Menu")

        picture = pygame.image.load("./Game/assets/Background.png")
        self.bg = pygame.transform.scale(picture, (self.width, self.height))

        self.diff_list = ['Easy', 'Medium', 'Hard', 'Very Hard']
        self.bullet_rate_ind = 1

        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.manager.add_font_paths(font_name = 'menu_font', regular_path="./Game/assets/font.ttf")
        self.manager.preload_fonts(font_list=({'name':'menu_font', 'point_size': 10, 'style':'regular'},))
        self.clock = pygame.time.Clock()

        self.main_menu()

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("./Game/assets/font.ttf", size)
        
    def options(self):
        self.lvl_diff=pygame_gui.elements.UIDropDownMenu(options_list= self.diff_list,
                                        starting_option='Medium',
                                        anchors={'centerx': 'centerx','centery': 'centery'},
                                        relative_rect=pygame.Rect((0, 0), (300, 100)),
                                        manager=self.manager)

        self._diff_back = Menu_Button(image=None, bg_size=(1,1),
                                pos=(self.width/2, 600), 
                                text_input="BACK", 
                                font=self.get_font(75), 
                                base_color="#d7fcd4", 
                                hovering_color="White")

        while True:
            self.delta_t = self.clock.tick(60)/1000.0

            self.diff_mouse_pos = pygame.mouse.get_pos()

            self._diff_back.changeColor(self.diff_mouse_pos)
            self._diff_back.update(self.display)

            pygame.display.update()
            self.display.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.display)
            self.manager.update(self.delta_t)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self._diff_back.checkForInput(self.diff_mouse_pos):
                        self.lvl_diff.kill()
                        return
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.lvl_diff:
                        self.bullet_rate_ind = self.diff_list.index(event.text)
            
                self.manager.process_events(event)

    def main_menu(self):

        self.menu_txt = self.get_font(100).render("MAIN MENU", True, "#b68f40")
        self.menu_rect = self.menu_txt.get_rect(center=(self.width/2, 100))

        self.button_height = (self.height/4)

        self.play_button = Menu_Button(image=pygame.image.load("./Game/assets/Play Rect.png"),
                                    bg_size=(1,1), 
                                    pos=(self.width/2, self.button_height+50), 
                                    text_input="PLAY", 
                                    font=self.get_font(75), 
                                    base_color="#d7fcd4", 
                                    hovering_color="White")

        self.options_button = Menu_Button(image=pygame.image.load("./Game/assets/Diff_Rect.png"), 
                                        bg_size=(1.4,1),
                                        pos=(self.width/2, (self.button_height*2)+50), 
                                        text_input="OPTIONS",
                                        font=self.get_font(75), base_color="#d7fcd4",
                                        hovering_color="White")

        self.quit_button = Menu_Button(image=pygame.image.load("./Game/assets/Quit Rect.png"),
                                    bg_size=(1,1),
                                    pos=(self.width/2, (self.button_height*3)+50), 
                                    text_input="QUIT",
                                    font=self.get_font(75),
                                    base_color="#d7fcd4",
                                    hovering_color="White")
        self.run = True

        while self.run:

            self.delta_t = self.clock.tick(60)/1000.0

            self.menu_mouse_pos = pygame.mouse.get_pos()

            self.display.blit(self.menu_txt, self.menu_rect)

            pygame.display.update()
            self.display.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.display)
            self.manager.update(self.delta_t)

            for button in [self.play_button, self.options_button, self.quit_button]:
                button.changeColor(self.menu_mouse_pos)
                button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('mouse clicked in main menu')
                    if self.play_button.checkForInput(self.menu_mouse_pos):
                        if self.play():
                            pygame.mixer.music.fadeout(500)
                            return
                    elif self.options_button.checkForInput(self.menu_mouse_pos):
                        self.options()
                    elif self.quit_button.checkForInput(self.menu_mouse_pos):
                        self.run = False
        
    def play(self) -> bool:

        self.name_box = NameBox(x = self.width/2, 
                            y = self.height/2,
                            w = 550,
                            h = 250)

        while True:
            self.delta_t = self.clock.tick(60)/1000.0

            self.menu_mouse_pos = pygame.mouse.get_pos()

            self.display.blit(self.menu_txt, self.menu_rect)

            pygame.display.update()
            self.display.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.display)
            self.manager.update(self.delta_t)

            for button in [self.play_button, self.options_button, self.quit_button]:
                button.update(self.display)
            
            self.name_box.draw(self.display, self.menu_mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.name_box.enter_button.checkForInput(self.menu_mouse_pos):
                        if self.name_box.input_box.text:
                            self.player_name = self.name_box.input_box.text
                            self.name_box.text = ''
                            return True
                    elif self.name_box.back_button.checkForInput(self.menu_mouse_pos):
                        return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.name_box.input_box.text:
                            self.player_name = self.name_box.input_box.text
                            self.name_box.text = ''
                            return True

                self.name_box.input_box.handle_event(event)
