from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import *
from functionality import controls

import random
def round_down(num):
	return num - (num%10)

def dump(obj):
	for attr in dir(obj):
		print "obj.%s = %s" % (attr, getattr(obj, attr))
		pass

class myLayout(GridLayout):
	def __init__(self, **kwargs):
		super(myLayout, self).__init__(**kwargs)
		screen = Window.size

		self.cols = 5
		self.rows = 1
		btn = Button(text = "Click")
		btn2 = Button(text = "Click")
		btn3 = Button(text = "Click")
		myboard = board()
		btn.bind(on_press=self.clk)
		btn2.bind(on_press=self.clk)
		btn3.bind(on_press=self.clk)
		myboard.bind()

		self.add_widget(btn)
		self.add_widget(btn2)
		self.add_widget(btn3)
		self.add_widget(myboard)


	def clk(self, obj):
		print("Hello World!")

class cell(Widget):
	def __init__(self, **kwargs):
		self.status = 1

class MyApp(App):
	# dump(controls.start)

	def build(self):
		layout = FloatLayout()
		# layout.add_widget(Button(text='1'))
		# layout.add_widget(Button(text='2'))
		# layout.add_widget(Button(text='3',size_hint=(.1,.1),pos_hint={'x':.2,'y':.0},color=[1,0,0]))
		layout.add_widget(controls.sett)
		layout.add_widget(controls.reset)
		layout.add_widget(controls.start)
		layout.add_widget(controls.stop)
		return layout


if __name__=="__main__":
	MyApp().run()