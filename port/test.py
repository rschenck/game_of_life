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
def round_down(num):
	return num - (num%10)

def dump(obj):
	for attr in dir(obj):
		print "obj.%s = %s" % (attr, getattr(obj, attr))
		pass

class RootWidget(FloatLayout):

	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)

		self.add_widget(controls.sett)
		self.add_widget(controls.info)
		self.add_widget(controls.reset)
		self.add_widget(controls.start)
		self.add_widget(controls.stop)
		self.add_widget(controls.prsts)



class MyApp(App):
	# dump(controls.start)

	def build(self):
		# dump(RootWidget)

		self.root = root = RootWidget()
		
				

		return root




if __name__=="__main__":
	MyApp().run()