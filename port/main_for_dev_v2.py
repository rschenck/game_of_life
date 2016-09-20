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

import random

import random
def round_down(num):
	return num - (num%10)

def dump(obj):
	for attr in dir(obj):
		print "obj.%s = %s" % (attr, getattr(obj, attr))
		pass

class MyPaintWidget(Widget):

	def on_touch_down(self, touch):
	    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
	    with self.canvas:
			Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			d = 30.
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
			touch.ud['line'] = Line(points=(touch.x, touch.y))

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]

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
		for cell in self.cells:
			self.cells[cell][2] == random.randint(0,1)
			if self.cells[cell][2] == 1:
				self.cells[cell][1].rgb = [1,1,1]
			else:
				self.cells[cell][1].rgb = [0,0,0]

class RootWidget(FloatLayout):

	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)

		self.add_widget(controls.sett)
		self.add_widget(controls.info)
		self.add_widget(controls.reset)
		self.add_widget(controls.start)
		self.add_widget(controls.stop)
		self.add_widget(controls.prsts)

		# Adds the area for the cells
		# theboard = board()
		# self.add_widget(theboard)


		# cells = theboard.drawGrid()
		# print cells
		# Clock.schedule_interval(theboard.update_cell, 0.5)



class MyApp(App):
	# dump(controls.start)

	def build(self):
		# dump(RootWidget)

		self.root = root = RootWidget()
		
		theboard = board()

		self.root.add_widget(theboard)

		cells = theboard.drawGrid()

		Clock.schedule_interval(theboard.update_cell, 0.2)

		return root




if __name__=="__main__":
	MyApp().run()