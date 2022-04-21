import pygame
import random
import os.path
import sys

pygame.font.init()

#VARIABILE
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30

stop = True
run = True

#POZITIONAREA SPATIULUI DE JOC
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

#PIESE SI ROTATII
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [ [(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color,):
   font = pygame.font.SysFont('arial', size, bold = True)
   label = font.render(text, 1, color)

   surface.blit(label, (top_left_x + play_width/2 -(label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range (len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        full = False
        if (0,0,0) not in row:
            inc += 1
            full = True
        if inc > 0 and full == False:
            for j in range(len(row)):
                if (j , i) in locked:
                    locked[(j,i + inc)] = locked.pop((j,i))
                else:
                    locked[(j, i + inc)] = (0,0,0)

    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height - 550
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0 )
                pygame.draw.rect(surface, (128, 128, 128), (int(sx + j * 30), int(sy + i * 30), 30, 30), 1) #grid pentru piese
    surface.blit(label, (sx + 15, sy - 50))

def update_score(new_score, missing_file=False):
    if missing_file == True:
        with open('scores.txt', 'w') as f:
            f.write(str(new_score))
    else:
        score = high_score()
        with open('scores.txt', 'w') as f:
            if int(score) > new_score:
                f.write(str(score))
            else :
                f.write(str(new_score))

def high_score():
    if os.path.isfile('scores.txt'):
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()
        return score
    else:
        update_score(0, True)


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((81, 50, 92))

    pygame.font.init()
    font = pygame.font.SysFont('verdana', 70)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 10))

    #delimitarea spatiului pentru scor
    pygame.draw.rect(surface, (143, 128, 153), (570, 380, 225, 110))
    pygame.draw.rect(surface, (77, 25, 51), (570, 380, 225, 110), 6)


    #current score
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 65
    sy = top_left_y + play_height - 450

    surface.blit(label, (sx + 18, sy + 140))

    #high score
    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 15
    sy = top_left_y + play_height - 400

    surface.blit(label, (sx + 18, sy + 140))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (250, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid)

def pause(surface):
    global stop
    global run
    while stop:
        surface.fill((81, 50, 92))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    stop = False
        pygame.draw.rect(surface, (143, 128, 153), (0, top_left_y + play_height / 2 - 100, 800, 200))
        draw_text_middle(surface, "GAME PAUSED", 90, (255, 255, 255))
        pygame.display.update()


def main(win):
    last_score = high_score()
    locked_positions = { }
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece= get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0
    global stop

    while run:
        grid = create_grid(locked_positions)

        #asiguram aceeasi viteza de cadere a pieselor indiferent de performanta calcuatorului
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        #crestem treptat viteza cu care cad piesele
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        #caderea piesei
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y>0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()

            #controlul piselor
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x +=1
                if event.key == pygame.K_RIGHT:
                    current_piece.x +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -=1
                if event.key == pygame.K_DOWN:
                    current_piece.y +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -=1
                if event.key == pygame.K_UP:
                    current_piece.rotation +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -=1
                if event.key == pygame.K_SPACE:
                    while current_piece.y < 21 and (valid_space(current_piece, grid)):
                        current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_p:
                    stop = True
                    pause(win)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            combo = clear_rows(grid, locked_positions)
            if combo == 1:
                score += 40
            if combo == 2:
                score += 100
            if combo == 3:
                score += 300
            if combo == 4:
                score += 1200

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            pygame.draw.rect(win, (143, 128, 153), (0, top_left_y + play_height/2 - 100, 800, 200))
            draw_text_middle(win, "YOU LOST!", 90, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            update_score(score)



def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press any key to start', 80, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)