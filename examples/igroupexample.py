from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import *
from kivy.uix.widget import Widget
from functools import partial
from random import random

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
        pass

class Groupings(Widget):
    blue = InstructionGroup()
    blue_color = InstructionGroup()
    blue_instr = Color(0, 0, 1, 1)
    blue_color.add(blue_instr)
    blue.add(Rectangle(pos=(0,0), size=(100, 100)))

    green = InstructionGroup()
    green_color = InstructionGroup()
    green_instr = Color(0, 1, 0, 1)
    green_color.add(green_instr)
    green.add(Rectangle(pos=(100, 100), size=(100, 100)))

    def draw_groupings(self,*largs):
        self.canvas.add(self.green_color)
        self.canvas.add(self.green)
        self.canvas.add(self.blue_color)
        self.canvas.add(self.blue)

    def change_color(self, groupname, *largs):
        print "change_color() called"
        print "color:", groupname
        if groupname == 'blue':
            group,color = self.blue_color,self.blue_instr
        else:
            group,color = self.green_color,self.green_instr
        group.remove(color)
        color = Color(random(),1,1,mode='hsv')
        group.add(color)


class InstructionApp(App):

    def build(self):
        board = FloatLayout(size=(Window.width, Window.height))
        groupings = Groupings()
        board.add_widget(groupings)
        groupings.draw_groupings()
        button1 = Button(text="d blue", on_press=partial(groupings.change_color, 'blue'), pos=(0,400),size_hint=(None,None), size=(50,45))
        button2 = Button(text="d green", on_press=partial(groupings.change_color, 'green'), pos=(51,400),size_hint=(None,None), size=(50,45))
        board.add_widget(button1)
        board.add_widget(button2)
        return board

if __name__ == '__main__':
    InstructionApp().run()
