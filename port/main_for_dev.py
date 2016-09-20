import kivy
from kivy.core.window import Window

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from functionality import controls
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
	sound = SoundLoader.load('img/emotion.wav')
	if sound:
		sound.loop = True
		sound.play()

	cells = {}
	count = 0
	screen = Window.size
	w, h = round_down(screen[0]),round_down(screen[1])

	def drawGrid(self):
		# screen = Window.size
		# w, h = round_down(screen[0]),round_down(screen[1])

		with self.canvas:
			for xx in range(0,self.w-10,10):
				for yy in range(0,self.h-100,10):
					self.cells.update({(xx,yy):0})
					
					stat = random.randint(0,1)
					self.color = Color(1,1,1)
					self.rect = Rectangle(pos=(5+xx,50+yy), size=(9,9))
					self.cells.update({(xx,yy):[self.rect,self.color,stat]})
		return self.cells

	def update_cell(self, *args):
		for cell in self.cells:
			self.cells[cell][2]=random.randint(0,1)
			if self.cells[cell][2] == 1:
				self.cells[cell][1].rgb = [1,1,1]
			else:
				self.cells[cell][1].rgb = [0,0,0]

	def on_touch_down(self, touch):
		xtouch = int(round_down(touch.x)-10)
		ytouch = int(round_down(touch.y)-50)
		sound = SoundLoader.load('img/button2.wav')
		if sound:
			sound.volume = 0.6
			sound.play()

		try: 
			self.cells[(xtouch,ytouch)][1].rgb = [1,0,0]
		except:
			pass

	def logic(self, *args):
		for cell in self.cells:
			alive = 0
			for xx in [-10,10,0]:
				for yy in [-10,10,0]:
					if (xx,yy) != (0,0):
						try:
							alive += self.cells[cell][2]
						except KeyError:
							pass
					else:
						pass

			if self.cells[cell][2] == 1:
				if alive < 2 or alive > 3:
					self.cells[cell][2] = 0
				else:
					self.cells[cell][2] = 1
			else:
				if alive == 3:
					self.cells[cell][2] = 1
					print self.cells[cell][2]



class mainGameApp(App):
	# Use this if you want to test different sizes of the window...
	# Right now it changes dynamically depending on the system.
	# Window.size = (1200,1200)
	
	def build(self):
		# self.layout = FloatLayout()
		# self.layout.add_widget(controls.start)
		cells = board()
		allcells = cells.drawGrid()
		
		#Figure out a way to allow the user to select the time frame (0->1)
		
		Clock.schedule_interval(cells.update_cell, 0.5)
		return cells

if __name__ == '__main__':
	mainGameApp().run()


