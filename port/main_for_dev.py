import kivy
from kivy.core.window import Window

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.clock import Clock

import random

# Considerations for user end:
	# Allow user to toggle between the shapes being 'Ellipse' or 'Rectangle' or ??? (Kivy terminology)
	# Allow user to adjust the rules for cells to die, live, or become alive

def round_down(num):
	return num - (num%10)

def dump(obj):
	for attr in dir(obj):
		print "obj.%s = %s" % (attr, getattr(obj, attr))
		pass

class board(Widget):
	cells = {}
	count = 0

	def drawGrid(self):
		screen = Window.size
		w, h = round_down(screen[0]),round_down(screen[1])

		with self.canvas:
			for xx in range(0,w-10,10):
				for yy in range(0,h-100,10):
					self.cells.update({(xx,yy):0})
					#if random.randint(0,1) == 1:
					self.color = Color(1,1,1)
					self.rect = Rectangle(pos=(5+xx,50+yy), size=(9,9))
					self.cells.update({(xx,yy):[self.rect,self.color,0]})
		return self.cells

	def update_cell(self, *args):
		for cell in self.cells:
			if random.randint(0,1) == 1:
				self.cells[cell][1].rgb = [1,1,1]
			else:
				self.cells[cell][1].rgb = [0,0,0]


class mainGameApp(App):
	# Use this if you want to test different sizes of the window...
	# Right now it changes dynamically depending on the system.
	# Window.size = (1200,1200)
	
	def build(self):
		cells = board()
		allcells = cells.drawGrid()

		# Figure out a way to allow the user to select the time frame (0->1)
		Clock.schedule_interval(cells.update_cell, 0.1)
		return cells

if __name__ == '__main__':
	mainGameApp().run()


