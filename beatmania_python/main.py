import pygame
import sys
import os

from create_beats import beat_array


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

class Note(pygame.sprite.Sprite):
    def __init__(self, identity, strum_time, position):
        pygame.sprite.Sprite.__init__(self)
        self.idnum = identity
        self.strum = strum_time
        self.miss = False
        self.hit = False
        self.difference = -2000000
        if position == 1:
            self.image = pygame.image.load('assets/noteA.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(pos_a, -100)
        if position == 2:
            self.image = pygame.image.load('assets/noteB.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(pos_b, -100)
        if position == 3:
            self.image = pygame.image.load('assets/noteC.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(pos_c, -100)
        if position == 4:
            self.image = pygame.image.load('assets/noteC.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(pos_d, -100)
        if position == 5:
            self.image = pygame.image.load('assets/noteB.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(pos_e, -100)
        if position == 6:
            self.image = pygame.image.load('assets/noteA.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(pos_f, -100)

    def update(self, pressed, time):
        if self.hit or self.miss:
            self.kill()

        if not self.hit and not self.miss and self.rect.centery > 520:
            self.miss = True
            self.difference = -1000000

        if self.rect.centery > 480 and not self.miss and pressed:
            if not self.hit:
                pressed = False
                self.difference = self.strum - time
            self.hit = True

    def move(self, shift):
        if shift > 0:
            self.rect.centery = shift

def combo_count(amount):
    font = pygame.font.SysFont("Roboto", 40)
    text = font.render( f"Combo: {amount}", True, white)
    screen.blit(text, (20, 20))

def multiplier_count(amount):
    font = pygame.font.SysFont("Roboto", 40)
    text = font.render( f"{amount}x", True, white)
    screen.blit(text, (20, 50))

def score_count(score_amount):
    font = pygame.font.SysFont("Roboto", 40)
    text = font.render(f"{score_amount}", True, white)
    screen.blit(text, (630, 20))

def initialize(difficulty, audio_file_name):
    print('Loading...')

    try:
        beatmap, ending_time = beat_array(audio_file_name, difficulty)
    except:
        print('Unable to read audio file')
        main_menu()

    game_loop(audio_file_name, beatmap, ending_time)

def game_loop(file_name, beatmap, ending_time):
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.set_volume(0.1)

    combo = 0
    score = 0
    multipier = 1

    keypress_s = False
    keypress_d = False
    keypress_f = False
    keypress_j = False
    keypress_k = False
    keypress_l = False

    notes_a = pygame.sprite.Group()
    notes_b = pygame.sprite.Group()
    notes_c = pygame.sprite.Group()
    notes_d = pygame.sprite.Group()
    notes_e = pygame.sprite.Group()
    notes_f = pygame.sprite.Group()

    note_dict = {
        1: notes_a.add,
        2: notes_b.add,
        3: notes_c.add,
        4: notes_d.add,
        5: notes_e.add,
        6: notes_f.add,
    }

    for idx, beat in enumerate(beatmap):
        timing = beat['time']
        position = beat['position']
        note_dict[position](Note(idx, timing, position))

    print('Loading Done!')

    current = 0
    previous_frametime = 0
    last_play_head_position = 0
    most_accurate = 0

    pygame.mixer.music.play()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    keypress_s = True
                if event.key == pygame.K_d:
                    keypress_d = True
                if event.key == pygame.K_f:
                    keypress_f = True
                if event.key == pygame.K_j:
                    keypress_j = True
                if event.key == pygame.K_k:
                    keypress_k = True
                if event.key == pygame.K_l:
                    keypress_l = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    keypress_s = False
                if event.key == pygame.K_d:
                    keypress_d = False
                if event.key == pygame.K_f:
                    keypress_f = False
                if event.key == pygame.K_j:
                    keypress_j = False
                if event.key == pygame.K_k:
                    keypress_k = False
                if event.key == pygame.K_l:
                    keypress_l = False

        current += clock.get_time()

        if current >= ending_time:
            pygame.mixer.music.unload()
            main_menu()

        most_accurate += current - previous_frametime
        previous_frametime = current
        song_time = pygame.mixer.music.get_pos()
        if song_time != last_play_head_position:
            most_accurate = (most_accurate + song_time) / 2
            last_play_head_position = song_time

        if combo < 10:
            multipier = 1
        if 10 <= combo < 20:
            multipier = 2
        elif 20 <= combo < 30:
            multipier = 3
        elif 30 <= combo:
            multipier = 4

        screen.fill(black)
        combo_count(combo)
        multiplier_count(multipier)
        score_count(score)

        if keypress_s:
            screen.blit(pressed, (pos_a, 494))
        if keypress_d:
            screen.blit(pressed, (pos_b, 494))
        if keypress_f:
            screen.blit(pressed, (pos_c, 494))
        if keypress_j:
            screen.blit(pressed, (pos_d, 494))
        if keypress_k:
            screen.blit(pressed, (pos_e, 494))
        if keypress_l:
            screen.blit(pressed, (pos_f, 494))

        notes_a.draw(screen)
        notes_b.draw(screen)
        notes_c.draw(screen)
        notes_d.draw(screen)
        notes_e.draw(screen)
        notes_f.draw(screen)

        screen.blit(strum, (0, 0))

        for note in notes_a:
            distance = strum_position - (note.strum / speed - most_accurate / speed) + visual_latency
            note.move(distance)
            status_a = note.difference
            if -500 <= status_a <= 500:
                combo += 1
                score += 1000 * multipier
            elif status_a == -1000000:
                combo = 0

        for note in notes_b:
            distances = strum_position - (note.strum / speed - most_accurate / speed) + visual_latency
            note.move(distances)
            status_b = note.difference
            if -500 <= status_b <= 500:
                combo += 1
                score += 1000 * multipier
            elif status_b == -1000000:
                combo = 0

        for note in notes_c:
            distance = strum_position - (note.strum / speed - most_accurate / speed) + visual_latency
            note.move(distance)
            status_c = note.difference
            if -500 <= status_c <= 500:
                combo += 1
                score += 1000 * multipier
            elif status_c == -1000000:
                combo = 0

        for note in notes_d:
            distance = strum_position - (note.strum / speed - most_accurate / speed) + visual_latency
            note.move(distance)
            status_d = note.difference
            if -500 <= status_d <= 500:
                combo += 1
                score += 1000 * multipier
            elif status_d == -1000000:
                combo = 0

        for note in notes_e:
            distance = strum_position - (note.strum / speed - most_accurate / speed) + visual_latency
            note.move(distance)
            status_e = note.difference
            if -500 <= status_e <= 500:
                combo += 1
                score += 1000 * multipier
            elif status_e == -1000000:
                combo = 0

        for note in notes_f:
            distance = strum_position - (note.strum / speed - most_accurate / speed) + visual_latency
            note.move(distance)
            status_f = note.difference
            if -500 <= status_f <= 500:
                combo += 1
                score += 1000 * multipier
            elif status_f == -1000000:
                combo = 0

        notes_a.update(keypress_s, most_accurate)
        notes_b.update(keypress_d, most_accurate)
        notes_c.update(keypress_f, most_accurate)
        notes_d.update(keypress_j, most_accurate)
        notes_e.update(keypress_k, most_accurate)
        notes_f.update(keypress_l, most_accurate)

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    main_menu()
