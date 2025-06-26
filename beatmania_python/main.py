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