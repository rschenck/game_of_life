from collections import defaultdict
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import *
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import dp
from kivy.properties import NumericProperty,BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingsWithSpinner, SettingOptions
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
import math
from random import randint
from random import uniform
from settings_options import settings_json


def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
        pass


class Grid(Widget):
    def draw_grid(self, *largs):
        self.size = (Window.width, Window.height - 100) # Should be fine to draw off window size
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
    def default_cells():
        return {'alive':0,'was':0}
    on_board = defaultdict(default_cells)
    changes_dict = {}
    mid_x,mid_y = 0,0
    mouse_positions = []
    should_draw = False # allows touches to add rectangles
    accept_touches = False # Avoid sticky cell from intial click/move
    alive_cell_instructions = InstructionGroup()
    alive_color_instruction = InstructionGroup()
    was_cell_instructions = InstructionGroup()
    was_cell_instructions.add(Color(0.25,0.25,0.25,mode='rgb'))
    all_activated = NumericProperty(0)
    a_d_ratio = NumericProperty(0)
    generations = NumericProperty(500)
    score = NumericProperty(0)
    game_over = False
    cell_count = NumericProperty(0)
    sound = SoundLoader.load('options_track.wav')
    mainsound = SoundLoader.load('main_track.wav')

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
                    self.on_board[x,y] = {'alive':1, 'was':0}
        modal.dismiss()

    def assign_blank(self, modal, *largs):
        self.setup_cells()
        self.music_control('main', True, True)
        modal.dismiss()

    def assign_gun(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -20 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -20 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 14 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 14 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 15 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 15 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 15 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 15 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 15 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 16 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 17 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.music_control('main', True, True)
        modal.dismiss()

    def assign_ten(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -6 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.music_control('main', True, True)
        modal.dismiss()

    def assign_binary(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -12 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

    def assign_face(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -5 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 11 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -4 )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

    def assign_maze(self, modal, *largs):
        self.setup_cells()
        self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        # self.draw_some_cells()
        self.music_control('main', True, True)
        modal.dismiss()

    def assign_gol(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -2 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

    def assign_pulsar(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -6 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

    def assign_gliders(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x -11 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

    def assign_imo_6(self, modal, *largs):
        self.setup_cells()
        # self.on_board[(self.mid_x+ 72 ,self.mid_y+ 56 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 9 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 11 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 10 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -11 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -10 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y- 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y- 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -13 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -12 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -14 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -15 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -14 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -15 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -14 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -15 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -14 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -15 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -16 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -17 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -18 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -19 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -23 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -23 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -24 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -24 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -25 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -25 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -26 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -26 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -31 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -31 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -32 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -32 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -33 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -33 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -34 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -34 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -30 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -29 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -28 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -27 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -26 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -25 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -24 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -23 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -23 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -24 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -25 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -26 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -31 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -32 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -33 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -34 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -34 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -33 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -32 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -31 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 30 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 31 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 31 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 30 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 18 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 19 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 20 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 21 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 22 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 23 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 24 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 25 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 26 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 27 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 22 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 23 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 24 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 25 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 26 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 27 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 28 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 29 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 30 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 31 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 31 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 31 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 31 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 30 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 30 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 30 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 22 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 23 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 24 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 25 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 26 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 27 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

    def assign_omega(self, modal, *largs):
        self.setup_cells()

        self.on_board[(self.mid_x+ 1 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -9 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y -10 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 8 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 7 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 6 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y -1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 0 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 1 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 2 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 3 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -9 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 4 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -8 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 5 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -7 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 6 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -5 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -6 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 4 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 5 ,self.mid_y+ 7 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 1 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 0 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -1 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -2 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -3 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x -4 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 2 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}
        self.on_board[(self.mid_x+ 3 ,self.mid_y+ 8 )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()

# Setup functions
    # Create all possible rectangles for the given window size
    def create_rectangles(self, *largs):
        self.rectangles_dict.clear()
        self.dimensions = (Window.width - 20, Window.height - 120)
        self.pos = (11,61)
        for x in range(0,self.dimensions[0]/10):
            for y in range(0,self.dimensions[1]/10):
                rect = Rectangle(pos=(self.x + x * 10, self.y + y *10), size=(9,9))
                self.rectangles_dict[x,y] = rect

    def add_instruction_groups(self, *largs):
        # self.canvas.add(self.alive_color_instruction)
        self.canvas.add(self.alive_cell_instructions)
        self.canvas.add(self.was_cell_instructions)

    # set canvas_color, self.pos and cells midpoint
    def setup_cells(self, *largs):
        self.set_canvas_color()
        self.pos = (11,61)
        self.mid_x,self.mid_y = self.dimensions[0]/20, self.dimensions[1]/20
    # assigns color instruction to canvas.before
    def set_canvas_color(self, on_request=False, *largs):
        self.canvas.before.clear()
        if self.cellcol == 'Random':
            self.canvas.before.add(Color(uniform(0.0,1.0),1,1,mode="hsv"))
        else:
            self.canvas.before.add(self.allcols[self.cellcol])
        if on_request:
            self.canvas.ask_update()
    # add the starting rectangles to the board
    def starting_cells(self, *largs):
        for x_y in self.on_board:
            self.alive_cell_instructions.add(self.rectangles_dict[x_y])
        self.should_draw = True
        self.accept_touches = True # Only first time matters
    # game logic for each iteration
    def get_cell_changes(self, *largs):
        for x in range(0,int(self.dimensions[0]/10)):
            for y in range(0,int(self.dimensions[1]/10)):
                over_x,over_y = (x + 1) % (self.dimensions[0]/10), (y + 1) % (self.dimensions[1]/10)
                bel_x, bel_y = (x - 1) % (self.dimensions[0]/10), (y - 1) % (self.dimensions[1]/10)
                alive_neighbors = self.on_board[bel_x,bel_y]['alive'] + self.on_board[bel_x,y]['alive'] + self.on_board[bel_x,over_y]['alive'] + self.on_board[x,bel_y]['alive'] + self.on_board[x,over_y]['alive'] + self.on_board[over_x,bel_y]['alive'] + self.on_board[over_x,y]['alive'] + self.on_board[over_x,over_y]['alive']

                if self.on_board[x,y]['alive']:
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
        plus, minus = 0,0
        for x_y in self.changes_dict:
            if self.changes_dict[x_y]:
                if self.on_board[x_y]['was']:
                    self.was_cell_instructions.remove(self.rectangles_dict[x_y])
                self.alive_cell_instructions.add(self.rectangles_dict[x_y])
                self.on_board[x_y]['alive'] = 1
                plus += 1
                self.cell_count += 1
            else:
                self.alive_cell_instructions.remove(self.rectangles_dict[x_y])
                self.was_cell_instructions.add(self.rectangles_dict[x_y])
                self.on_board[x_y] = {'alive':0,'was':1}
                minus += 1
                self.cell_count -= 1
        self.changes_dict.clear()
        self.all_activated += plus
        self.a_d_ratio += (plus - minus)
    # Our start/step scheduled function
    def update_cells(self,*largs):
        # self.update_count += 1
        if self.cellcol == 'Random':
            self.set_canvas_color(on_request=True)
        self.get_cell_changes()
        self.update_canvas_objects()
        self.generations -= 1

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

    def reset_interval(self, events, grid, modal,*largs):
        for x in largs:
            if type(x) == Popup:
                x.dismiss()
        self.should_draw = False
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        self.on_board.clear()
        self.changes_dict.clear()
        grid.canvas.clear()
        self.alive_cell_instructions.clear()
        self.was_cell_instructions.clear()
        self.was_cell_instructions.add(Color(0.25,0.25,0.25,mode='rgb'))
        self.setup_cells()
        self.game_over = False
        self.reset_counters()
        modal.open()
        self.music_control('options', True, True)

    def reset_counters(self):
        self.all_activated = 0
        self.a_d_ratio = 0
        self.generations = 500
        self.score = 0
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
        # print "self.on_board[(self.mid_x" + sign_x, pos_x - self.mid_x,",self.mid_y"+sign_y,pos_y-self.mid_y,")] = {'alive':1, 'was':0}"
        if self.accept_touches and in_bounds and self.a_d_ratio > 0:
        # if self.accept_touches and in_bounds:
            try:
                if not self.on_board[pos_x,pos_y]['alive']:
                    if self.should_draw:
                        self.on_board[pos_x,pos_y]['alive'] = 1
                        if self.on_board[pos_x,pos_y]['was']:
                            self.was_cell_instructions.remove(self.rectangles_dict[pos_x,pos_y])
                        self.alive_cell_instructions.add(self.rectangles_dict[pos_x,pos_y])
                    else:
                        self.changes_dict[(pos_x,pos_y)] = 1
                    self.a_d_ratio -= 1
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
            # print "self.on_board[(", pos_x, ",",pos_y,")] = {'alive':1, 'was':0}"
            if self.accept_touches and in_bounds and self.a_d_ratio > 0:
            # if self.accept_touches and in_bounds:
                try:
                    if not self.on_board[pos_x,pos_y]['alive']:
                        if self.should_draw:
                            self.on_board[pos_x,pos_y]['alive'] = 1
                            if self.on_board[pos_x,pos_y]['was']:
                                self.was_cell_instructions.remove(self.rectangles_dict[pos_x,pos_y])
                            self.alive_cell_instructions.add(self.rectangles_dict[pos_x,pos_y])
                        else:
                            self.changes_dict[(pos_x,pos_y)] = 1
                        self.a_d_ratio -= 1
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
            size_hint=(.8, .8),title_align='center')
        popup.bind(on_dismiss=partial(self.music_control, 'main', True, True))
        # self.stopmainmusic()
        self.music_control('options', True, True)
        popup.open()

    def loadimg(self, events, *largs):
        content = Image(source='IMO_GOL2.png')
        popup = Popup(title='', content=content,
              auto_dismiss=False, separator_height=0,title_size=0, separator_color=[0.,0.,0.,0.], size=(Window.height,Window.width),
              # border=[20,20,20,20],
              background='black_thing.png',
              background_color=[0,0,0,1])
        content.bind(on_touch_down=popup.dismiss)
        popup.open()

    def music_control(self, track, switch, on, *largs):
    	select = {'options':'options_track.wav','main':'main_track.wav','score':None}

    	if on == True and switch == False:
    		sound = SoundLoader.load(select[track])
    		global sound
    		sound.loop = True
    		sound.volume = 0.5
    		sound.play()
    	elif on == False and switch == False:
    		sound.stop()

    	if switch == True:
    		sound.stop()
    		sound.unload()
    		sound = None
    		sound = SoundLoader.load(select[track])
    		global sound
    		sound.loop = True
    		sound.volume = 0.5
    		sound.play()
    	

    # def stopmainmusic(self, *largs):
    #     self.mainsound.stop()

class score_frame(Widget):
    def draw_scorepad(self, *largs):
        # self.size = (Window.width/2., 50)
        # self.pos = (Window.width,Window.height-50)

        with self.canvas:
            border = Color(0.5,0.5,0.5, mode='rgb')
            Rect = Rectangle(size=((Window.width),50), pos=(0,Window.height-50))
            inner = Color(0,0,0,mode='rgb')
            Inner_rect = Rectangle(size=(Window.width/3.*2+50-10,50-5), pos=(Window.width/3.-50+5,Window.height-50))

class SettingScrollOptions(SettingOptions):

    def _create_popup(self, instance):
        content         = GridLayout(cols=1, spacing='5dp')
        scrollview      = ScrollView( do_scroll_x=False)
        scrollcontent   = GridLayout(cols=1,  spacing='5dp', size_hint=(1, None))
        scrollcontent.bind(minimum_height=scrollcontent.setter('height'))
        self.popup   = popup = Popup(content=content, title=self.title, title_align='center', size_hint=(0.5, 0.6),  auto_dismiss=False)

        popup.open()
        content.add_widget(Widget(size_hint_y=None, height=dp(2)))

        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid, height=dp(55), size_hint=(1, None))
            btn.bind(on_release=self._set_option)
            scrollcontent.add_widget(btn)

        scrollview.add_widget(scrollcontent)
        content.add_widget(scrollview)
        content.add_widget(Widget(size_hint=(1,0.02)))

        btn = Button(text='Cancel', size=(popup.width, dp(50)),size_hint=(0.9, None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

class GameApp(App):
    events = []
    game_cells = None
    # seconds = 0

    def update_score(self,cells,adratval, csval, placeval, *largs):
        csval.text = str(cells.all_activated + cells.a_d_ratio)
        adratval.text = str(cells.a_d_ratio)
        num = cells.a_d_ratio if cells.a_d_ratio > 0 else 0
        placeval.text = str(num)
    def update_game(self,cells,label,game_end,*largs):
        label.text = str(cells.generations)
        if cells.generations == 0 or cells.game_over:
            cells.stop_interval(self.events)
            game_end.open()

    def reset_labels(self, adratval, csval, genval, placeval, *largs):
        adratval.text = "--"
        csval.text = "--"
        genval.text = "1000"
        placeval.text = "100"

    def update_final_score_label(self, label, cells, *largs):
        label.text = "Final Score: " + str(cells.all_activated + cells.a_d_ratio)
    def settings(self, events, *largs):
            self.open_settings()

    def build(self):

        self.settings_cls = SettingsWithSpinner
        self.config.items('initiate')
        self.use_kivy_settings = False

        # Delete this once finalized
        if Window.width < 1334 and Window.height < 750:
            Window.size = (1334,750)



        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(Window.width, Window.height - 100), pos=(0,50))
        self.game_cells = cells = Cells(size=(Window.width - 20, Window.height - 120), pos=(11,61))

        board.add_widget(grid)
        board.add_widget(cells)
        cells.create_rectangles()
        cells.add_instruction_groups()
        Clock.schedule_once(cells.loadimg, 0)
        cells.music_control('options', False, True)

        start_patterns = Popup(title="Select Pattern", title_font='joystix', separator_height=0 ,size_hint=(0.3,0.8),title_align='center' ,pos_hint={'x':0.35,'top':0.95})
        start_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        start_layout.bind(minimum_height=start_layout.setter('height'))
        patt_blank = Button(text='THE GAME', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_blank, start_patterns))
        patt_random = Button(text='RANDOM', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_random, start_patterns))
        patt_gun = Button(text='GUN', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_gun, start_patterns))
        patt_ten = Button(text='TEN', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_ten, start_patterns))
        patt_binary = Button(text='BINARY', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_binary, start_patterns))
        patt_face = Button(text='FACE', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_face, start_patterns))
        patt_gol = Button(text='GOL', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_gol, start_patterns))
        patt_pulsar = Button(text='PULSAR', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.assign_pulsar, start_patterns))
        patt_gliders = Button(text='GLIDERS', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.assign_gliders, start_patterns))
        patt_imo_6 = Button(text='IMO 6', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.assign_imo_6, start_patterns))
        patt_omega = Button(text='RESISTANCE', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.assign_omega,start_patterns))
        patt_maze = Button(text='MAZE', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.assign_maze,start_patterns))


        patterns = [patt_blank, patt_imo_6, patt_omega, patt_gol,patt_random,patt_gun,patt_ten,patt_pulsar,patt_gliders,patt_face,patt_binary, patt_maze]
        for pattern in patterns:
            start_layout.add_widget(pattern)
        pattern_scroll = ScrollView(size_hint=(1, 1))
        pattern_scroll.add_widget(start_layout)
        start_patterns.add_widget(pattern_scroll)

        btn_start = Button(text='START', font_name='joystix' ,on_press=partial(cells.start_interval, self.events), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_stop = Button(text='Stop', font_name='joystix' ,on_press=partial(cells.stop_interval, self.events), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_step = Button(text='Step', font_name='joystix' ,on_press=partial(cells.step, self.events), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_reset = Button(text='Reset', font_name='joystix' ,
                           on_press=partial(cells.reset_interval, self.events,grid,start_patterns), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_place = Button(text='Place', font_name='joystix' , on_press=partial(cells.place_option, self.events), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        # dump(btn_place)
        btn_sett = Button(text='Options', font_name='joystix' ,on_press=partial(self.settings, self.events), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_info = Button(text='Info', font_name='joystix' ,on_press=partial(cells.info, self.events), background_down='bttn_dn.png', background_normal='btn_solid.png', border=[0,0,0,0], background_disabled_down='test_dn.png', background_disabled_normal='test.png')
        btn_sett.bind(on_press=partial(cells.stop_interval, self.events))

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})

        board.bind(size=cells.create_rectangles)
        board.bind(size=partial(cells.reset_interval,self.events,grid,start_patterns))

        controls =[btn_start,btn_stop,btn_step,btn_reset,btn_sett,btn_info]
        for btn in controls:
            buttons.add_widget(btn)

        # top_buttons = BoxLayout(size_hint=(.3,None), height=50, #pos_hint={'x':0, 'y': 0}, padding=[0,0,0,Window.height-25]
        #     pos=[0,Window.height-50])
        #
        # top_controls =[btn_sett,btn_info]
        # for btn in top_controls:
        #     top_buttons.add_widget(btn)

        # start_patterns.attach_on = board
        start_patterns.open()
        start_patterns.bind(on_dismiss=grid.draw_grid)
        start_patterns.bind(on_dismiss=cells.starting_cells)

        #attach the scorepad
        # scorepad = score_frame()
        # start_patterns.bind(on_dismiss=scorepad.draw_scorepad)
        # Clock.schedule_once(song(False), 3)
        # board.add_widget(scorepad)


        # Score Label Widgets
        top_buttons = BoxLayout(size_hint=(1,None), height=50, pos_hint={'x':0, 'y': 0}, padding=[0,0,0,Window.height-25], pos=[0,Window.height-50])
        hs = Button(text='High Score:', font_name='Roboto',  font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        hsval = Button(text='--', font_name='Roboto',  font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        cs = Button(text='Score:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        csval = Button(text='--', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        adrat = Button(text='A/D (+/-):', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        adratval = Button(text='--', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        place = Button(text='Spawns:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        placeval = Button(text='100', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        gen = Button(text='Gens:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        genval = Button(text='500', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])

        btns_top = [place, placeval, gen, genval, adrat, adratval, cs, csval, hs, hsval]
        for btn in btns_top:
            top_buttons.add_widget(btn)

        game_end = Popup(title="Game Over", title_font='joystix', separator_height=0, size_hint=(0.3,0.8),title_align='center' ,pos_hint={'x':0.35,'top':0.95})
        end_layout = GridLayout(cols=1, spacing=10, size_hint=(1,1))
        high_score_label = Label(text="High Score: 1000000", font_name='Roboto', font_size=24)
        final_score_label = Label(text=("Final Score: " + str(cells.score)), font_name='Roboto', font_size=24)
        play_again = Button(text="Play Again", font_name='joystix', on_press=partial(cells.reset_interval, self.events, grid, start_patterns, game_end))

        end_layout.add_widget(high_score_label)
        end_layout.add_widget(final_score_label)
        end_layout.add_widget(play_again)
        game_end.add_widget(end_layout)

        cells.bind(a_d_ratio=partial(self.update_score, cells, adratval, csval,placeval))
        cells.bind(generations=partial(self.update_game, cells, genval, game_end))
        start_patterns.bind(on_open=partial(self.reset_labels, adratval, csval, genval, placeval))
        game_end.bind(on_open=partial(self.update_final_score_label, final_score_label, cells))

        # board.add_widget(hs)
        # board.add_widget(cs)
        # board.add_widget(adrat)
        # board.add_widget(place)
        # board.add_widget(gen)


        board.add_widget(top_buttons)
        board.add_widget(buttons)
        return board

    def update(self,event):
        self.hs.text = randint(0,100)

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
        settings.register_type('scrolloptions', SettingScrollOptions)
        settings.add_json_panel('Game Settings', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if key == 'Speed':
            self.game_cells.speed = float(value)
        if key == 'Color':
            self.game_cells.cellcol = value
            self.game_cells.set_canvas_color()
        if key == 'Born':
            self.game_cells.birth = int(value)
        if key == 'Lonely':
            self.game_cells.lonely = int(value)
        if key == 'Crowded':
            self.game_cells.crowded = int(value)
        else:
            pass
        print config, section, key, value

if __name__ == '__main__':
    GameApp().run()
