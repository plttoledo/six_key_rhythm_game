import pygame
import sys
import os

screen_width, screen_height = 800, 600

fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

pos_a = 187
pos_b = 258
pos_c = 329
pos_d = 400
pos_e = 471
pos_f = 542

speed = 3
visual_latency = 80

strum_position = 500

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
strum = pygame.image.load('assets/notestrum.png')
pressed = pygame.image.load('assets/pressed.png')
pygame.display.set_caption('Beatmania Python')

class Button():
    def __init__(self, pos, text_input, font, base_color, hover_color, file_name = None):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hover_color = base_color, hover_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.file_name = file_name

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def check_hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

def main_menu():
    menu_text = pygame.font.SysFont("Roboto", 100).render("Beatmania Python", True, "#ff5c5c")
    menu_rect = menu_text.get_rect(center=(400, 100))

    play_button = Button(pos=(400, 250), text_input="Play",
                         font=pygame.font.SysFont("Roboto", 80), base_color="#60d4fc", hover_color="White")
    quit_button = Button(pos=(400, 400), text_input="Quit",
                         font=pygame.font.SysFont("Roboto", 80), base_color="#60d4fc", hover_color="White")

    while True:
        screen.fill(black)

        pos = pygame.mouse.get_pos()

        screen.blit(menu_text, menu_rect)

        play_button.change_color(pos)
        play_button.update(screen)

        quit_button.change_color(pos)
        quit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.check_for_input(pos):
                    does_exist = os.path.isfile('settings.txt')
                    if does_exist:
                        file_browser(read_file(), 0)
                    else:
                        dir_path = os.path.dirname(os.path.realpath(__file__))
                        file_browser(dir_path, 0)
                if quit_button.check_for_input(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def write_file(text):
    settings = open("settings.txt","w", encoding='utf8')
    settings.write(text)
    settings.close()

def read_file():
    settings = open("settings.txt","r", encoding='utf8')
    text = settings.read()
    settings.close()
    return text


def file_browser(path, offset):
    write_file(path)
    file_names = os.listdir(path)
    filtered_names = []

    for name in file_names:
        full_path = f"{path}/{name}"
        if os.path.isdir(full_path):
            filtered_names.append(name)
        elif os.path.isfile(full_path):
            split = os.path.splitext(name)
            extension = split[1]
            if extension == '.mp3' or extension == '.flac':
                filtered_names.append(name)

    menu_text = pygame.font.SysFont("Roboto", 40).render(path, True, "#ff5c5c")
    menu_rect = menu_text.get_rect(center=(400, 30))

    up_button = Button(pos=(150, 70), text_input="Go to parent folder", font=pygame.font.SysFont("Roboto", 40),
                       base_color="#60d4fc", hover_color="White")
    back_button = Button(pos=(50, 570), text_input="Back", font=pygame.font.SysFont("Roboto", 40), base_color="#60d4fc",
                         hover_color="White")

    show_next = False
    if (len(filtered_names) - offset) - 24 > 0:
        next_button = Button(pos=(730, 570), text_input="Next", font=pygame.font.SysFont("Roboto", 40),
                             base_color="#60d4fc", hover_color="White")
        show_next = True

    show_prev = False
    if offset > 0:
        prev_button = Button(pos=(650, 570), text_input="Prev", font=pygame.font.SysFont("Roboto", 40),
                             base_color="#60d4fc", hover_color="White")
        show_prev = True

    file_buttons = []
    folder_buttons = []

    for idx, name in enumerate(filtered_names[offset:]):
        if idx > 24:
            break

        full_path = f"{path}/{name}"

        y = ((idx % 8) * 50) + 120
        x = (idx // 8) * 280 + 120

        adjusted_name = name
        if len(name) > 11:
            adjusted_name = f"{name[:12]}..."

        if os.path.isdir(full_path):
            folder_buttons.append(Button(pos=(x, y), text_input=adjusted_name,
                                         font=pygame.font.SysFont("Roboto", 40), base_color="#60d4fc",
                                         hover_color="White", file_name=name))
        elif os.path.isfile(full_path):
            file_buttons.append(Button(pos=(x, y), text_input=adjusted_name,
                                       font=pygame.font.SysFont("Roboto", 40), base_color="#88fc5c",
                                       hover_color="White", file_name=name))

    while True:
        hovered_name = None
        screen.fill(black)
        pos = pygame.mouse.get_pos()
        screen.blit(menu_text, menu_rect)

        up_button.change_color(pos)
        up_button.update(screen)

        back_button.change_color(pos)
        back_button.update(screen)

        if show_next:
            next_button.change_color(pos)
            next_button.update(screen)

        if show_prev:
            prev_button.change_color(pos)
            prev_button.update(screen)

        for file_button in file_buttons:
            file_button.change_color(pos)
            file_button.update(screen)
            if file_button.check_hover(pos):
                hovered_name = file_button.file_name

        for folder_button in folder_buttons:
            folder_button.change_color(pos)
            folder_button.update(screen)
            if folder_button.check_hover(pos):
                hovered_name = folder_button.file_name

        if hovered_name:
            hover_text = pygame.font.SysFont("Roboto", 40).render(hovered_name, True, "#ff5c5c")
            hover_rect = hover_text.get_rect(center=(400, 530))
            screen.blit(hover_text, hover_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if up_button.check_for_input(pos):
                    file_browser(os.path.dirname(path), 0)
                if back_button.check_for_input(pos):
                    main_menu()
                if show_next:
                    if next_button.check_for_input(pos):
                        file_browser(path, offset + 24)
                if show_prev:
                    if prev_button.check_for_input(pos):
                        file_browser(path, offset - 24)
                for file_button in file_buttons:
                    if file_button.check_for_input(pos):
                        choose_difficulty(f"{path}/{file_button.file_name}")
                for folder_button in folder_buttons:
                    if folder_button.check_for_input(pos):
                        file_browser(f"{path}/{folder_button.file_name}", 0)

        pygame.display.update()

def choose_difficulty(file_name):
    menu_text = pygame.font.SysFont("Roboto", 100).render("Choose Difficulty", True, "#ff5c5c")
    menu_rect = menu_text.get_rect(center=(400, 100))

    easy_button = Button(pos=(400, 250), text_input="Easy", font=pygame.font.SysFont("Roboto", 80),
                         base_color="#60d4fc", hover_color="White")
    hard_button = Button(pos=(400, 400), text_input="Hard", font=pygame.font.SysFont("Roboto", 80),
                         base_color="#60d4fc", hover_color="White")
    back_button = Button(pos=(50, 570), text_input="Back", font=pygame.font.SysFont("Roboto", 40), base_color="#60d4fc",
                         hover_color="White")

    while True:
        screen.fill(black)
        pos = pygame.mouse.get_pos()
        screen.blit(menu_text, menu_rect)

        easy_button.change_color(pos)
        easy_button.update(screen)

        hard_button.change_color(pos)
        hard_button.update(screen)

        back_button.change_color(pos)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_button.check_for_input(pos):
                    initialize('easy', file_name)
                if hard_button.check_for_input(pos):
                    initialize('hard', file_name)
                if back_button.check_for_input(pos):
                    main_menu()

        pygame.display.update()

if __name__ == '__main__':
    main_menu()
