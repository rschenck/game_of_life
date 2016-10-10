import pygame, sys
from pygame.locals import *
# import numpy as np
import math
import random
import time

# Define global variables
width = 1200
height = 600
cellsize = 10
fps = 60
# Catch if width and height are valid for board
assert width % cellsize == 0
assert height % cellsize == 0

black = (0,  0,  0)
white = (255,255,255)
darkgrey = (40, 40, 40)
red = (220,20,60)

# use these to track current cells and updates
gridDict = {}
otherDict = {}

class cell(object):
    def __init__(self, loc, stat):
        self.loc = loc
        self.stat = stat
        self.x = loc[0]
        self.y = loc[1]

    def check_neighbors (self, gridDict):
        # Make a class method
        # Looks around just like this
        # Assigns a status the same way
        #
        alive = 0
        dead = 0
        newStat = 0

        # passes x,y of the cell looked up from blanks and returns 0 or 1
        for x in [10, -10, 0]:
            for y in [10, -10, 0]:
                neighborx = self.x+x
                neighbory = self.y+y
                if (x,y) != (0,0):
                    try:
                        alive += gridDict[(neighborx,neighbory)].stat
                    except KeyError:
                        pass

        if alive < 2:
            newstat = 0
        elif alive > 3:
            newstat = 0
        else:
            nestat = 1



        # print('%s %s') % (alive, dead)
        if self.stat == 1:
            # print("ALIVE")
            if alive < 2:
                newStat = 0
            elif alive > 3:
                newStat = 0
            else:
                newStat = 1
        elif self.stat == 0:
            # print("DEAD")
            if alive == 3:
                newStat = 1
            else:
                pass

        self.stat = newStat


# draw an empty grid for our cells to live in
def drawGrid():
    for x in range(0, width, cellsize):
        pygame.draw.line(display_surface, darkgrey, (x,0),(x,height))
    for y in range(0, height, cellsize):
        pygame.draw.line(display_surface, darkgrey, (0,y),(width,y))
    return None

# fill gridDict will cells, randomly assign cell.stat values
def blanks(gridDict):

    for y in range(0, height, cellsize):
        for x in range (0, width, cellsize):
            gridDict[x,y] = cell((x,y), 0)

    for i in range(600,700, 10):
        gridDict[i,300] = cell((i,300), 1)
    # print str(gridDict[(100,100)].loc) + '\t' + str(gridDict[(100,100)].stat)

    return gridDict

# cycles through
def tick(gridDict):
    # newDraw = {}
    for indcell in gridDict.values():
        indcell.check_neighbors(gridDict)
        # newDraw[item] = check_neighbors(item, gridDict)
        # check_neighbors(item, gridDict)
    # gridDict = newDraw.copy()

    color(gridDict)


# draw the cells
def color(gridDict):
    to_col = gridDict
    for item in to_col:
        # draw live cells as a colored rect
        if to_col[item].stat == 1:
            pygame.draw.rect(display_surface, random_color(), (to_col[item].loc[0],to_col[item].loc[1],cellsize,cellsize))
        # draw dead cells as black rect
        elif to_col[item].stat ==0:
            pygame.draw.rect(display_surface, black, (to_col[item].loc[0],to_col[item].loc[1],cellsize,cellsize))


def main(gridDict):

    pygame.init()

    global display_surface

    fpsclock = pygame.time.Clock()
    display_surface = pygame.display.set_mode((width,height))
    display_surface.fill(black)
    pygame.display.set_caption('Game of Life')

    blanks(gridDict)
    color(gridDict)
    drawGrid()

    pygame.display.update()
    #time.sleep(20)
    x = width
    y = height
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        tick(gridDict)

        # pygame.draw.rect(display_surface, red, (x,y,cellsize,cellsize))
        # x -= 10
        # y -= 10

        drawGrid()

        pygame.display.update()
        fpsclock.tick(fps)


if __name__ == '__main__':

    main(gridDict)
