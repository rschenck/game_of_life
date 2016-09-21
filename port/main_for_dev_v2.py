from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import *
from functionality import controls
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout

import random
import time

def round_down(num):
	return num - (num%10)

def dump(obj):
	for attr in dir(obj):
		print "obj.%s = %s" % (attr, getattr(obj, attr))
		pass

def song():
	sound = SoundLoader.load('img/emotion.wav')
	if sound:
		sound.loop = True
		sound.play()

class board(Widget):
	# sound = SoundLoader.load('img/emotion.wav')
	# if sound:
	# 	sound.loop = True
	# 	sound.play()

	cells = {}
	count = 0
	# gets the overall window.size of the screen
	screen = Window.size
	w, h = round_down(screen[0]),int(round_down(screen[1] * .8))
	# portion of screen dedicated to the widgets
	btns = int(round_down(screen[1] * .2))



	def drawGrid(self):
		with self.canvas:
			for xx in range(0,self.w-10,10):
				for yy in range(0,self.h,10):
					self.cells.update({(xx,yy):0})
					
					stat = random.randint(0,1)
					if stat == 1:
						self.color = Color(1,1,1)
					else:
						self.color = Color(0,0,0)
					self.rect = Rectangle(pos=(5+xx,int(self.btns/2.)+yy), size=(9,9))
					self.cells.update({(xx,yy):[self.rect,self.color,stat]})
		return self.cells

	def update_cell(self, *args):
		print "Passed"
		for cell in self.cells:
			self.cells[cell][2] == random.randint(0,1)
			if self.cells[cell][2] == 1:
				self.cells[cell][1].rgb = [1,1,1]
			else:
				self.cells[cell][1].rgb = [0,0,0]

class boardWidget(GridLayout):
	def __init__(self, **kwargs):
		super(boardWidget, self).__init__(**kwargs)
		# Set up grid size
		self.cols = 60
		self.rows = 40
		# Padding on all sides; Spacing between cells
		self.padding = 0
		self.spacing = [0,0]

		#necessary to properly position the grid in the window
		self.pos_hint = {'center_x':.5, 'center_y':.5}
		self.size_hint=(.99,.8)

		count = 0
		for i in range(0,self.cols*self.rows):
			btn = Button(background_normal='', background_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)), border = (0,0,0,0))
			btn.id = "%s" % (i)
			btn.stat = random.randint(0,1)
			
			# if btn.stat == 1:
				# btn.background_color = (1,1,1)

			self.add_widget(btn)



class RootWidget(FloatLayout):

	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)

		self.btns = [controls.sett, controls.info, controls.reset, controls.start, controls.stop, controls.prsts]
		for item in self.btns:
			self.add_widget(item)

		w = boardWidget()
		dump(w)
		self.add_widget(w)




class MyApp(App):

	def build(self):
		root = RootWidget()
		
		# song()

		return root


if __name__=="__main__":
	MyApp().run()