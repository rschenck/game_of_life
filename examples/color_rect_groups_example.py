from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import *
from kivy.uix.widget import Widget
from functools import partial
from random import random, randint
from kivy.clock import Clock
from time import time

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
        pass

class Groupings(Widget):
    rectangles_dict = {}
    iterations = 0
    def create_rectangles(self, *largs):
        self.rectangles_dict.clear()
        self.dimensions = (Window.width - 20, Window.height - 120)
        self.pos = (11,61)
        for x in range(0,self.dimensions[0]/10):
            for y in range(0,self.dimensions[1]/10):
                color = Color(0,0,1,mode="hsv")
                rect = Rectangle(pos=(self.x + x * 10, self.y + y *10), size=(9,9))
                self.rectangles_dict[x,y] = {"rect": rect, "color": color}

    def draw_rectangles(self,*largs):
        for x_y in self.rectangles_dict:
            self.canvas.add(self.rectangles_dict[x_y]["color"])
            self.canvas.add(self.rectangles_dict[x_y]["rect"])

    def change_color(self, x_y, hue,*largs):
        self.rectangles_dict[x_y]['color'].hsv = hue

    def randomly_change_rects(self, *largs):
        then = time()

        for x_y in self.rectangles_dict:
            if randint(0,1):
                self.change_color(x_y,(random(),1,1))
        self.iterations += 1
        print time() - then

    def dump_one(self, *largs):
        dump(self.rectangles_dict[1,1]["color"])
class InstructionApp(App):
    events = []

    def schedule(self, fxn, time, *largs):
        if len(self.events) > 0:
            self.events[-1].cancel()
            self.events.pop()
        self.events.append(Clock.schedule_interval(fxn,float(time)))

    def unschedule(self,*largs):
        if len(self.events) > 0:
            self.events[-1].cancel()
            self.events.pop()

    def build(self):
        if Window.width < 1334 and Window.height < 750:
            Window.size = (1334,750)
        board = FloatLayout(size=(Window.width, Window.height))
        groupings = Groupings(size=(Window.width - 20, Window.height - 120), pos=(11,61))
        board.add_widget(groupings)
        groupings.create_rectangles()
        groupings.draw_rectangles()
        groupings.dump_one()
        button = Button(text="change 'em", on_press=partial(self.schedule, groupings.randomly_change_rects, 0.001), pos=(100,0),size_hint=(None,None), size=(150,45))
        button2 = Button(text="stop 'em'", on_press=self.unschedule, pos=(300,0),size_hint=(None,None), size=(150,45))
        board.add_widget(button)
        board.add_widget(button2)
        return board

if __name__ == '__main__':
    InstructionApp().run()
