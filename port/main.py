from kivy.app import App
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
from random import randint
from random import uniform
from functools import partial
import math

# def song(music):
#     sound = SoundLoader.load('img/emotion.wav')
#     if sound and music:
#         sound.loop = True
#         sound.play()

# def dump(obj):
#     for attr in dir(obj):
#         print "obj.%s = %s" % (attr, getattr(obj, attr))
#         pass


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
	'White': [1,1,1],
	'Grey': [0.5,0.5,0.5],
	'Blue': [0,0,1],
	'Green': [0,1,0],
	'Red': [1,0,0],
	'Random': [0,0,0]
	}
	# speed, cellcol, birth, lonely, crowded = .1, 'White', 3, 1, 4

	mid_x,mid_y = 0,0
	positions = []
	current = []
	nextRound = []
	def assign_random(self, modal, *largs):
	    self.create_cells(random=True)
	    # self.draw_some_cells()
	    modal.dismiss()


	def assign_blank(self, modal, *largs):
	    self.create_cells()
	    # self.draw_some_cells()
	    modal.dismiss()

	def assign_gun(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -20 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -20 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -19 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -19 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -12 ][self.mid_y ]=1
		self.current[self.mid_x -12 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -11 ][self.mid_y ]=1
		self.current[self.mid_x -11 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -10 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -10 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -4 ][self.mid_y -2 ]=1
		self.current[self.mid_x -4 ][self.mid_y -1 ]=1
		self.current[self.mid_x -4 ][self.mid_y ]=1
		self.current[self.mid_x -3 ][self.mid_y ]=1
		self.current[self.mid_x -2 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -9 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -8 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y -10 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y -8 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y -8 ]=1
		self.current[self.mid_x+ 14 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 14 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 15 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 15 ][self.mid_y -4 ]=1
		self.current[self.mid_x+ 15 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 15 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 15 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 16 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 17 ][self.mid_y -4 ]=1
		# self.draw_some_cells()
		modal.dismiss()

	def assign_ten(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -6 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -5 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -1 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 2 ]=1
		# self.draw_some_cells()
		modal.dismiss()

	def assign_binary(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -12 ][self.mid_y ]=1
		self.current[self.mid_x -12 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -12 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -12 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x -11 ][self.mid_y ]=1
		self.current[self.mid_x -11 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -11 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -11 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x -9 ][self.mid_y -2 ]=1
		self.current[self.mid_x -9 ][self.mid_y -1 ]=1
		self.current[self.mid_x -9 ][self.mid_y ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x -8 ][self.mid_y -3 ]=1
		self.current[self.mid_x -8 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -7 ][self.mid_y -3 ]=1
		self.current[self.mid_x -7 ][self.mid_y -2 ]=1
		self.current[self.mid_x -7 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -7 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -7 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -7 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -7 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x -7 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -5 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -5 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x -1 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x ][self.mid_y -3 ]=1
		self.current[self.mid_x ][self.mid_y -2 ]=1
		self.current[self.mid_x ][self.mid_y+ 1 ]=1
		self.current[self.mid_x ][self.mid_y+ 2 ]=1
		self.current[self.mid_x ][self.mid_y+ 3 ]=1
		self.current[self.mid_x ][self.mid_y+ 4 ]=1
		self.current[self.mid_x ][self.mid_y+ 7 ]=1
		self.current[self.mid_x ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 5 ]=1
		# self.draw_some_cells()
		modal.dismiss()

	def assign_face(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -5 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -5 ][self.mid_y+ 9 ]=1
		self.current[self.mid_x -5 ][self.mid_y+ 10 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x -2 ][self.mid_y -4 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 9 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 10 ]=1
		self.current[self.mid_x -1 ][self.mid_y -5 ]=1
		self.current[self.mid_x -1 ][self.mid_y -4 ]=1
		self.current[self.mid_x -1 ][self.mid_y -3 ]=1
		self.current[self.mid_x ][self.mid_y -6 ]=1
		self.current[self.mid_x ][self.mid_y -5 ]=1
		self.current[self.mid_x ][self.mid_y -3 ]=1
		self.current[self.mid_x ][self.mid_y -2 ]=1
		self.current[self.mid_x ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -7 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -6 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -7 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -6 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -7 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -6 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 9 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 10 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -7 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -6 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y -6 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 7 ]=1
		self.current[self.mid_x+ 5 ][self.mid_y+ 11 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y -5 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y -4 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y -3 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 9 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 10 ]=1
		self.current[self.mid_x+ 7 ][self.mid_y -4 ]=1
		# self.draw_some_cells()
		modal.dismiss()

	def assign_maze(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -3 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x ][self.mid_y+ 1 ]=1
		self.current[self.mid_x ][self.mid_y+ 5 ]=1
		self.current[self.mid_x ][self.mid_y+ 6 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 4 ]=1
		# self.draw_some_cells()
		modal.dismiss()

	def assign_pulsar(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -6 ][self.mid_y -2 ]=1
		self.current[self.mid_x -6 ][self.mid_y -1 ]=1
		self.current[self.mid_x -6 ][self.mid_y ]=1
		self.current[self.mid_x -6 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -6 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x -6 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x -4 ][self.mid_y -4 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -3 ][self.mid_y -4 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -2 ][self.mid_y -4 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x -2 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x -1 ][self.mid_y -2 ]=1
		self.current[self.mid_x -1 ][self.mid_y -1 ]=1
		self.current[self.mid_x -1 ][self.mid_y ]=1
		self.current[self.mid_x -1 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -1 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x -1 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y -4 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 2 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y -4 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 3 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y -4 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 3 ]=1
		self.current[self.mid_x+ 4 ][self.mid_y+ 8 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x+ 6 ][self.mid_y+ 6 ]=1
		# self.draw_some_cells()
		modal.dismiss()

	def assign_gliders(self, modal, *largs):
		self.create_cells()
		self.current[self.mid_x -11 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -10 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 4 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 5 ]=1
		self.current[self.mid_x -9 ][self.mid_y+ 6 ]=1
		self.current[self.mid_x -5 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 1 ]=1
		self.current[self.mid_x -4 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x -3 ][self.mid_y+ 2 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -2 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y -1 ]=1
		self.current[self.mid_x+ 1 ][self.mid_y ]=1
		self.current[self.mid_x+ 2 ][self.mid_y ]=1
		self.current[self.mid_x+ 3 ][self.mid_y ]=1
		# self.draw_some_cells()
		modal.dismiss()


	def create_cells(self, random=False,*largs):
		self.size = (Window.width - 20, Window.height - 70)
		self.pos = (11,61)
		for x in range(0,self.width/10):
		    row = []
		    empties = []
		    for y in range(0,self.height/10):
		        if random:
		            row.append(randint(0,1))
		        else:
		            row.append(0)
		        empties.append(0)
		    self.current.append(row)
		    self.nextRound.append(empties)
		self.mid_x,self.mid_y = len(self.current)/2, len(self.current[0])/2

	def draw_some_cells(self, *largs):
		# print "drawing some cells"
		# print "length of list: ", len(self.current)
		with self.canvas:
		# Initializes Color() Kivy object
			self.color = Color(self.allcols[self.cellcol])
			# Changes the Color() Kivy object depending what user selects
			self.color.rgb = self.allcols[self.cellcol]

			for x in range(len(self.current)):
				for y in range(len(self.current[x])):
					if self.current[x][y] == 1:
						# p_x = "+" if x-65 > 0 else ""
						# p_y = "+" if y-34 > 0 else ""
						# print "self.current[self.mid_x" + p_x,x-65,"][self.mid_y"+p_y,y-34,"]=1"
						x_coord = self.x + x * 10
						y_coord = self.y + y * 10
						if self.cellcol == 'Random':
						    self.color.rgb = [uniform(0.0,1.0),uniform(0.0,1.0),uniform(0.0,1.0)]
						Rectangle(pos=(x_coord,y_coord), size=(9,9))

	def update_cells(self, *largs):

	    self.canvas.clear()
	    self.size = (Window.width - 20, Window.height - 70)
	    self.pos = (11,61)
	    # print "new size and pos after clear(): ", self.size, self.pos
	    for x in range(len(self.current)):
	        for y in range(len(self.current[x])):

	            over_x = x + 1
	            if over_x == len(self.current):
	                over_x = 0
	            over_y = y + 1
	            if over_y == len(self.current[x]):
	                over_y = 0

	            alive_neighbors = self.current[x-1][y-1] + self.current[x-1][y] + self.current[x-1][over_y] + self.current[x][y-1] + self.current[x][over_y] + self.current[over_x][y-1] + self.current[over_x][y] + self.current[over_x][over_y]

	            if self.current[x][y] == 1:
	                if (int(self.lonely) >= alive_neighbors or alive_neighbors >= int(self.crowded)):
	                    self.nextRound[x][y] = 0
	                else:
	                    self.nextRound[x][y] = 1
	            elif self.current[x][y] == 0:
	                if alive_neighbors == int(self.birth):
	                    self.nextRound[x][y] = 1
	                else:
	                    self.nextRound[x][y] = 0

	    self.switch_lists()
	    self.draw_some_cells()

	def switch_lists(self,*largs):
	    holder = self.current
	    self.current = self.nextRound
	    # print holder == self.nextRound
	    self.nextRound = holder
	    # print holder == self.nextRound

	def start_interval(self, events, *largs):
	    if len(events) > 0:
	        events[-1].cancel()
	        events.pop()
	    events.append(Clock.schedule_interval(self.update_cells,float(self.speed)))

	def stop_interval(self, events, *largs):
	    if len(events) > 0:
	        events[-1].cancel()
	        events.pop()

	def step(self, events, *largs):
	    if len(events) > 0:
	        events[-1].cancel()
	        events.pop()
	    Clock.schedule_once(self.update_cells, 1.0/60.0)

	def reset_interval(self, events, grid, modal, *largs):
	    if len(events) > 0:
	        events[-1].cancel()
	        events.pop()
	    self.current = []
	    self.nextRound = []
	    grid.canvas.clear()
	    self.canvas.clear()
	    self.size = (Window.width - 20, Window.height - 70)
	    self.pos = (11,61)
	    # self.create_cells()
	    # self.draw_some_cells()
	    modal.open()

	def on_touch_down(self, touch):
	    pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
	    pos_x = int(math.floor(pos_x / 10.0))
	    pos_y = int(math.floor(pos_y / 10.0))
	    # print "self.current[", pos_x, "][",pos_y,"]=1"
	    try:
	        self.current[pos_x][pos_y] = 1
	        with self.canvas:
	            # Initializes Color() Kivy object
	            self.color = Color(self.allcols[self.cellcol])
	            # Changes the Color() Kivy object depending what user selects
	            self.color.rgb = self.allcols[self.cellcol]
	            x_coord = self.x + pos_x * 10
	            y_coord = self.y + pos_y * 10
	            Rectangle(pos=(x_coord,y_coord), size=(9,9))
	    except IndexError:
	        pass

	def on_touch_move(self, touch):
		self.positions.append(touch.pos)
		print(touch.pos)
		for pos in self.positions:
		    pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
		    pos_x = int(math.floor(pos_x / 10.0))
		    pos_y = int(math.floor(pos_y / 10.0))
		    # print "self.current[", pos_x, "][",pos_y,"]=1"
		    try:
		        self.current[pos_x][pos_y] = 1
		        with self.canvas:
		            # Initializes Color() Kivy object
		            self.color = Color(self.allcols[self.cellcol])
		            # Changes the Color() Kivy object depending what user selects
		            self.color.rgb = self.allcols[self.cellcol]
		            x_coord = self.x + pos_x * 10
		            y_coord = self.y + pos_y * 10
		            Rectangle(pos=(x_coord,y_coord), size=(9,9))
		    except IndexError:
		        pass
		self.positions = []

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

    def settings(self, events, *largs):
            self.open_settings()

    def build(self):
		self.settings_cls = SettingsWithSpinner
		self.config.items('initiate')
		self.use_kivy_settings = False
		# Window.size = (1334,750)

		# make layout and additional widgets
		board = FloatLayout(size=(Window.width, Window.height))
		grid = Grid(size_hint=(1, 0.93), pos=(0,50))
		cells = Cells(size_hint=(0.985,0.91), pos=(11,61))

		# generate cell lists
		# cells.create_cells()
		# add grid and cells to layout
		board.add_widget(grid)
		board.add_widget(cells)
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
		patt_maze = Button(text='Maze',on_press=partial(cells.assign_maze, start_patterns))
		patt_pulsar = Button(text='Pulsar',on_press=partial(cells.assign_pulsar, start_patterns))
		patt_gliders = Button(text='Gliders',on_press=partial(cells.assign_gliders, start_patterns))
		
		# add pattern buttons to the layout
		patterns = [patt_label, patt_blank,patt_random,patt_gun,patt_ten,patt_binary,patt_face,patt_maze,patt_pulsar,patt_gliders]
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
		start_patterns.bind(on_dismiss=cells.draw_some_cells)
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
		config.read('game.ini')
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
