from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.uix.settings import SettingsWithSidebar
from settings_options import settings_json
from kivy.core.audio import SoundLoader
from random import randint
from random import uniform
from functools import partial
import math

# def song(music):
#     sound = SoundLoader.load('img/emotion.wav')
#     if sound and music:
#         sound.loop = True
#         sound.play()

# def dump(obj):
#     for attr in dir(obj):
#         print "obj.%s = %s" % (attr, getattr(obj, attr))
#         pass


class Grid(Widget):


    def draw_grid(self, *largs):
        self.size = (Window.width, Window.height - 50)
        self.pos = (0,50)
        with self.canvas:
            Color(0.5,0.5,0.5, mode='rgb')
            for x in range(10,self.width,10):
                Rectangle(pos=(x,self.y),size=(1,self.height))
            for y in range(self.y,self.height+self.y,10):
                Rectangle(pos=(self.x,y),size=(self.width,1))
            Rectangle(pos=(self.x,self.y),size=(10,self.height))
            Rectangle(pos=(self.x,self.y),size=(self.width,10))
            Rectangle(pos=(self.width-10,self.y),size=(10,self.height))
            Rectangle(pos=(self.x,self.y+self.height-10),size=(self.width,10))

class Cells(Widget):
    allcols = {
    'White': [1,1,1],
    'Grey': [0.5,0.5,0.5],
    'Blue': [0,0,1],
    'Green': [0,1,0],
    'Red': [1,0,0],
    'Random': [0,0,0]
    }
    speed, cellcol, birth, lonely, crowded = .1, 'White', 3, 1, 4


    current = []
    nextRound = []
    def assign_random(self, modal, *largs):
        print "assign_random() caled"
        self.create_cells(random=True)
        self.draw_some_cells()
        modal.dismiss()


    def assign_blank(self, modal, *largs):
        print "assign_blank() caled"
        self.create_cells()
        self.draw_some_cells()
        modal.dismiss()

    def assign_gun(self, modal, *largs):
        print "assign_gun() caled"
        self.create_cells()
        self.current[ 62 ][ 34 ]=1
        self.current[ 61 ][ 34 ]=1
        self.current[ 61 ][ 33 ]=1
        self.current[ 61 ][ 32 ]=1
        self.current[ 63 ][ 33 ]=1
        self.current[ 54 ][ 34 ]=1
        self.current[ 53 ][ 34 ]=1
        self.current[ 53 ][ 35 ]=1
        self.current[ 54 ][ 36 ]=1
        self.current[ 55 ][ 36 ]=1
        self.current[ 55 ][ 35 ]=1
        self.current[ 46 ][ 35 ]=1
        self.current[ 45 ][ 35 ]=1
        self.current[ 45 ][ 36 ]=1
        self.current[ 46 ][ 36 ]=1
        self.current[ 67 ][ 37 ]=1
        self.current[ 67 ][ 36 ]=1
        self.current[ 68 ][ 36 ]=1
        self.current[ 68 ][ 38 ]=1
        self.current[ 69 ][ 38 ]=1
        self.current[ 69 ][ 37 ]=1
        self.current[ 79 ][ 38 ]=1
        self.current[ 79 ][ 37 ]=1
        self.current[ 80 ][ 37 ]=1
        self.current[ 80 ][ 38 ]=1
        self.current[ 80 ][ 31 ]=1
        self.current[ 80 ][ 30 ]=1
        self.current[ 80 ][ 29 ]=1
        self.current[ 81 ][ 31 ]=1
        self.current[ 82 ][ 30 ]=1
        self.current[ 69 ][ 26 ]=1
        self.current[ 69 ][ 25 ]=1
        self.current[ 70 ][ 26 ]=1
        self.current[ 71 ][ 26 ]=1
        self.current[ 70 ][ 24 ]=1
        self.draw_some_cells()
        # self.current[][]=1
        modal.dismiss()

    def assign_ten(self, modal, *largs):
        print "assign_ten() caled"
        self.create_cells()
        self.current[ 64 ][ 36 ]=1
        self.current[ 63 ][ 36 ]=1
        self.current[ 62 ][ 36 ]=1
        self.current[ 61 ][ 36 ]=1
        self.current[ 60 ][ 36 ]=1
        self.current[ 59 ][ 36 ]=1
        self.current[ 65 ][ 36 ]=1
        self.current[ 66 ][ 36 ]=1
        self.current[ 67 ][ 36 ]=1
        self.current[ 68 ][ 36 ]=1
        self.draw_some_cells()
        modal.dismiss()

    def assign_binary(self, modal, *largs):
        print "assign_binary() caled"
        self.create_cells()
        self.current[ 61 ][ 38 ]=1
        self.current[ 62 ][ 38 ]=1
        self.current[ 63 ][ 37 ]=1
        self.current[ 63 ][ 36 ]=1
        self.current[ 62 ][ 35 ]=1
        self.current[ 61 ][ 35 ]=1
        self.current[ 60 ][ 36 ]=1
        self.current[ 60 ][ 37 ]=1
        self.current[ 65 ][ 38 ]=1
        self.current[ 65 ][ 37 ]=1
        self.current[ 65 ][ 36 ]=1
        self.current[ 65 ][ 35 ]=1
        self.current[ 58 ][ 38 ]=1
        self.current[ 58 ][ 37 ]=1
        self.current[ 58 ][ 36 ]=1
        self.current[ 58 ][ 35 ]=1
        self.current[ 65 ][ 41 ]=1
        self.current[ 65 ][ 42 ]=1
        self.current[ 66 ][ 42 ]=1
        self.current[ 65 ][ 32 ]=1
        self.current[ 65 ][ 31 ]=1
        self.current[ 66 ][ 31 ]=1
        self.current[ 58 ][ 32 ]=1
        self.current[ 58 ][ 31 ]=1
        self.current[ 57 ][ 31 ]=1
        self.current[ 58 ][ 41 ]=1
        self.current[ 58 ][ 42 ]=1
        self.current[ 57 ][ 42 ]=1
        self.current[ 67 ][ 41 ]=1
        self.current[ 67 ][ 40 ]=1
        self.current[ 67 ][ 38 ]=1
        self.current[ 67 ][ 39 ]=1
        self.current[ 67 ][ 37 ]=1
        self.current[ 67 ][ 36 ]=1
        self.current[ 67 ][ 35 ]=1
        self.current[ 67 ][ 34 ]=1
        self.current[ 67 ][ 33 ]=1
        self.current[ 67 ][ 32 ]=1
        self.current[ 56 ][ 32 ]=1
        self.current[ 56 ][ 33 ]=1
        self.current[ 56 ][ 34 ]=1
        self.current[ 56 ][ 35 ]=1
        self.current[ 56 ][ 36 ]=1
        self.current[ 56 ][ 37 ]=1
        self.current[ 56 ][ 38 ]=1
        self.current[ 56 ][ 39 ]=1
        self.current[ 56 ][ 40 ]=1
        self.current[ 56 ][ 41 ]=1
        self.current[ 64 ][ 45 ]=1
        self.current[ 63 ][ 45 ]=1
        self.current[ 62 ][ 45 ]=1
        self.current[ 69 ][ 38 ]=1
        self.current[ 69 ][ 39 ]=1
        self.current[ 70 ][ 39 ]=1
        self.current[ 70 ][ 38 ]=1
        self.current[ 69 ][ 35 ]=1
        self.current[ 69 ][ 34 ]=1
        self.current[ 70 ][ 34 ]=1
        self.current[ 70 ][ 35 ]=1
        self.current[ 54 ][ 38 ]=1
        self.current[ 54 ][ 39 ]=1
        self.current[ 53 ][ 39 ]=1
        self.current[ 53 ][ 38 ]=1
        self.current[ 54 ][ 35 ]=1
        self.current[ 53 ][ 35 ]=1
        self.current[ 53 ][ 34 ]=1
        self.current[ 54 ][ 34 ]=1
        self.draw_some_cells()
        modal.dismiss()

    def assign_face(self, modal, *largs):
        print "assign_face() caled"
        self.create_cells()
        self.current[ 70 ][ 36 ]=1
        self.current[ 70 ][ 37 ]=1
        self.current[ 71 ][ 37 ]=1
        self.current[ 71 ][ 36 ]=1
        self.current[ 70 ][ 41 ]=1
        self.current[ 69 ][ 41 ]=1
        self.current[ 71 ][ 42 ]=1
        self.current[ 71 ][ 43 ]=1
        self.current[ 71 ][ 44 ]=1
        self.current[ 70 ][ 45 ]=1
        self.current[ 69 ][ 45 ]=1
        self.current[ 68 ][ 44 ]=1
        self.current[ 68 ][ 43 ]=1
        self.current[ 68 ][ 42 ]=1
        self.current[ 63 ][ 42 ]=1
        self.current[ 63 ][ 43 ]=1
        self.current[ 63 ][ 44 ]=1
        self.current[ 62 ][ 45 ]=1
        self.current[ 61 ][ 45 ]=1
        self.current[ 60 ][ 44 ]=1
        self.current[ 60 ][ 43 ]=1
        self.current[ 60 ][ 42 ]=1
        self.current[ 61 ][ 41 ]=1
        self.current[ 62 ][ 41 ]=1
        self.current[ 68 ][ 37 ]=1
        self.current[ 67 ][ 38 ]=1
        self.current[ 67 ][ 36 ]=1
        self.current[ 66 ][ 36 ]=1
        self.current[ 65 ][ 37 ]=1
        self.current[ 66 ][ 33 ]=1
        self.current[ 67 ][ 33 ]=1
        self.current[ 68 ][ 33 ]=1
        self.current[ 69 ][ 33 ]=1
        self.current[ 65 ][ 32 ]=1
        self.current[ 66 ][ 32 ]=1
        self.current[ 67 ][ 32 ]=1
        self.current[ 68 ][ 32 ]=1
        self.current[ 69 ][ 32 ]=1
        self.current[ 70 ][ 32 ]=1
        self.current[ 64 ][ 31 ]=1
        self.current[ 65 ][ 31 ]=1
        self.current[ 66 ][ 31 ]=1
        self.current[ 67 ][ 31 ]=1
        self.current[ 68 ][ 31 ]=1
        self.current[ 69 ][ 31 ]=1
        self.current[ 70 ][ 31 ]=1
        self.current[ 71 ][ 31 ]=1
        self.current[ 72 ][ 30 ]=1
        self.current[ 71 ][ 30 ]=1
        self.current[ 63 ][ 30 ]=1
        self.current[ 64 ][ 30 ]=1
        self.current[ 64 ][ 29 ]=1
        self.current[ 65 ][ 29 ]=1
        self.current[ 66 ][ 29 ]=1
        self.current[ 67 ][ 29 ]=1
        self.current[ 68 ][ 29 ]=1
        self.current[ 69 ][ 29 ]=1
        self.current[ 70 ][ 29 ]=1
        self.current[ 71 ][ 29 ]=1
        self.current[ 65 ][ 28 ]=1
        self.current[ 66 ][ 28 ]=1
        self.current[ 67 ][ 28 ]=1
        self.current[ 68 ][ 28 ]=1
        self.current[ 69 ][ 28 ]=1
        self.current[ 70 ][ 28 ]=1
        self.current[ 66 ][ 27 ]=1
        self.current[ 67 ][ 27 ]=1
        self.current[ 68 ][ 27 ]=1
        self.current[ 69 ][ 27 ]=1
        self.draw_some_cells()
        modal.dismiss()

    def assign_maze(self, modal, *largs):
        print "assign_maze() caled"
        self.create_cells()
        self.current[ 65 ][ 39 ]=1
        self.current[ 65 ][ 40 ]=1
        self.current[ 66 ][ 40 ]=1
        self.current[ 67 ][ 37 ]=1
        self.current[ 68 ][ 37 ]=1
        self.current[ 68 ][ 38 ]=1
        self.current[ 67 ][ 35 ]=1
        self.current[ 65 ][ 35 ]=1
        self.current[ 66 ][ 34 ]=1
        self.current[ 63 ][ 39 ]=1
        self.current[ 62 ][ 38 ]=1
        self.current[ 63 ][ 37 ]=1
        self.draw_some_cells()
        modal.dismiss()

    def assign_pulsar(self, modal, *largs):
        print "assign_pulsar() caled"
        self.create_cells()
        self.current[ 66 ][ 38 ]=1
        self.current[ 64 ][ 38 ]=1
        self.current[ 64 ][ 34 ]=1
        self.current[ 66 ][ 34 ]=1
        self.current[ 67 ][ 37 ]=1
        self.current[ 67 ][ 35 ]=1
        self.current[ 63 ][ 37 ]=1
        self.current[ 63 ][ 35 ]=1
        self.current[ 68 ][ 37 ]=1
        self.current[ 69 ][ 37 ]=1
        self.current[ 68 ][ 35 ]=1
        self.current[ 69 ][ 35 ]=1
        self.current[ 66 ][ 33 ]=1
        self.current[ 66 ][ 32 ]=1
        self.current[ 64 ][ 33 ]=1
        self.current[ 64 ][ 32 ]=1
        self.current[ 62 ][ 35 ]=1
        self.current[ 61 ][ 35 ]=1
        self.current[ 61 ][ 37 ]=1
        self.current[ 62 ][ 37 ]=1
        self.current[ 64 ][ 39 ]=1
        self.current[ 64 ][ 40 ]=1
        self.current[ 66 ][ 40 ]=1
        self.current[ 66 ][ 39 ]=1
        self.current[ 67 ][ 42 ]=1
        self.current[ 68 ][ 42 ]=1
        self.current[ 69 ][ 42 ]=1
        self.current[ 71 ][ 38 ]=1
        self.current[ 71 ][ 39 ]=1
        self.current[ 71 ][ 40 ]=1
        self.current[ 71 ][ 34 ]=1
        self.current[ 71 ][ 33 ]=1
        self.current[ 71 ][ 32 ]=1
        self.current[ 67 ][ 30 ]=1
        self.current[ 68 ][ 30 ]=1
        self.current[ 69 ][ 30 ]=1
        self.current[ 63 ][ 30 ]=1
        self.current[ 62 ][ 30 ]=1
        self.current[ 61 ][ 30 ]=1
        self.current[ 59 ][ 34 ]=1
        self.current[ 59 ][ 33 ]=1
        self.current[ 59 ][ 32 ]=1
        self.current[ 59 ][ 38 ]=1
        self.current[ 59 ][ 39 ]=1
        self.current[ 59 ][ 40 ]=1
        self.current[ 63 ][ 42 ]=1
        self.current[ 62 ][ 42 ]=1
        self.current[ 61 ][ 42 ]=1
        self.draw_some_cells()
        modal.dismiss()

    def assign_gliders(self, modal, *largs):
        print "assign_gliders() caled"
        self.create_cells()
        self.current[ 60 ][ 36 ]=1
        self.current[ 61 ][ 36 ]=1
        self.current[ 62 ][ 36 ]=1
        self.current[ 61 ][ 35 ]=1
        self.current[ 66 ][ 34 ]=1
        self.current[ 67 ][ 34 ]=1
        self.current[ 68 ][ 34 ]=1
        self.current[ 66 ][ 33 ]=1
        self.current[ 66 ][ 32 ]=1
        self.current[ 56 ][ 38 ]=1
        self.current[ 55 ][ 38 ]=1
        self.current[ 54 ][ 38 ]=1
        self.current[ 56 ][ 39 ]=1
        self.current[ 56 ][ 40 ]=1
        self.draw_some_cells()
        modal.dismiss()


    def create_cells(self, random=False,*largs):
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,61)
        print "create_cells() called, random = ", random
        print "size of cells: ", self.size
        for x in range(0,self.width/10):
            row = []
            empties = []
            for y in range(0,self.height/10):
                if random:
                    row.append(randint(0,1))
                else:
                    row.append(0)
                empties.append(0)
            self.current.append(row)
            self.nextRound.append(empties)


    def draw_some_cells(self, *largs):
        # print "length of list: ", len(self.current)
        with self.canvas:
            # Initializes Color() Kivy object
            self.color = Color(self.allcols[self.cellcol])
            # Changes the Color() Kivy object depending what user selects
            self.color.rgb = self.allcols[self.cellcol]

            for x in range(len(self.current)):
                for y in range(len(self.current[x])):
                    if self.current[x][y] == 1:
                        x_coord = self.x + x * 10
                        y_coord = self.y + y * 10
                        if self.cellcol == 'Random':
                            self.color.rgb = [uniform(0.0,1.0),uniform(0.0,1.0),uniform(0.0,1.0)]
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
                    if (int(self.lonely) >= alive_neighbors or alive_neighbors >= int(self.crowded)):
                        self.nextRound[x][y] = 0
                    else:
                        self.nextRound[x][y] = 1
                elif self.current[x][y] == 0:
                    if alive_neighbors == int(self.birth):
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
        print
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        events.append(Clock.schedule_interval(self.update_cells,float(self.speed)))

    def stop_interval(self, events, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()

    def step(self, events, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        Clock.schedule_once(self.update_cells, 1.0/60.0)

    def reset_interval(self, events, grid, modal, *largs):
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        self.current = []
        self.nextRound = []
        grid.canvas.clear()
        self.canvas.clear()
        self.size = (Window.width - 20, Window.height - 70)
        self.pos = (11,61)
        # self.create_cells()
        # self.draw_some_cells()
        modal.open()

    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
        pos_x = int(math.floor(pos_x / 10.0))
        pos_y = int(math.floor(pos_y / 10.0))
        print "self.current[", pos_x, "][",pos_y,"]=1"
        try:
            self.current[pos_x][pos_y] = 1
            with self.canvas:
                # Initializes Color() Kivy object
                self.color = Color(self.allcols[self.cellcol])
                # Changes the Color() Kivy object depending what user selects
                self.color.rgb = self.allcols[self.cellcol]
                x_coord = self.x + pos_x * 10
                y_coord = self.y + pos_y * 10
                Rectangle(pos=(x_coord,y_coord), size=(9,9))
        except IndexError:
            pass

    def place_option(self, events, *largs):
        pass

    def info(self, events, *largs):
        pass

class GameApp(App):
    events = []

    def settings(self, events, *largs):
            self.open_settings()

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.config.items('initiate')
        self.use_kivy_settings = False
        # Window.size = (1334,750)

        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size_hint=(1, 0.93), pos=(0,50))
        cells = Cells(size_hint=(0.985,0.91), pos=(11,61))

        # generate cell lists
        # cells.create_cells()
        # add grid and cells to layout
        board.add_widget(grid)
        board.add_widget(cells)
        # draw grid and initial cells
        # grid.draw_grid()
        # cells.draw_some_cells()
        # schedule the updating of cells
        start_patterns = ModalView(size_hint=(0.3,0.8), pos_hint={'top': 0.95}, auto_dismiss=False)
        start_layout = BoxLayout(size_hint=(1,1), orientation='vertical')
        patt_label = Label(text='Select Start Pattern', pos=(200,200), font_size='25sp')
        patt_blank = Button(text='Blank',on_press=partial(cells.assign_blank, start_patterns))
        patt_random = Button(text='Random',on_press=partial(cells.assign_random, start_patterns))
        patt_gun = Button(text='Gun',on_press=partial(cells.assign_gun, start_patterns))
        patt_ten = Button(text='Ten',on_press=partial(cells.assign_ten, start_patterns))
        patt_binary = Button(text='Binary',on_press=partial(cells.assign_binary, start_patterns))
        patt_face = Button(text='Face',on_press=partial(cells.assign_face, start_patterns))
        patt_maze = Button(text='Maze',on_press=partial(cells.assign_maze, start_patterns))
        patt_pulsar = Button(text='Pulsar',on_press=partial(cells.assign_pulsar, start_patterns))
        patt_gliders = Button(text='Gliders',on_press=partial(cells.assign_gliders, start_patterns))
		# add pattern buttons to the layout
		start_layout.add_widget(patt_label)
        start_layout.add_widget(patt_blank)
        start_layout.add_widget(patt_random)
        start_layout.add_widget(patt_gun)
        start_layout.add_widget(patt_ten)
        start_layout.add_widget(patt_binary)
        start_layout.add_widget(patt_face)
        start_layout.add_widget(patt_maze)
        start_layout.add_widget(patt_pulsar)
        start_layout.add_widget(patt_gliders)
        start_patterns.add_widget(start_layout)

        btn_start = Button(text='Start', on_press=partial(cells.start_interval, self.events))
        btn_stop = Button(text='Stop', on_press=partial(cells.stop_interval, self.events))
        btn_step = Button(text='Step', on_press=partial(cells.step, self.events))
        btn_reset = Button(text='Reset',
                           on_press=partial(cells.reset_interval, self.events,grid,start_patterns))
        btn_place = Button(text='Place', on_press=partial(cells.place_option, self.events))
        btn_sett = Button(text='Settings',on_press=partial(self.settings, self.events))
        btn_sett.size_hint = (.6,1)
        btn_info = Button(text='info',on_press=partial(cells.info, self.events))
        btn_info.size_hint = (.6,1)

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})

        controls =[btn_start,btn_stop,btn_step,btn_reset,btn_place,btn_sett,btn_info]
        for btn in controls:
            buttons.add_widget(btn)

		start_patterns.attach_on = board
        start_patterns.open()
        start_patterns.bind(on_dismiss=grid.draw_grid)
        start_patterns.bind(on_dismiss=cells.draw_some_cells)
        board.add_widget(buttons)
        return board

    def build_config(self, config):
        config.setdefaults('initiate', {
            'Speed': 0.1,
            'Lonely': 1,
            'Crowded': 4,
            'Born': 3,
            'Color': 'White',
            'Music': True,
            'Sound': True,
            })

    def build_settings(self, settings):
        settings.add_json_panel('Game Settings', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if key == 'Speed':
            Cells.speed = value
        if key == 'Color':
            Cells.cellcol = value
        if key == 'Born':
            Cells.birth = value
        if key == 'Lonely':
            Cells.lonely = value
        else:
            pass
        print config, section, key, value

if __name__ == '__main__':
    GameApp().run()
