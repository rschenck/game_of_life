from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.uix.settings import SettingsWithSidebar
from settings_options import settings_json
from random import randint
from functools import partial
import math

class Grid(Widget):
    def draw_grid(self, *largs):
        with self.canvas:
            Color(.5,.5,.5, mode='rgb')
            for x in range(10,self.width,10):
                Rectangle(pos=(x,self.y),size=(1,self.height))
            for y in range(self.y,self.height+self.y,10):
                Rectangle(pos=(self.x,y),size=(self.width,1))
            Rectangle(pos=(self.x,self.y),size=(10,self.height))
            Rectangle(pos=(self.x,self.y),size=(self.width,10))
            Rectangle(pos=(self.width-10,self.y),size=(10,self.height))
            Rectangle(pos=(self.x,self.y+self.height-10),size=(self.width,10))

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
                        x_coord = self.x + x * 10
                        y_coord = self.y + y * 10
                        Rectangle(pos=(x_coord,y_coord), size=(9,9))

    def update_cells(self, *largs):
        self.canvas.clear()
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,61)
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
        events.append(Clock.schedule_interval(self.update_cells,1.0/15.0))

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
        self.pos = (11,61)
        self.create_cells()
        self.draw_some_cells()

    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
        pos_x = int(math.floor(pos_x / 10.0))
        pos_y = int(math.floor(pos_y / 10.0))
        try:
            self.current[pos_x][pos_y] = 1
            with self.canvas:
                Color(1,1,1,mode='rgb')
                x_coord = self.x + pos_x * 10
                y_coord = self.y + pos_y * 10
                Rectangle(pos=(x_coord,y_coord), size=(9,9))
        except IndexError:
            pass

    def place_option(self, events, *largs):
        pass


class GameApp(App):
    events = []

    def settings(self, events, *largs):
            self.open_settings()

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.config.items('initiate')
        self.use_kivy_settings = False
        Window.size = (1334,750)

        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(board.width, board.height - 50), pos=(0,50))
        cells = Cells(size=(grid.width - 20, grid.height - 20), pos=(11,61))

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

        btn_place = Button(text='Place',
                           on_press=partial(cells.place_option, self.events))

        btn_sett = Button(text='Settings',
                           on_press=partial(self.settings, self.events))


        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})
        buttons.add_widget(btn_start)
        buttons.add_widget(btn_stop)
        buttons.add_widget(btn_step)
        buttons.add_widget(btn_reset)
        buttons.add_widget(btn_place)
        buttons.add_widget(btn_sett)

        board.add_widget(buttons)
        print Window.size
        return board

    def build_config(self, config):
        config.setdefaults('initiate', {
            'Speed': 0.1,
            'Lonely': 1,
            'Crowded': 4,
            'Lives1': 2,
            'Lives2': 3,
            'Born': 3,
            'Color': 'White',
            'GridColor': 'Grey',
            'Music': True,
            'Sound': True,
            })

    def build_settings(self, settings):
        settings.add_json_panel('Game Settings', self.config, data=settings_json)

if __name__ == '__main__':
    GameApp().run()
