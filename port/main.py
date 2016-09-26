from kivy.app import App
from collections import defaultdict
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.uix.settings import SettingsWithSpinner
from settings_options import settings_json
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.graphics.instructions import InstructionGroup
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
# def dump(obj):
#     for attr in dir(obj):
#         print "obj.%s = %s" % (attr, getattr(obj, attr))
#         pass
#

class Grid(Widget):


    def draw_grid(self, *largs):
        self.size = (Window.width, Window.height - 50)
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
    rectangles_dict = {}
    on_board = defaultdict(int)
    changes_dict = {}
    mid_x,mid_y = 0,0
    mouse_positions = []
    should_draw = False
    first_touch = True
    def assign_random(self, modal, *largs):
        self.setup_cells()
        for x in range(0,self.width/10):
            for y in range(0,self.height/10):
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

    # def assign_maze(self, modal, *largs):
    #     self.setup_cells()
    #     self.on_board[(self.mid_x -3 ,self.mid_y+ 4 )]=1
    #     self.on_board[(self.mid_x -2 ,self.mid_y+ 3 )]=1
    #     self.on_board[(self.mid_x -2 ,self.mid_y+ 5 )]=1
    #     self.on_board[(self.mid_x ,self.mid_y+ 1 )]=1
    #     self.on_board[(self.mid_x ,self.mid_y+ 5 )]=1
    #     self.on_board[(self.mid_x ,self.mid_y+ 6 )]=1
    #     self.on_board[(self.mid_x+ 1 ,self.mid_y )]=1
    #     self.on_board[(self.mid_x+ 1 ,self.mid_y+ 6 )]=1
    #     self.on_board[(self.mid_x+ 2 ,self.mid_y+ 1 )]=1
    #     self.on_board[(self.mid_x+ 2 ,self.mid_y+ 3 )]=1
    #     self.on_board[(self.mid_x+ 3 ,self.mid_y+ 3 )]=1
    #     self.on_board[(self.mid_x+ 3 ,self.mid_y+ 4 )]=1
    #     # self.draw_some_cells()
    #     modal.dismiss()
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

    def create_rectangles(self, *largs):
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,61)
        for x in range(0,self.width/10):
            for y in range(0,self.height/10):
                rect = Rectangle(pos=(self.x + x * 10, self.y + y *10), size=(9,9))
                self.rectangles_dict[x,y] = rect

    def setup_cells(self, *largs):
        self.set_canvas_color()
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,61)
        self.mid_x,self.mid_y = self.width/20, self.height/20

    def set_canvas_color(self, on_request=False, *largs):
        self.canvas.before.clear()
        if self.cellcol == 'Random':
            self.canvas.before.clear()
            self.canvas.before.add(Color(uniform(0.0,1.0),uniform(0.0,1.0),uniform(0.0,1.0)))
        else:
            self.canvas.before.add(self.allcols[self.cellcol])
        if on_request:
            self.canvas.ask_update()

    def starting_cells(self, *largs):
        for x_y in self.on_board:
            self.canvas.add(self.rectangles_dict[x_y])
        self.should_draw = True


    def get_cell_changes(self, *largs):
        for x in range(0,int(self.width/10)):
            for y in range(0,int(self.height/10)):
                over_x,over_y = (x + 1) % (self.width/10), (y + 1) % (self.height/10)
                bel_x, bel_y = (x - 1) % (self.width/10), (y - 1) % (self.height/10)
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

    def update_canvas_objects(self,*largs):

        for x_y in self.changes_dict:
            if self.changes_dict[x_y]:
                self.canvas.add(self.rectangles_dict[x_y])
                self.on_board[x_y] = 1
            else:
                self.canvas.remove(self.rectangles_dict[x_y])
                del self.on_board[x_y]
        self.changes_dict.clear()

    def update_cells(self,*largs):
        # self.update_count += 1
        self.size = (Window.width - 20, Window.height - 70)
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

    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
        print(touch.pos)
        pos_x = int(math.floor(pos_x / 10.0))
        pos_y = int(math.floor(pos_y / 10.0))
        # sign_x = "+" if pos_x - self.mid_x > 0 else ""
        # sign_y = "+" if pos_y - self.mid_y > 0 else ""
        # print "self.on_board[(self.mid_x" + sign_x, pos_x - self.mid_x,",self.mid_y"+sign_y,pos_y-self.mid_y,")]=1"
        if not self.first_touch:
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
            self.first_touch = False

    def on_touch_move(self, touch):
        self.mouse_positions.append(touch.pos)
        print(touch.pos)
        for pos in self.mouse_positions:
            pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
            pos_x = int(math.floor(pos_x / 10.0))
            pos_y = int(math.floor(pos_y / 10.0))
            # print "self.on_board[(", pos_x, ",",pos_y,")]=1"
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

    def place_option(self, events, *largs):
        pass

    def info(self, events, *largs):
        info1 = '''Rules:\n\nFor a cell that is alive:\nIf a cell has 0-1 neighbors dies.\nIf a cell has 4 or more neighbors, it dies.\nIf a cell has 2-3 neighbors it survives\n\nFor an empty space:\nIf a space is surrounded by 3 neighbors, a cell is born.\n\n'''
        info2 = '''Controls:\n\nClick on an empty space to add a grid.\nModify the default rules or colors in settings.\nStop and start the simulation again for new settings to take effect.\n'''
        info3 = '''\nCreated by:\n\nSteven Lee-Kramer\nRyan O. Schenck'''
        popup = Popup(title="John Conway's Game of Life",
        content=Label(text=''.join([info1,info2,info3]),font_size=14),
        size_hint=(.7, .8), size=(400, 400),title_align='center')
        popup.open()

class GameApp(App):
    events = []
    # seconds = 0
    def settings(self, events, *largs):
            self.open_settings()

    def build(self):
        self.settings_cls = SettingsWithSpinner
        self.config.items('initiate')
        self.use_kivy_settings = False
        Window.size = (1334,750)

        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(Window.width, Window.height - 50), pos=(0,50))
        cells = Cells(size=(Window.width - 20, Window.height - 70), pos=(11,61))

        # generate cell lists
        # cells.create_cells()
        # add grid and cells to layout
        board.add_widget(grid)
        board.add_widget(cells)
        cells.create_rectangles()
        # draw grid and initial cells
        # grid.draw_grid()
        # cells.draw_some_cells()
        # schedule the updating of cells
        start_patterns = ModalView(size_hint=(0.3,0.8), pos_hint={'top': 0.95}, auto_dismiss=False)
        start_layout = BoxLayout(size_hint=(1,1), orientation='vertical')
        patt_label = Label(text='Select Start Pattern', pos=(200,200), font_size='18sp')
        patt_blank = Button(text='Blank',on_press=partial(cells.assign_blank, start_patterns))
        patt_random = Button(text='Random',on_press=partial(cells.assign_random, start_patterns))
        patt_gun = Button(text='Gun',on_press=partial(cells.assign_gun, start_patterns))
        patt_ten = Button(text='Ten',on_press=partial(cells.assign_ten, start_patterns))
        patt_binary = Button(text='Binary',on_press=partial(cells.assign_binary, start_patterns))
        patt_face = Button(text='Face',on_press=partial(cells.assign_face, start_patterns))
        patt_gol = Button(text='GOL',on_press=partial(cells.assign_gol, start_patterns))
        patt_pulsar = Button(text='Pulsar',on_press=partial(cells.assign_pulsar, start_patterns))
        patt_gliders = Button(text='Gliders',on_press=partial(cells.assign_gliders, start_patterns))

        patterns = [patt_label, patt_blank,patt_gol,patt_random,patt_gun,patt_binary,patt_face,patt_ten,patt_pulsar,patt_gliders]
        for pattern in patterns:
            start_layout.add_widget(pattern)
        start_patterns.add_widget(start_layout)

        btn_start = Button(text='Start', on_press=partial(cells.start_interval, self.events))
        btn_stop = Button(text='Stop', on_press=partial(cells.stop_interval, self.events))
        btn_step = Button(text='Step', on_press=partial(cells.step, self.events))
        btn_reset = Button(text='Reset',
                           on_press=partial(cells.reset_interval, self.events,grid,start_patterns))
        btn_place = Button(text='Place', on_press=partial(cells.place_option, self.events))
        btn_sett = Button(text='Options',on_press=partial(self.settings, self.events))
        # btn_sett.size_hint = (.6,1)
        btn_info = Button(text='i',on_press=partial(cells.info, self.events))
        # btn_info.size_hint = (.6,1)
        btn_sett.bind(on_press=partial(cells.stop_interval, self.events))

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})

        controls =[btn_start,btn_stop,btn_step,btn_reset,btn_place,btn_sett,btn_info]
        for btn in controls:
            buttons.add_widget(btn)

        start_patterns.attach_on = board
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
            Cells.speed = value
        if key == 'Color':
            Cells.cellcol = value
        if key == 'Born':
            Cells.birth = value
        if key == 'Lonely':
            Cells.lonely = value
        if key == 'Crowded':
            Cells.crowded = value
        else:
            pass
        print config, section, key, value

if __name__ == '__main__':
    GameApp().run()
