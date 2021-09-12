import pygame
import time
import random
import string
import requests
import json

window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 200)
soup_color = pygame.Color(203, 66, 20)
noodle_color = pygame.Color(247, 165, 66)

snake_speed = 15
unit = 10
font = 'comicsansms'
high_score = 0

soup_valid_x_start = 100
soup_valid_x_start = 60


# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Alphabet Soup')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()


def show_score(color, font, size, text, y_pos):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(text, True, color)
    score_rect = score_surface.get_rect(y=y_pos)
    game_window.blit(score_surface, score_rect)

# game over function
# when snake hits itself or the wall


def text_objects(text, font, color=noodle_color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(text, x, y, w, h, initial_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_window, active_color, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_window, initial_color, (x, y, w, h))

    smallText = pygame.font.SysFont(font, 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    game_window.blit(textSurf, textRect)


def render_food(food_letter, food_pos):
    smallText = pygame.font.SysFont(font, 20)
    textSurf, textRect = text_objects(food_letter, smallText)
    textRect.center = (food_pos[0] + unit/2, food_pos[1] + unit/4)
    game_window.blit(textSurf, textRect)


def quit_game():
    pygame.quit()
    quit()


def run_game():
    snake_position = [100, 50]
    snake_body = [[100, 100]]
    word = ""

    food_pos = [random.randrange(1, (window_x//unit)) * unit,
                random.randrange(1, (window_y//unit)) * unit]
    food_spawn = True
    food_letter = random.choice(string.ascii_lowercase)

    food_pos_1 = [random.randrange(1, (window_x//unit)) * unit,
                  random.randrange(1, (window_y//unit)) * unit]
    food_letter_1 = random.choice(string.ascii_lowercase)

    direction = 'DOWN'
    change_to = direction

    score = 0
    message = ""
    while True:
        snake_color = noodle_color
        score_color = noodle_color

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    word = ""
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        else:
            snake_color = red

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= unit
        if direction == 'DOWN':
            snake_position[1] += unit
        if direction == 'LEFT':
            snake_position[0] -= unit
        if direction == 'RIGHT':
            snake_position[0] += unit

        # grow body. add to score
        snake_body.insert(0, list(snake_position))
        if snake_color == red:
            snake_body.pop()
            show_score(score_color, font, 20, "", 20)
        elif snake_position[0] == food_pos[0] and snake_position[1] == food_pos[1]:
            score += 1
            word += food_letter
            response_API = requests.get(
                'https://api.dictionaryapi.dev/api/v2/entries/en/' + word)

            if (isinstance(response_API.json(), list)):
                response_str = str(response_API.json()[0])
            else:
                response_str = str(response_API.json())

            if (not ("No Definitions Found" in response_str or "\'partOfSpeech\': \'abbreviation\'" in response_str)):
                print(response_str)
                message = word + " is a word! +" + str(len(word)) + "points."
                score += len(word)
            else:
                message = ""
            food_spawn = False
        elif snake_position[0] == food_pos_1[0] and snake_position[1] == food_pos_1[1]:
            score += 1
            word += food_letter_1
            response_API = requests.get(
                'https://api.dictionaryapi.dev/api/v2/entries/en/' + word)

            if (isinstance(response_API.json(), list)):
                response_str = str(response_API.json()[0])
            else:
                response_str = str(response_API.json())

            if (not ("No Definitions Found" in response_str or "\'partOfSpeech\': \'abbreviation\'" in response_str)):
                print(response_str)
                message = word + " is a word! +" + str(len(word)) + "points."
                score += len(word)
            else:
                message = ""
            food_spawn = False
        else:
            snake_body.pop()
            show_score(score_color, font, 20, "", 20)

        if not food_spawn:
            food_pos = [random.randrange(1, (window_x//unit)) * unit,
                        random.randrange(1, (window_y//unit)) * unit]
            food_letter = random.choice(string.ascii_lowercase)
            food_pos_1 = [random.randrange(1, (window_x//unit)) * unit,
                          random.randrange(1, (window_y//unit)) * unit]
            food_letter_1 = random.choice(string.ascii_lowercase)

        food_spawn = True
        game_window.fill(soup_color)

        for pos in snake_body:
            pygame.draw.rect(game_window, snake_color, pygame.Rect(
                pos[0], pos[1], unit, unit))

        # render food
        render_food(food_letter, food_pos)
        render_food(food_letter_1, food_pos_1)

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-unit:
            intro_screen(score)
        if snake_position[1] < 0 or snake_position[1] > window_y-unit:
            intro_screen(score)

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                intro_screen(score)

        show_score(score_color, font, 20, 'Score: ' + str(score), 0)
        show_score(score_color, font, 20, 'Word: ' + word, 20)
        show_score(score_color, font, 20, message, 40)

        pygame.display.update()

        global high_score
        high_score = max(score, high_score)
        # refresh rate
        fps.tick(snake_speed)


def intro_screen(score):
    # the intro code
    intro = True
    
    while intro:
        # must handle OS event or will freeze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_window.fill(soup_color)
        
        spacing = 25
        instructions_y = 130
        title_font = pygame.font.SysFont(font, 20)
        title_title_font = pygame.font.SysFont(font, 30)
        title_desc_font = pygame.font.SysFont(font, 15)
        print_title('Alphabet Soup', 0, title_title_font)
        print_title('HighScore : ' + str(high_score) + ' ', 70, title_font)
        print_title('Score : ' + str(score), 100, title_font)
        print_title('How to Play:', instructions_y, title_desc_font)
        print_title('eat letters to earn 1 point.', instructions_y + spacing, title_desc_font)
        print_title('spell a valid words to earn points equal to the word length.', instructions_y + spacing * 2, title_desc_font)
        print_title('try to get as many points as possible.', instructions_y + spacing * 3, title_desc_font)

        # pygame.display.flip()

        button_y = 150
        button("PLAY", window_x//3 - 50, window_y//2 + button_y,
               100, 50, green, bright_green, run_game)
        button("QUIT", 2 * window_x//3 - 50, window_y //
               2 + button_y, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        fps.tick(snake_speed)


def print_title(text, y, title_font):
    game_over_surface = title_font.render(text, True, noodle_color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4 + y)
    game_window.blit(game_over_surface, game_over_rect)

intro_screen(0)
