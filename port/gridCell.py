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

class board(Widget):
    # sound = SoundLoader.load('img/emotion.wav')
    # if sound:
    #     sound.loop = True
    #     sound.play()

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
        self.screen = Window.size
        self.w, self.h = self.screen[0],self.screen[1]
        self.cols = 20
        self.rows = 10
        self.padding = 5
        self.pos = (0,int(self.h*.1))
        
        for i in range(0,200):
            btn = Button(background_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
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

        # grid = boardWidget()
        # self.add_widget(grid)
        # Adds the area for the cells
        # theboard = board()
        # self.add_widget(theboard)


        # cells = theboard.drawGrid()
        # print cells




class MyApp(App):

    def build(self):
        '''Older version'''
        self.root = root = RootWidget()
        
        # test = RootWidget()

        # test.update_cell()

        return self.root

        '''New version?'''
        # self.layout = RootWidget()

        # theboard = board()

        # self.layout.add_widget(theboard)

        # cells = theboard.drawGrid()
        # theboard.update_cell()

        # Clock.schedule_interval(theboard.update_cell, 0.5)

        # return self.layout




if __name__=="__main__":
    MyApp().run()