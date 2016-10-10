import pygame, sys
from pygame.locals import *
# import numpy as np
import math
import random
import time


from functionality import random_color, user_select, start, stop, reset, reset_options, info_button, info, click_creator
from presets import gun, create_glider, blank, tens, pulsar, gliders, maze, faces, binary_101, rando

# Define global variables
# width = 1200
# height = 600
cellsize = 10
fps = 30.0


black = (0,  0,  0)
white = (255,255,255)
darkgrey = (40, 40, 40)
red = (220,20,60)
b_red = (255,0,0)
green = (0,200,0)
b_green = (0,255,0)

# use these to track current cells and updates
gridDict = {}
otherDict = {}

class cell:
    def __init__(self, loc, stat):
        self.loc = loc
        self.stat = stat

# draw an empty grid for our cells to live in
def drawGrid(width, height):
    for x in range(0, width, cellsize):
        pygame.draw.line(display_surface, darkgrey, (x,0),(x,height))
    for y in range(0, height, cellsize):
        pygame.draw.line(display_surface, darkgrey, (0,y),(width,y))
    return None

# fill gridDict will cells, randomly assign cell.stat values
def blanks(gridDict, width, height):

    for y in range(-20, height+20, cellsize):
        for x in range (-20, width+20, cellsize):
            # stat = 1 if random.randint(0,12) > 10 else 0
            stat = 0
            gridDict[x,y] = cell((x,y), stat)

    # Default Starting option
    rando(gridDict)

    return gridDict

def user_tick(gridDict):
    #Colors user boxes
    color(gridDict)

def check_neighbors(item, gridDict):
    '''
        alive - number of neighboring cells that are alive
        dead - 1: current cell is alive, 0: its dead
        newStat - value to assign to the new cell object
    '''
    alive = 0
    dead = 0
    newStat = 0

    # cycle through neigbors and increment alive and assign dead
    for x in [10, -10, 0]:
        for y in [10, -10, 0]:
            if (x,y) != (0,0):
                    try:
                        alive += gridDict[(item[0]+x,item[1]+y)].stat
                    except KeyError:
                        pass
            else:
                try:
                    dead += gridDict[(item[0]+x,item[1]+y)].stat
                except KeyError:
                    pass
    # implement rules for conway's game of life
    if dead == 1:
        if alive < 2 or alive > 3:
            newStat = 0
        else:
            newStat = 1
    elif dead == 0:
        if alive == 3:
            newStat = 1
        else:
            pass
    if x < -10 or y < -10 or x > 510 or y > 510:
        newStat = 0
    return cell(item, newStat)

# update cells for next round
def tick(gridDict, otherDict):
    for item in gridDict:
        otherDict[item] = check_neighbors(item, gridDict)

    copyDict = otherDict.copy()
    otherDict = {}
    gridDict = copyDict.copy()
    # redraw cells
    color(gridDict)
    return gridDict, otherDict

# draw the cells
def color(gridDict):
    to_col = gridDict
    for item in to_col:
        # draw live cells as a colored rect
        color = white if to_col[item].stat == 1 else black
        try:
            pygame.draw.rect(display_surface, color, (to_col[item].loc[0],to_col[item].loc[1],cellsize,cellsize))
        except KeyError:
            pass
        # draw dead cells as black rect


def banner(display_surface, x, y):
    pygame.draw.rect(display_surface, white, (0, y-30, x, 30))

def main(gridDict, otherDict):
    pygame.init()
    pygame.mixer.init()

    # get screen size
    display_info = pygame.display.Info()

    if display_info.current_w > 2000:
        width = int(display_info.current_w/2.)
        height = int(display_info.current_h/2.)
    else:
        width = int(display_info.current_w)
        height = int(display_info.current_h)

    # Catch if width and height are valid for board
    assert width % cellsize == 0
    assert height % cellsize == 0

    pygame.mixer.music.load('sound/emotion.wav')
    pygame.mixer.music.play(loops=-1, start=0.0)

    global display_surface

    fpsclock = pygame.time.Clock()
    display_surface = pygame.display.set_mode((width,height))
    display_surface.fill(black)
    pygame.display.set_caption('Game of Life')

    blanks(gridDict, width, height)
    color(gridDict)
    drawGrid(width, height)

    x = width
    y = height
    click_option = 1
    mouse = (0,0,0)
    reset_this = False
    show_i = False
    option = ''
    banner(display_surface, x, y)
    run = start(display_surface, width, height)

    pygame.display.update()
    # time.sleep(40)

    # pos = (0,0)
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse = (1,0,0) if event.button == 1 else (0,0,0)
                # pos = event.pos

        # mouse = mouse if mouse else pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        # User picks grids (not if option menu is on)
        if mouse[0]:
            if reset_this == False and show_i == False:
                # create_glider(gridDict,pos[0],pos[1])
                user_select(gridDict,pos[0],pos[1],width, height, click_option)

        if run:
            gridDict, otherDict = tick(gridDict, otherDict)
        else:
            pass

        user_tick(gridDict)
        drawGrid(width, height)

        banner(display_surface, x, y)

        # Controls
        click_option = click_creator(display_surface, width, height, click_option, pos, mouse)
        if run:
            run = stop(display_surface, width, height, pos, mouse)
            run, reset_this = reset(display_surface, width, height, run, pos, mouse)
            # info panel
            run, show_i = info_button(display_surface, width, height, run, pos, mouse)
        else:
            # stops start from being displayed with the Reset choices
            if reset_this or show_i:
                pass
            else:
                run = start(display_surface, width, height, pos, mouse)
                # info panel
                run, show_i = info_button(display_surface, width, height, run, pos, mouse)

        # Brings up options menu
        if reset_this:
            option = reset_options(display_surface, width, height, pos, mouse)
        else:
            pass

        if option == 'Blank':
            blank(gridDict)
            reset_this = False
        elif option == 'Gun':
            blank(gridDict)
            gun(gridDict)
            reset_this = False
        elif option == 'Ten':
            blank(gridDict)
            tens(gridDict)
            reset_this = False
        elif option == 'Binary':
            blank(gridDict)
            binary_101(gridDict)
            reset_this = False
        elif option == 'Face':
            blank(gridDict)
            faces(gridDict)
            reset_this = False
        elif option == 'Maze':
            blank(gridDict)
            maze(gridDict)
            reset_this = False
        elif option == 'Pulsar':
            blank(gridDict)
            pulsar(gridDict)
            reset_this = False
        elif option == 'Gliders':
            blank(gridDict)
            gliders(gridDict)
            reset_this = False
        elif option == 'Random':
            blank(gridDict)
            rando(gridDict)
            reset_this = False
        else:
            pass

        if show_i:
            show_i = info(display_surface, width, height, pos, mouse)
        else:
            pass

        pygame.display.update()
        fpsclock.tick(fps)

        mouse = (0,0,0)
        option = ''


if __name__ == '__main__':
    main(gridDict, otherDict)
