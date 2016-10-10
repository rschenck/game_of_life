from kivy.app import App
from collections import defaultdict
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.uix.settings import SettingsWithSpinner
from settings_options import settings_json
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.image import Image
from random import randint
from random import uniform
from functools import partial
import math

# def song(music):
#     sound = SoundLoader.load('img/emotion.wav')
#     if sound and music:
#         sound.loop = True
#         sound.play()
#
def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
        pass


class Grid(Widget):
    def draw_grid(self, *largs):
        self.size = (Window.width, Window.height - 50) # Should be fine to draw off window size
        self.pos = (0,50)
        with self.canvas:
            Color(0.5,0.5,0.5, mode='rgb')
            for x in range(10,self.width,10):
                Rectangle(pos=(x,self.y),size=(1,self.height))
            for y in range(self.y,self.height+self.y,10):
                Rectangle(pos=(self.x,y),size=(self.width,1))
            Rectangle(pos=(self.x,self.y),size=(10,self.height))
            Rectangle(pos=(self.x,self.y),size=(self.width,10))
            Rectangle(pos=(self.width-10,self.y),size=(10,self.height))
            Rectangle(pos=(self.x,self.y+self.height-10),size=(self.width,10))

class Cells(Widget):
    allcols = {
    'White': Color(1,1,1,mode="rgb"),
    'Grey': Color(0.5,0.5,0.5,mode="rgb"),
    'Blue': Color(0,0,1,mode="rgb"),
    'Green': Color(0,1,0,mode="rgb"),
    'Red': Color(1,0,0,mode="rgb"),
    'Random': Color(0,0,0,mode="rgb")
    }
    # speed, cellcol, birth, lonely, crowded = .1, 'White', 3, 1, 4
    # update_count = 0
    dimensions = None # Use this instead of self.size, which resets each frame
    rectangles_dict = {}
    on_board = defaultdict(int)
    changes_dict = {}
    mid_x,mid_y = 0,0
    mouse_positions = []
    should_draw = False # allows touches to add rectangles
    accept_touches = False # Avoid sticky cell from intial click/move

# Starting Patterns
# Each will:
# 1) call self.setup_cells() to make sure color, and midpoint are set
# 2) Then assign values to self.on_board using midpoint value to center the patterns
# 3) call modal.dismiss() --> triggers calls to grid.draw_grid and cells.starting_cells

    def assign_random(self, modal, *largs):
        self.setup_cells()
        # Loop through possible x and y indexes
        for x in range(0,self.dimensions[0]/10):
            for y in range(0,self.dimensions[1]/10):
                # assign 25% chance of life
                if randint(0,3) == 1:
                    self.on_board[x,y] = 1
        modal.dismiss()

    def assign_blank(self, modal, *largs):
        self.setup_cells()
        modal.dismiss()

    def assign_gun(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -20 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -20 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 14 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 14 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 15 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 15 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 15 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 15 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 15 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 16 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 17 ,self.mid_y -4 )]=1

        modal.dismiss()

    def assign_ten(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -6 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 2 )]=1

        modal.dismiss()

    def assign_binary(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -12 ,self.mid_y )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 5 )]=1

        modal.dismiss()

    def assign_face(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -5 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 9 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 10 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 9 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 10 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 9 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 10 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 11 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 9 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 10 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -4 )]=1

        modal.dismiss()

    def assign_maze(self, modal, *largs):
        self.setup_cells()
        self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 4 )]=1
        # self.draw_some_cells()
        modal.dismiss()

    def assign_gol(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -2 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y )]=1
        self.on_board[(self.mid_x ,self.mid_y )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y )]=1

        modal.dismiss()

    def assign_pulsar(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -6 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 6 )]=1

        modal.dismiss()

    def assign_gliders(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -11 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y )]=1

        modal.dismiss()

    def assign_imo_6(self, modal, *largs):
        self.setup_cells()
        # self.on_board[(self.mid_x+ 72 ,self.mid_y+ 56 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 9 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -11 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -10 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y- 1 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y- 1 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -13 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -12 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -14 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -15 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -14 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -15 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -14 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -15 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -14 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -15 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -16 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -17 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -18 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -19 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -23 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -23 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -24 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -24 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -25 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -25 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -26 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -26 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -31 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -31 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -32 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -32 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -33 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -33 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -34 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -34 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -30 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -29 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -28 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -27 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -26 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -25 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -24 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -23 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -23 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -24 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -25 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -26 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -31 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -32 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -33 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -34 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -34 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -33 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -32 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -31 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 30 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 31 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 31 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 30 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 18 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 19 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 20 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 21 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 22 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 23 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 24 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 25 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 26 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 27 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 22 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 23 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 24 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 25 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 26 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 27 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 29 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 30 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 31 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 31 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 31 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 31 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 30 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 30 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 30 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 1 )]=1

        modal.dismiss()

    def assign_omega(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x+ 1 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -9 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y -10 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -8 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -7 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -6 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -5 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -4 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -3 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y -1 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 0 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 1 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 2 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )]=1
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 4 )]=1
        self.on_board[(self.mid_x -8 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 5 )]=1
        self.on_board[(self.mid_x -7 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 6 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -5 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -6 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 7 )]=1
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -1 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -2 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -3 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x -4 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 8 )]=1
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )]=1

        modal.dismiss()
# Setup functions
    # Create all possible rectangles for the given window size
    def create_rectangles(self, *largs):
        self.rectangles_dict.clear()
        self.dimensions = (Window.width - 20, Window.height - 70)
        self.pos = (11,61)
        for x in range(0,self.dimensions[0]/10):
            for y in range(0,self.dimensions[1]/10):
                rect = Rectangle(pos=(self.x + x * 10, self.y + y *10), size=(9,9))
                self.rectangles_dict[x,y] = rect
    # set canvas_color, self.pos and cells midpoint
    def setup_cells(self, *largs):
        self.set_canvas_color()
        self.pos = (11,61)
        self.mid_x,self.mid_y = self.dimensions[0]/20, self.dimensions[1]/20
    # assigns color instruction to canvas.before
    def set_canvas_color(self, on_request=False, *largs):
        self.canvas.before.clear()
        if self.cellcol == 'Random':
            self.canvas.before.clear()
            self.canvas.before.add(Color(uniform(0.0,1.0),1,1,mode="hsv"))
        else:
            self.canvas.before.add(self.allcols[self.cellcol])
        if on_request:
            self.canvas.ask_update()
    # add the starting rectangles to the board
    def starting_cells(self, *largs):
        for x_y in self.on_board:
            self.canvas.add(self.rectangles_dict[x_y])
        self.should_draw = True
        self.accept_touches = True # Only first time matters
    # game logic for each iteration
    def get_cell_changes(self, *largs):
        for x in range(0,int(self.dimensions[0]/10)):
            for y in range(0,int(self.dimensions[1]/10)):
                over_x,over_y = (x + 1) % (self.dimensions[0]/10), (y + 1) % (self.dimensions[1]/10)
                bel_x, bel_y = (x - 1) % (self.dimensions[0]/10), (y - 1) % (self.dimensions[1]/10)
                alive_neighbors = self.on_board[bel_x,bel_y] + self.on_board[bel_x,y] + self.on_board[bel_x,over_y] + self.on_board[x,bel_y] + self.on_board[x,over_y] + self.on_board[over_x,bel_y] + self.on_board[over_x,y] + self.on_board[over_x,over_y]

                if self.on_board[x,y]:
                    if (int(self.lonely) >= alive_neighbors or alive_neighbors >= int(self.crowded)):
                        self.changes_dict[x,y] = 0
                    else:
                        pass
                else:
                    if alive_neighbors == int(self.birth):
                        self.changes_dict[x,y] = 1
                    else:
                        pass
    # loops through changes from ^^ and adds the rectangles
    def update_canvas_objects(self,*largs):
        for x_y in self.changes_dict:
            if self.changes_dict[x_y]:
                self.canvas.add(self.rectangles_dict[x_y])
                self.on_board[x_y] = 1
            else:
                self.canvas.remove(self.rectangles_dict[x_y])
                del self.on_board[x_y]
        self.changes_dict.clear()
    # Our start/step scheduled function
    def update_cells(self,*largs):
        # self.update_count += 1
        if self.cellcol == 'Random':
            self.set_canvas_color(on_request=True)
        self.get_cell_changes()
        self.update_canvas_objects()

    def start_interval(self, events, *largs):
        self.should_draw = False
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        events.append(Clock.schedule_interval(self.update_cells,float(self.speed)))

    def stop_interval(self, events, *largs):
        self.should_draw = True
        if len(events) > 0:
            events[-1].cancel()
            events.pop()

    def step(self, events, *largs):
        self.should_draw = True
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        Clock.schedule_once(self.update_cells, 1.0/60.0)

    def reset_interval(self, events, grid, modal, *largs):
        self.should_draw = False
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        self.on_board.clear()
        self.changes_dict.clear()
        grid.canvas.clear()
        self.canvas.clear()
        self.setup_cells()
        modal.open()

    # Touch Handlers
    # Add rectangles and positive values to on_board when the animation is stopped.
    # Add values to changes_dict otherwise, rects added on next iteration
    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
        # print (touch.pos), self.accept_touches
        pos_x = int(math.floor(pos_x / 10.0))
        pos_y = int(math.floor(pos_y / 10.0))
        in_bounds = (0 <= pos_x < (self.dimensions[0] / 10)) and (0 <= pos_y < (self.dimensions[1] / 10))
        # sign_x = "+" if pos_x - self.mid_x >= 0 else ""
        # sign_y = "+" if pos_y - self.mid_y >= 0 else ""
        # print "self.on_board[(self.mid_x" + sign_x, pos_x - self.mid_x,",self.mid_y"+sign_y,pos_y-self.mid_y,")]=1"
        if self.accept_touches and in_bounds:
            try:
                if not self.on_board[pos_x,pos_y]:
                    if self.should_draw:
                        self.on_board[pos_x,pos_y] = 1
                        self.canvas.add(self.rectangles_dict[pos_x,pos_y])
                    else:
                        self.changes_dict[(pos_x,pos_y)] = 1
            except KeyError:
                pass
        else:
            pass

    def on_touch_move(self, touch):
        self.mouse_positions.append(touch.pos)
        # print(touch.pos), self.accept_touches
        for pos in self.mouse_positions:
            pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
            pos_x = int(math.floor(pos_x / 10.0))
            pos_y = int(math.floor(pos_y / 10.0))

            in_bounds = (0 <= pos_x < (self.dimensions[0] / 10)) and (0 <= pos_y < (self.dimensions[1] / 10))

            # print "touch_move in bounds?", in_bounds
            # print "pos_x, pos_y", pos_x ,",",pos_y
            # print "canvas width and height", self.width, self.height
            # print "self.on_board[(", pos_x, ",",pos_y,")]=1"
            if self.accept_touches and in_bounds:
                try:
                    if not self.on_board[pos_x,pos_y]:
                        if self.should_draw:
                            self.on_board[pos_x,pos_y] = 1
                            self.canvas.add(self.rectangles_dict[pos_x,pos_y])
                        else:
                            self.changes_dict[(pos_x,pos_y)] = 1
                except KeyError:
                    pass
        self.mouse_positions = []

    def on_rotate(self):
        self.loadimg
        self.reset_interval

    def on_flip(self):
        self.loadimg
        self.reset_interval

    # Need to add some placement options...
    def place_option(self, events, *largs):
        pass

    def info(self, events, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        info1 = '''Rules:\n      If a cell has 0-1 neighbors, it dies.\n      If a cell has 4 or more neighbors, it dies.\n      If a cell has 2-3 neighbors, it survives.\n      If a space is surrounded by 3 neighbors, a cell is born.\n\n'''
        info2 = '''Controls:\n      Click or draw to add cells.\n       Modify the default rules and more in settings.\n'''
        info3 = '''\nCreated by:\n      Steven Lee-Kramer\n      Ryan O Schenck'''
        popup = Popup(title="John Conway's Game of Life", separator_height=0, title_size=titlesize,
            content=Label(text=''.join([info1,info2,info3]),font_size=mysize),
            size_hint=(.8, .8),title_align='center',)
        popup.open()

    def loadimg(self, events, *largs):
        content = Image(source='logo.png')
        popup = Popup(title='', content=content,
              auto_dismiss=False, separator_height=0,title_size=0, separator_color=[0.,0.,0.,0.], size=(Window.height,Window.width),
              # border=[20,20,20,20],
              background='black_thing.png',
              background_color=[0,0,0,1])
        content.bind(on_touch_down=popup.dismiss)
        popup.open()

class GameApp(App):
    events = []
    game_cells = None
    # seconds = 0
    def settings(self, events, *largs):
            self.open_settings()

    def build(self):
        self.settings_cls = SettingsWithSpinner
        self.config.items('initiate')
        self.use_kivy_settings = False

        # Delete this once finalized
        # if Window.width < 1334 and Window.height < 750:
        #     Window.size = (1334,750)



        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(Window.width, Window.height - 50), pos=(0,50))
        self.game_cells = cells = Cells(size=(Window.width - 20, Window.height - 70), pos=(11,61))

        board.add_widget(grid)
        board.add_widget(cells)
        cells.create_rectangles()

        Clock.schedule_once(cells.loadimg, 0)

        start_patterns = Popup(title="Select Start Pattern", size_hint=(0.3,0.8),title_align='center' ,pos_hint={'x':0.35,'top':0.95})
        start_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        start_layout.bind(minimum_height=start_layout.setter('height'))
        patt_blank = Button(text='Blank',size_hint_y=None, height=50,on_press=partial(cells.assign_blank, start_patterns))
        patt_random = Button(text='Random',size_hint_y=None, height=50,on_press=partial(cells.assign_random, start_patterns))
        patt_gun = Button(text='Gun',size_hint_y=None, height=50,on_press=partial(cells.assign_gun, start_patterns))
        patt_ten = Button(text='Ten',size_hint_y=None, height=50,on_press=partial(cells.assign_ten, start_patterns))
        patt_binary = Button(text='Binary',size_hint_y=None, height=50,on_press=partial(cells.assign_binary, start_patterns))
        patt_face = Button(text='Face',size_hint_y=None, height=50,on_press=partial(cells.assign_face, start_patterns))
        patt_gol = Button(text='GOL',size_hint_y=None, height=50,on_press=partial(cells.assign_gol, start_patterns))
        patt_pulsar = Button(text='Pulsar',size_hint_y=None, height=50,on_press=partial(cells.assign_pulsar, start_patterns))
        patt_gliders = Button(text='Gliders',size_hint_y=None, height=50,on_press=partial(cells.assign_gliders, start_patterns))
        patt_imo_6 = Button(text='IMO 6', size_hint_y=None, height=50,on_press=partial(cells.assign_imo_6, start_patterns))
        patt_omega = Button(text='Resistance', size_hint_y=None, height=50,on_press=partial(cells.assign_omega,start_patterns))
        patt_maze = Button(text='Maze', size_hint_y=None, height=50,on_press=partial(cells.assign_maze,start_patterns))


        patterns = [patt_imo_6, patt_omega, patt_blank, patt_gol,patt_random,patt_gun,patt_ten,patt_pulsar,patt_gliders,patt_face,patt_binary, patt_maze]
        for pattern in patterns:
            start_layout.add_widget(pattern)
        pattern_scroll = ScrollView(size_hint=(1, 1))
        pattern_scroll.add_widget(start_layout)
        start_patterns.add_widget(pattern_scroll)


        btn_start = Button(text='Start', on_press=partial(cells.start_interval, self.events), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_stop = Button(text='Stop', on_press=partial(cells.stop_interval, self.events), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_step = Button(text='Step', on_press=partial(cells.step, self.events), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_reset = Button(text='Reset',
                           on_press=partial(cells.reset_interval, self.events,grid,start_patterns), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_place = Button(text='Place', on_press=partial(cells.place_option, self.events), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        # dump(btn_place)
        btn_sett = Button(text='Options',on_press=partial(self.settings, self.events), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_info = Button(text='i',on_press=partial(cells.info, self.events), background_down='test_dn.png', background_normal='test.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_sett.bind(on_press=partial(cells.stop_interval, self.events))

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})
        board.bind(size=cells.create_rectangles)
        board.bind(size=partial(cells.reset_interval,self.events,grid,start_patterns))

        controls =[btn_start,btn_stop,btn_step,btn_reset,btn_place,btn_sett,btn_info]
        for btn in controls:
            buttons.add_widget(btn)

        # start_patterns.attach_on = board
        start_patterns.open()
        start_patterns.bind(on_dismiss=grid.draw_grid)
        start_patterns.bind(on_dismiss=cells.starting_cells)

        board.add_widget(buttons)

        return board

    def build_config(self, config):
        config.setdefaults('initiate', {
            'Speed': 0.05,
            'Lonely': 1,
            'Crowded': 4,
            'Born': 3,
            'Color': 'White',
            })
        config_file = self.get_application_config()
        config.read(config_file)
        for item in config._sections:
            for x in config._sections[item]:
                if x == 'speed':
                    Cells.speed = config._sections[item][x]
                if x == 'color':
                    Cells.cellcol = config._sections[item][x]
                if x == 'born':
                    Cells.birth = config._sections[item][x]
                if x == 'lonely':
                    Cells.lonely = config._sections[item][x]
                if x == 'crowded':
                    Cells.crowded = config._sections[item][x]

    def build_settings(self, settings):
        settings.add_json_panel('Game Settings', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if key == 'Speed':
            self.game_cells.speed = value
        if key == 'Color':
            self.game_cells.cellcol = value
            self.game_cells.set_canvas_color()
        if key == 'Born':
            self.game_cells.birth = value
        if key == 'Lonely':
            self.game_cells.lonely = value
        if key == 'Crowded':
            self.game_cells.crowded = value
        else:
            pass
        print config, section, key, value

if __name__ == '__main__':
    GameApp().run()
