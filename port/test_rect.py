import kivy
from collections import defaultdict
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.clock import Clock
from kivy.graphics.instructions import InstructionGroup
from random import random, randint
from functools import partial
import math

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
        pass

class LotsRect(Widget):
    rect_dict = {}
    on_board = defaultdict(int)
    def draw_self(self, *largs):
        for x in range(Window.width / 10):
            for y in range(Window.height/ 10):
                rect = InstructionGroup()
                rect.add(Rectangle(size=(9,9), pos=(x*10,y*10)))
                self.rect_dict[x,y] = rect
                self.on_board[x,y] = 1
                self.canvas.add(rect)

        with self.canvas.before:
            Color(1,1,1,mode="rgb")


    def update_color(self, *largs):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(random(),random(),random(),mode="rgb")
        self.canvas.ask_update()

    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0], touch.pos[1]
        x = int(math.floor(pos_x / 10.0))
        y = int(math.floor(pos_y / 10.0))
        try:
            if self.on_board[x,y]:
                self.canvas.remove(self.rect_dict[x,y])
                del self.on_board[x,y]
            else:
                self.canvas.add(self.rect_dict[x,y])
                self.on_board[x,y] = 1

        except:
            pass

    def update_randomly(self, *largs):
        for i in range(1200):
            x,y = randint(0,132), randint(0,74)
            if self.on_board[x,y]:
                self.canvas.remove(self.rect_dict[x,y])
                del self.on_board[x,y]
            else:
                self.canvas.add(self.rect_dict[x,y])
                self.on_board[x,y] = 1

class MyApp(App):

    def build(self):
        Window.size = (1334,750)
        board = FloatLayout(size=(Window.width, Window.height))
        rectangle = LotsRect(size_hint=(1,1))
        board.add_widget(rectangle)
        rectangle.draw_self()
        button = Button(text="update color", on_press=rectangle.update_color, size_hint=(0.1,0.1), pos_hint={'x':0, 'y':0})
        board.add_widget(button)
        Clock.schedule_interval(rectangle.update_randomly,0.001)
        return board


if __name__ == '__main__':
    MyApp().run()
