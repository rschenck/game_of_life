from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import randint
from functools import partial

class Grid(Widget):
    def draw_grid(self, *largs):
        with self.canvas:
            Color(.5,.5,.5, mode='rgb')
            for x in range(10,self.width,10):
                Rectangle(pos=(x,0),size=(1,self.height))
            for y in range(10,self.height,10):
                Rectangle(pos=(0,y),size=(self.width,1))
            Rectangle(pos=(0,0),size=(10,self.height))
            Rectangle(pos=(0,0),size=(self.width,10))
            Rectangle(pos=(self.width-10,0),size=(10,self.height))
            Rectangle(pos=(0,self.height-10),size=(self.width,10))

class Cells(Widget):
    current = []
    nextRound = []
    def create_cells(self, *largs):
        for x in range(0,self.width/10):
            row = []
            empties = []
            for y in range(0,self.height/10):
                row.append(randint(0,1))
                empties.append(0)
            self.current.append(row)
            self.nextRound.append(empties)

    def draw_some_cells(self, *largs):
        # print "length of list: ", len(self.current)
        with self.canvas:
            Color(1,1,1, mode='rgb')
            for x in range(len(self.current)):
                for y in range(len(self.current[x])):
                    if self.current[x][y] == 1:
                        x_coord = 11 + x * 10
                        y_coord = 11 + y * 10
                        Rectangle(pos=(x_coord,y_coord), size=(9,9))

    def update_cells(self, *largs):
        self.canvas.clear()
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,11)
        # print "new size and pos after clear(): ", self.size, self.pos
        for x in range(len(self.current)):
            for y in range(len(self.current[x])):

                over_x = x + 1
                if over_x == len(self.current):
                    over_x = 0
                over_y = y + 1
                if over_y == len(self.current[x]):
                    over_y = 0

                alive_neighbors = self.current[x-1][y-1] + self.current[x-1][y] + self.current[x-1][over_y] + self.current[x][y-1] + self.current[x][over_y] + self.current[over_x][y-1] + self.current[over_x][y] + self.current[over_x][over_y]

                if self.current[x][y] == 1:
                    if (2 > alive_neighbors or alive_neighbors > 3):
                        self.nextRound[x][y] = 0
                    else:
                        self.nextRound[x][y] = 1
                elif self.current[x][y] == 0:
                    if alive_neighbors == 3:
                        self.nextRound[x][y] = 1
                    else:
                        self.nextRound[x][y] = 0

        self.switch_lists()
        self.draw_some_cells()

    def switch_lists(self,*largs):
        holder = self.current
        self.current = self.nextRound
        # print holder == self.nextRound
        self.nextRound = holder
        # print holder == self.nextRound

    def start_interval(self, events, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        events.append(Clock.schedule_interval(self.update_cells,1.0/30.0))

    def stop_interval(self, events, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()

    def step(self, events, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        Clock.schedule_once(self.update_cells, 1.0/60.0)

    def reset_interval(self, events, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        self.current = []
        self.nextRound = []
        self.canvas.clear()
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,11)
        self.create_cells()
        self.draw_some_cells()

class GameApp(App):
    events = []
    def draw_grid(self, wid,*largs):
        # print wid.height, wid.width, wid.size, wid.pos
        with wid.canvas:
            Color(.5,.5,.5, mode='rgb')
            for x in range(10,wid.width,10):
                Rectangle(pos=(x,0),size=(1,wid.height))
            for y in range(10,wid.height,10):
                Rectangle(pos=(0,y),size=(wid.width,1))
            Rectangle(pos=(0,0),size=(10,wid.height))
            Rectangle(pos=(0,0),size=(wid.width,10))
            Rectangle(pos=(wid.width-10,0),size=(10,wid.height))
            Rectangle(pos=(0,wid.height-10),size=(wid.width,10))

    def build(self):
        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(board.width, board.height - 50))
        cells = Cells(size=(grid.width - 20, grid.height - 20), pos=(11,11))

        # generate cell lists
        cells.create_cells()
        # add grid and cells to layout
        board.add_widget(grid)
        board.add_widget(cells)
        # draw grid and initial cells
        grid.draw_grid()
        cells.draw_some_cells()
        # schedule the updating of cells


        btn_start = Button(text='Start',
                            on_press=partial(cells.start_interval, self.events))

        btn_stop = Button(text='Stop',
                            on_press=partial(cells.stop_interval, self.events))

        btn_step = Button(text='Step',
                            on_press=partial(cells.step, self.events))

        btn_reset = Button(text='Reset',
                           on_press=partial(cells.reset_interval, self.events))

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'top':1})
        buttons.add_widget(btn_start)
        buttons.add_widget(btn_stop)
        buttons.add_widget(btn_step)
        buttons.add_widget(btn_reset)

        board.add_widget(buttons)
        return board

if __name__ == '__main__':
    GameApp().run()
