from enum import Enum
import random
class Conway_Shape(Enum):
    Dot = 1
    Plus = 2
    Tub = 3
    Boat = 4
    Ship = 5
    Pond = 6
    Glider = 7
    LWSS = 8
    MWSS = 9
    HWSS = 10

    def max(self):
        count = 0
        for item in Conway_Shape:
            count = count + 1
        return count

def change_stats(gridDict, coords):
    for tup in coords:
        try:
            gridDict[tup].stat = 1
        except KeyError:
            pass

def create_glider(gridDict, x, y):
    coords = []

    # assign one of four glider orientation coordinates
    direction = random.randint(0,3)
    if direction == 0:
        coords = [(x,y),(x+10,y-10),(x+20,y+10),(x+20,y),(x+20,y-10)]
    elif direction == 1:
        coords = [(x,y),(x-10,y-10),(x-10,y-20),(x,y-20),(x+10,y-20)]
    elif direction == 2:
        coords = [(x,y),(x-10,y+10),(x-20,y+10),(x-20,y),(x-20,y-10)]
    else:
        coords = [(x,y),(x+10,y+10),(x+10,y+20),(x,y+20),(x-10,y+20)]

    # try to update each coordinate if it's in the gridDict
    change_stats(gridDict, coords)

def create_lwss(gridDict, x, y):
    coords = [(x,y-20),(x-10,y-10),(x+30,y-20),(x-10,y),(x+30,y),(x-10,y+10),(x,y+10),(x+10,y+10),(x+20,y+10)]
    change_stats(gridDict, coords)

def create_mwss(gridDict, x, y):
    coords = [(x+10,y-20),(x-10,y-10),(x+30,y-10),(x-20,y),(x-20,y+10),(x+30,y+10),(x-20,y+20),(x-10,y+20),(x,y+20),(x+10,y+20),(x+20,y+20)]
    change_stats(gridDict, coords)

def create_hwss(gridDict, x, y):
    coords = [(x,y-20),(x+10,y-20),(x-20,y-10),(x+30,y-10),(x-30,y),(x-30,y+10),(x+30,y+10),(x-30,y+20),(x-20,y+20),(x-10,y+20),(x,y+20),(x+10,y+20),(x+20,y+20)]
    change_stats(gridDict, coords)

def create_boat(gridDict, x, y):
    coords = [(x-10,y-10),(x,y-10),(x-10,y),(x+10,y),(x,y+10)]
    change_stats(gridDict, coords)

def create_ship(gridDict, x, y):
    coords = [(x-10,y-10),(x,y-10),(x-10,y),(x+10,y),(x,y+10),(x+10,y+10)]
    change_stats(gridDict, coords)

def create_pond(gridDict, x, y):
    coords = [(x-10,y-10),(x,y-10),(x-20,y),(x+10,y),(x-20,y+10),(x+10,y+10),(x-10,y+20),(x,y+20)]
    change_stats(gridDict, coords)

def create_plus(gridDict, x, y):
    coords = [(x,y-10),(x-10,y),(x,y),(x+10,y),(x,y+10)]
    change_stats(gridDict, coords)

def create_tub(gridDict, x, y):
    coords = [(x,y-10),(x-10,y),(x+10,y),(x,y+10)]
    change_stats(gridDict, coords)

def click_handler(gridDict, x, y, click_option):
    choice = click_option
    if choice == 1:
        gridDict[x,y].stat = 1;
    elif choice == 2:
        create_plus(gridDict, x, y)
    elif choice == 3:
        create_tub(gridDict, x, y)
    elif choice == 4:
        create_boat(gridDict, x, y)
    elif choice == 5:
        create_ship(gridDict, x, y)
    elif choice == 6:
        create_pond(gridDict, x, y)
    elif choice == 7:
        create_glider(gridDict, x, y)
    elif choice == 8:
        create_lwss(gridDict, x, y)
    elif choice == 9:
        create_mwss(gridDict, x, y)
    elif choice == 10:
        create_hwss(gridDict, x, y)
    else:
        pass
