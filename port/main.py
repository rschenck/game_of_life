# coding: latin-1
from collections import defaultdict
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import *
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import dp
from kivy.properties import NumericProperty,BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingsWithSpinner, SettingOptions
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
import math
from os.path import join
from random import randint
from random import uniform
from settings_options import settings_json
from presets import presets

# def dump(obj):
#     for attr in dir(obj):
#         print "obj.%s = %s" % (attr, getattr(obj, attr))
#         pass
cellsize = 10
v_border = (0,0)
h_border = (0,0)
class Grid(Widget):
    def draw_grid(self, *largs):
        self.size = (Window.width, Window.height - 100) # Should be fine to draw off window size
        self.determine_grid(self.width,self.height)
        self.pos = (0,50)
        with self.canvas:
            Color(0.5,0.5,0.5, mode='rgb')
            for x in range(v_border[0],self.width,cellsize):
                Rectangle(pos=(x,self.y),size=(1,self.height))
            for y in range(self.y+h_border[0],self.height+self.y,cellsize):
                Rectangle(pos=(self.x,y),size=(self.width,1))
            Rectangle(pos=(self.x,self.y),size=(v_border[0],self.height))
            Rectangle(pos=(self.x,self.y),size=(self.width,h_border[0]))
            Rectangle(pos=(self.width-v_border[1],self.y),size=(v_border[1],self.height))
            Rectangle(pos=(self.x,self.y+self.height-h_border[1]),size=(self.width,h_border[1]))

    def determine_grid(self,width,height,*largs):
        global v_border, h_border, cellsize
        w_mult, h_mult = 80.,30.
        cellsize = int(width / w_mult)

        while (height / cellsize) < h_mult:
            cellsize -= 1
        cellsize = 10 if cellsize < 10 else cellsize
        v_w = (width - 20) % cellsize + 20
        h_w = (height - 20) % cellsize + 20
        v_border = (int(v_w / 2.),int((v_w + 1 ) / 2.))
        h_border = (int(h_w / 2.), int((h_w + 1) / 2.))


class Cells(Widget):
    allcols = {
    'White': (0,0,1),
    'Grey': (0,0,0.25),
    'Blue': (0.638888,1,1),
    'Green': (0.3333,1,1),
    'Black':(0,0,0),
    'Red': (1,1,1),
    'Orange': (0.06388,1,1),
    'Yellow': (.16666,1,1),
    'Pink': (0.872222,1,1),
    'Purple': (0.76111,.8,.7),
    'Cyan': (0.5,1,.9),
    'Stem': (0.80555,0.4,1)
    }

    speeds = {
    "Max Speed": 0.0,
    "Very Fast": 0.01,
    "Faster": 0.03,
    "Fast": 0.05,
    "Above Average": 0.07,
    "Average": 0.1,
    "Slow": 0.15,
    "Slower": 0.25,
    "Very Slow": 0.5,
    "Min Speed": 1.
    }
    dimensions = None # Use this instead of self.size, which resets each frame
    rectangles_dict = {}
    def default_cells():
        return {'alive':0,'was':0}
    on_board = defaultdict(default_cells)
    changes_dict = {}
    mid_x,mid_y = 0,0
    mouse_positions = []
    should_draw = False # allows touches to add rectangles
    accept_touches = False # Avoid sticky cell from intial click/move
    all_activated = NumericProperty(0)
    score = NumericProperty(0)
    # old_mech = NumericProperty(0)
    bonus_multiplier = 1
    spawn_count = NumericProperty(100)
    generations = NumericProperty(500)
    game_over = False
    active_cell_count = NumericProperty(0)
    game_mode = 0
    spawn_adder = NumericProperty(0)
    cell_color = (0,0,0)
    main_menu = None
    cellcount = 0
    game_over_message = "You've done better!"
    wrap = 0
    ever_was_alive = 0
    non_positive_gens = 10
    events = []
    stop_iteration = False
    prevent_update = False
    # Starting Patterns
    # Each will:
    # 1) call self.setup_cells() to make sure color, and midpoint are set
    # 2) Then assign values to self.on_board using midpoint value to center the patterns
    # 3) call modal.dismiss() --> triggers calls to grid.draw_grid and cells.starting_cells
    def assign_blank(self, modal, *largs):
        self.setup_cells()
        if modal:
            self.music_control('main', True, True)
            modal.dismiss()
        else:
            self.music_control('main', True, True)
            pass



    def place_pattern(self, modal, selection, *largs):
        self.setup_cells()

        if selection == 'blank':
            if modal:
                modal.dismiss()
            else:
                pass
        elif selection == 'random':
            for x_y in self.rectangles_dict:
                # assign 25% chance of life
                if randint(0,3) == 1:
                    self.on_board[x_y] = {'alive':1, 'was':0}
                    self.active_cell_count += 1
        else:
            for coor in presets[selection]:
                self.on_board[( self.mid_x + int(coor[0]), self.mid_y + int(coor[1]) )] = {'alive':1, 'was':0}
                self.active_cell_count += 1

        self.music_control('main', True, True)
        modal.dismiss()

    def place_viral_cells(self, *largs):
        for x_y in [(self.mid_x+15,self.mid_y+10),(self.mid_x+15,self.mid_y-10),(self.mid_x-15,self.mid_y+10),(self.mid_x-15,self.mid_y-10),(3,3),(3,self.dimensions[1]/cellsize -4),(self.dimensions[0]/cellsize-4,3),(self.dimensions[0]/cellsize-4,self.dimensions[1]/cellsize-4),(self.mid_x,self.mid_y)]:
            self.rectangles_dict[x_y]['color'].hsv = self.allcols["Red"]
            self.canvas.add(self.rectangles_dict[x_y]['color'])
            self.canvas.add(self.rectangles_dict[x_y]['rect'])
            self.on_board[x_y] = {'alive':-5}
            self.ever_was_alive += 1

    # Setup functions
    def determine_borders(self,*largs):
        width,height = Window.width, Window.height - 100
        global v_border, h_border, cellsize
        w_mult, h_mult = 80.,30.
        cellsize = int(width / w_mult)
        while (height / cellsize) < h_mult:
            cellsize -= 1
        cellsize = 10 if cellsize < 10 else cellsize
        v_w = (width - 20) % cellsize + 20
        h_w = (height - 20) % cellsize + 20
        v_border = (int(v_w / 2.),int((v_w + 1 )/ 2.))
        h_border = (int(h_w / 2.), int((h_w + 1)/2.))
    # Create all possible rectangles for the given window size
    def create_rectangles(self, *largs):
        self.cellcount = 0
        self.determine_borders()
        v_borders = v_border[0] + v_border[1]
        h_borders = h_border[0] + h_border[1]
        self.rectangles_dict.clear()
        self.dimensions = (Window.width - v_borders, Window.height - 100 - h_borders)
        self.pos = (v_border[0] + 1, h_border[0] + 51)
        cell_side = cellsize - 1
        for x in range(0,self.dimensions[0]/cellsize):
            for y in range(0,self.dimensions[1]/cellsize):
                rect = Rectangle(pos=(self.x + x * cellsize, self.y + y *cellsize), size=(cell_side,cell_side))
                color = Color(0,0,0,mode="hsv")
                self.rectangles_dict[x,y] = {"rect":rect,"color":color}
                self.cellcount += 1

    # set canvas_color, self.pos and cells midpoint
    def setup_cells(self, *largs):
        self.set_canvas_color()
        self.pos = (v_border[0] +1,h_border[0] +51)
        self.mid_x,self.mid_y = self.dimensions[0]/(2 * cellsize), self.dimensions[1]/(2 * cellsize)

    # assigns color instruction to canvas.before
    def set_canvas_color(self, on_request=False, *largs):
        if self.cellcol == 'Random':
            self.cell_color = (uniform(0.0,1.0),1,1)
        else:
            self.cell_color = self.allcols[self.cellcol]
        if on_request:
            self.canvas.ask_update()

    # add the starting rectangles to the board
    def starting_cells(self, *largs):
        for x_y in self.on_board:
            self.rectangles_dict[x_y]["color"].hsv = self.cell_color
            self.canvas.add(self.rectangles_dict[x_y]["color"])
            self.canvas.add(self.rectangles_dict[x_y]["rect"])
        if self.game_mode == 2:
            self.place_viral_cells()
        self.should_draw = True
        self.accept_touches = True # Only first time matters

    # game logic for each iteration
    def get_cell_changes(self, *largs):
        for x in range(0,int(self.dimensions[0]/cellsize)):
            for y in range(0,int(self.dimensions[1]/cellsize)):
                # With wrap-around
                if self.wrap:
                    over_x,over_y = (x + 1) % (self.dimensions[0]/cellsize), (y + 1) % (self.dimensions[1]/cellsize)
                    bel_x, bel_y = (x - 1) % (self.dimensions[0]/cellsize), (y - 1) % (self.dimensions[1]/cellsize)
                # w/o wrap-around
                else:
                    over_x,over_y = (x + 1) , (y + 1)
                    bel_x, bel_y = (x - 1) , (y - 1)

                alive_neighbors = self.on_board[bel_x,bel_y]['alive'] + self.on_board[bel_x,y]['alive'] + self.on_board[bel_x,over_y]['alive'] + self.on_board[x,bel_y]['alive'] + self.on_board[x,over_y]['alive'] + self.on_board[over_x,bel_y]['alive'] + self.on_board[over_x,y]['alive'] + self.on_board[over_x,over_y]['alive']

                if self.game_mode == 2:
                    self.mark_changes_survival(x,y,alive_neighbors)
                else:
                    self.mark_changes(x,y,alive_neighbors)

    def mark_changes(self,x,y,alive_neighbors,*largs):
        if self.on_board[x,y]['alive']:
            if (int(self.lonely) >= alive_neighbors or alive_neighbors >= int(self.crowded)):
                self.changes_dict[x,y] = 0
            else:
                pass
        else:
            if alive_neighbors == int(self.birth):
                self.changes_dict[x,y] = 1
            else:
                pass

    def mark_changes_survival(self,x,y,alive_neighbors,*largs):
        if self.on_board[x,y]['alive'] == 9:
            self.on_board[x,y]['survival'] -= 1
            if self.on_board[x,y]['survival'] == 0:
                self.changes_dict[x,y] = 0
        elif self.on_board[x,y]['alive'] == -5:
            if alive_neighbors >= 5:
                self.changes_dict[x,y] = 0
        elif self.on_board[x,y]['alive'] == 1:
            if alive_neighbors < 0:
                self.changes_dict[x,y] = -1
            elif alive_neighbors in [2,3] or alive_neighbors > 8:
                pass
            else:
                self.changes_dict[x,y] = 0
        else:
            if alive_neighbors == int(self.birth) or alive_neighbors > 8:
                self.changes_dict[x,y] = 1
            else:
                pass


    # loops through changes from ^^ and adds the rectangles
    def update_canvas_objects(self,*largs):
        last_active_cell_count = self.active_cell_count
        plus, minus = 0,0

        for x_y in self.changes_dict:
            if self.changes_dict[x_y]:
                self.rectangles_dict[x_y]["color"].hsv = self.cell_color
                if not self.on_board[x_y]['was']:
                    self.canvas.add(self.rectangles_dict[x_y]["color"])
                    self.canvas.add(self.rectangles_dict[x_y]["rect"])
                self.on_board[x_y]['alive'] = 1
                plus += 1
                self.active_cell_count += 1
            else:
                self.rectangles_dict[x_y]["color"].hsv = self.allcols["Grey"]
                self.on_board[x_y] = {'alive':0,'was':1}
                minus += 1
                self.active_cell_count -= 1
        self.all_activated += plus
        self.spawn_adder = self.all_activated / (1000)
        self.score += ((max(self.active_cell_count - last_active_cell_count,0) * 0.7) + (plus * 0.3)) * self.bonus_multiplier * 10

        if self.game_mode:
            self.check_game_over()
        self.changes_dict.clear()

    def update_canvas_survival(self,*largs):
        last_active_cell_count = self.active_cell_count
        plus = 0
        for x_y in self.changes_dict:
            if self.changes_dict[x_y] == 2:
                self.rectangles_dict[x_y]["color"].hsv = self.allcols["Stem"]
                self.on_board[x_y]['alive'] = 9
                self.on_board[x_y]['survival'] = 15
                plus += 1
                self.active_cell_count += 1
            elif self.changes_dict[x_y] == 1:
                self.rectangles_dict[x_y]["color"].hsv = self.cell_color
                self.on_board[x_y]['alive'] = 1
                plus += 1
                self.active_cell_count += 1
            elif self.changes_dict[x_y] == -1:
                self.rectangles_dict[x_y]["color"].hsv = self.allcols["Red"]
                self.on_board[x_y]['alive'] = -5
                self.on_board[x_y]['was'] = 1
                self.active_cell_count -= 1
            else:
                self.rectangles_dict[x_y]["color"].hsv = self.allcols["Grey"]
                self.on_board[x_y] = {'alive':0,'was':1}
                self.active_cell_count -= 1
            if not self.on_board[x_y]['was']:
                self.canvas.add(self.rectangles_dict[x_y]["color"])
                self.canvas.add(self.rectangles_dict[x_y]["rect"])
                self.spawn_count += 1
                self.ever_was_alive += 1
        if not (self.generations % 5):
            x_y = (randint(0,self.dimensions[0]/cellsize-1), randint(0,self.dimensions[1]/cellsize-1))
            while self.on_board[x_y]['alive'] == -5:
                x_y = (randint(0,self.dimensions[0]/cellsize-1), randint(0,self.dimensions[1]/cellsize-1))
            self.rectangles_dict[x_y]["color"].hsv = self.allcols["Red"]
            if self.on_board[x_y]['alive'] == 1:
                self.on_board[x_y]['was'] = 1
                self.active_cell_count -= 1
            self.on_board[x_y]['alive'] = -5
            if not self.on_board[x_y]['was']:
                self.canvas.add(self.rectangles_dict[x_y]["color"])
                self.canvas.add(self.rectangles_dict[x_y]["rect"])
                self.ever_was_alive += 1
        self.all_activated += plus
        self.spawn_adder = self.all_activated / (1000)
        bonus = self.bonus_multiplier * (int(self.active_cell_count > last_active_cell_count))
        self.score += 1 + bonus
        if self.active_cell_count <= last_active_cell_count:
            self.non_positive_gens -= 1
        else:
            self.non_positive_gens = 10
            if not self.stop_iteration:
                self.start_interval()
        if self.game_mode:
            self.check_game_over()
        self.changes_dict.clear()


    def check_game_over(self,*largs):
        if not bool(self.changes_dict) and not self.spawn_count:
            if self.generations > 0:
                self.game_over_message = "Out of moves!\nUse your spawns wisely."
                self.game_over = True
        if not self.active_cell_count:
            if self.spawn_count != 100 and self.generations > 0:
                self.game_over = True
                self.game_over_message = "All your cells are dead!\nTry placing cells in groups of 3 or more."
        if self.game_mode == 2:
            if self.non_positive_gens == 0:
                self.game_over = True
                self.game_over_message = "10 generations without population growth.\nYou must promote life!"

    # Our start/step scheduled function
    def update_cells(self,*largs):
        if self.prevent_update:
            self.prevent_update = False
        else:
            if self.cellcol == 'Random':
                self.set_canvas_color(on_request=True)
            self.get_cell_changes()
            if self.game_mode == 2:
                self.update_canvas_survival()
                if self.non_positive_gens < 5 and not self.stop_iteration:
                    self.step(1.)
            else:
                self.update_canvas_objects()
            self.update_counters()


    def add_spawns(self, *largs):
        if self.game_mode == 2:
            if self.ever_was_alive >= self.cellcount:
                self.spawn_count += 10
        else:
            self.spawn_count += 5

    def update_counters(self,*largs):
        if self.game_mode == 2:
            self.generations += 1
            if self.ever_was_alive >= self.cellcount:
                self.bonus_multiplier = self.generations / 500
            else:
                self.bonus_multiplier = 0
        else:
            if self.game_mode == 1:
                self.generations -= 1
            self.bonus_multiplier = 1 + (self.active_cell_count * 30000 / pow(self.cellcount,2))




    def start_interval(self, *largs):
        self.stop_iteration = False
        self.should_draw = False
        if len(self.events) > 0:
            self.events[-1].cancel()
            self.events.pop()
        self.events.append(Clock.schedule_interval(self.update_cells,self.speed))

    def stop_interval(self, *largs):
        self.stop_iteration = True
        self.prevent_update = True
        self.should_draw = True
        if len(self.events) > 0:
            self.events[-1].cancel()
            self.events.pop()

    def step(self, interval, from_button=False,*largs):
        if from_button:
            self.stop_iteration = True
            self.prevent_update = False
        self.should_draw = True
        if len(self.events) > 0:
            self.events[-1].cancel()
            self.events.pop()
        Clock.schedule_once(self.update_cells, interval)

    def reset_interval(self, grid, modal,*largs):
        for x in largs:
            if type(x) == Popup:
                x.dismiss()
        self.should_draw = False
        if len(self.events) > 0:
            self.events[-1].cancel()
            self.events.pop()
        self.on_board.clear()
        self.changes_dict.clear()
        grid.canvas.clear()
        self.canvas.clear()
        self.setup_cells()
        self.game_over = False
        self.stop_iteration = False
        self.prevent_update = False
        if modal:
            modal.open()
            self.game_mode = 0
        else:
            self.assign_blank(None)
            grid.draw_grid()
            self.starting_cells()


    def reset_counters(self):
        self.all_activated = 0
        self.active_cell_count = 0
        self.spawn_count = 100
        self.score = 0
        self.game_over_message = "You've done better!"
        self.spawn_adder = 0
        if self.game_mode == 2:
            self.generations = 1
            self.ever_was_alive = 0
            self.non_positive_gens = 10
        else:
            self.generations = 500
            self.bonus_multiplier = 1




    # Touch Handlers
    # Add rectangles and positive values to on_board when the animation is stopped.
    # Add values to changes_dict otherwise, rects added on next iteration
    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
        # print (touch.pos), self.accept_touches
        pos_x = int(pos_x / cellsize)
        pos_y = int(pos_y / cellsize)
        in_bounds = (0 <= pos_x < (self.dimensions[0] / cellsize)) and (0 <= pos_y < (self.dimensions[1] / cellsize))

        # print "self.on_board[(self.mid_x" + sign_x, pos_x - self.mid_x,",self.mid_y"+sign_y,pos_y-self.mid_y,")] = {'alive':1, 'was':0}"
        if self.accept_touches and in_bounds and self.spawn_count > 0:
            if self.game_mode == 2:
                self.handle_touch_survival(pos_x,pos_y)
            else:
                self.handle_touch(pos_x,pos_y)


    def on_touch_move(self, touch):
        self.mouse_positions.append(touch.pos)
        # print(touch.pos), self.accept_touches
        for pos in self.mouse_positions:
            pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
            pos_x = int(pos_x / cellsize)
            pos_y = int(pos_y / cellsize)

            in_bounds = (0 <= pos_x < (self.dimensions[0] / cellsize)) and (0 <= pos_y < (self.dimensions[1] / cellsize))

            # print "self.on_board[(", pos_x, ",",pos_y,")] = {'alive':1, 'was':0}"
            if self.accept_touches and in_bounds and self.spawn_count > 0:
                if self.game_mode == 2:
                    self.handle_touch_survival(pos_x,pos_y)
                else:
                    self.handle_touch(pos_x,pos_y)
        self.mouse_positions = []

    def handle_touch(self, pos_x,pos_y,*largs):
        try:
            if not self.on_board[pos_x,pos_y]['alive']:
                if self.should_draw:
                    self.on_board[pos_x,pos_y]['alive'] = 1
                    self.rectangles_dict[pos_x,pos_y]["color"].hsv = self.cell_color
                    self.active_cell_count += 1
                    if not self.on_board[pos_x,pos_y]['was']:
                        self.canvas.add(self.rectangles_dict[pos_x,pos_y]["color"])
                        self.canvas.add(self.rectangles_dict[pos_x,pos_y]["rect"])
                else:
                    self.changes_dict[(pos_x,pos_y)] = 1
                if self.game_mode:
                    self.spawn_count -= 1
        except KeyError:
            pass

    def handle_touch_survival(self,pos_x,pos_y,*largs):
        try:
            if self.on_board[pos_x,pos_y]['alive'] == -5 and self.spawn_count >= 5:
                if self.should_draw:
                    self.rectangles_dict[pos_x,pos_y]['color'].hsv = self.allcols["Grey"]
                    self.on_board[pos_x,pos_y] = {'alive':0,'was':1}
                else:
                    self.changes_dict[pos_x,pos_y] = 0
                self.spawn_count -= 5
            elif not self.on_board[pos_x,pos_y]['alive']:
                if self.should_draw:
                    if randint(0,30) == 30:
                        self.on_board[pos_x,pos_y]['alive'] = 9
                        self.on_board[pos_x,pos_y]['survival'] = 15
                        self.rectangles_dict[pos_x,pos_y]['color'].hsv = self.allcols['Stem']
                    else:
                        self.on_board[pos_x,pos_y]['alive'] = 1
                        self.rectangles_dict[pos_x,pos_y]["color"].hsv = self.cell_color
                    self.active_cell_count += 1
                    if 'was' not in self.on_board[pos_x,pos_y] or not self.on_board[pos_x,pos_y]['was']:
                        self.canvas.add(self.rectangles_dict[pos_x,pos_y]["color"])
                        self.canvas.add(self.rectangles_dict[pos_x,pos_y]["rect"])
                        self.ever_was_alive += 1
                else:
                    if randint(0,30) == 30:
                        self.changes_dict[(pos_x,pos_y)] = 2
                    else:
                        self.changes_dict[(pos_x,pos_y)] = 1

                self.spawn_count -= 1
        except KeyError:
            pass

    def on_rotate(self):
        self.loadimg
        self.reset_interval

    def on_flip(self):
        self.loadimg
        self.reset_interval

    def info(self, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        # info0 = '''Game modes:\n   Select Playground Mode or Game Mode.\n    The playground has unlimited cells!\n    Change the colors!\n    Change the rules!\n'''
        info1 = '''Rules:\n      If a cell has 0-1 neighbors, it dies.\n      If a cell has 4 or more neighbors, it dies.\n      If a cell has 2-3 neighbors, it survives.\n      If a space is surrounded by 3 neighbors, a cell is born.\n\n'''
        info2 = '''Controls:\n      Click or draw to add cells.\n      Modify the default rules and more in settings.\n'''
        info3 = '''\nCreated by:\n      Steven Lee-Kramer\n      Ryan O Schenck'''
        text_info = Label(text=''.join([info1,info2,info3]),font_size=mysize)

        content = BoxLayout()
        content.add_widget(Label(text=''.join([info1,info2,info3]),font_size=mysize))

        tutorial_btn = Button(text='Tutorial', size_hint_x=.2, size_hint_y=.1)
        # tutorial_btn.bind(on_press=self.tutorial_main)
        content.add_widget(tutorial_btn)

        popup = Popup(title="John Conway's Game of Life", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.8, .8),title_align='center',)
        tutorial_btn.bind(on_press=partial(self.tutorial_main, popup))
        popup.bind(on_dismiss=partial(self.music_control, 'main', True, True))
        self.music_control('options', True, True)
        popup.open()
        self.stop_interval()


    def tutorial_main(self, popup, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        try:
            popup.dismiss()
        except:
            pass


        self.main_menu.open()


        playground = '''Playground mode allows for infinite play, and rule customization!\n\nCompete in game mode against yourself or others on twitter!\n'''
        choose_mode = Label(text=playground, font_size=mysize)

        content = BoxLayout(pos_hint={'center':1,'center':1})
        content.add_widget(choose_mode)

        next_btn = Button(text='Next', size_hint_x=.2, size_hint_y=.25, font_size=mysize)

        content.add_widget(next_btn)

        popup = Popup(title="Main Menu", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.95, .45),title_align='center', auto_dismiss=False, background_color=[0,0,0,.2])
        next_btn.bind(on_press=self.main_menu.dismiss)
        next_btn.bind(on_release=partial(self.tutorial_bottom, popup))
        popup.open()

    def tutorial_bottom(self, popup, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        try:
            popup.dismiss()
        except:
            pass

        playground = '''Here you have the main controls\n\nStart, Stop, Step: Progress one generation, and Reset\n\nSettings will allow you to change the rules, but only in Playground Mode.\n'''
        choose_mode = Label(text=playground, font_size=mysize)

        content = BoxLayout()
        content.add_widget(choose_mode)

        next_btn = Button(text='Next', size_hint_x=.2, size_hint_y=.25, font_size=mysize)

        content.add_widget(next_btn)

        popup = Popup(title="Bottom Controls Bar", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.95, .45),title_align='center', auto_dismiss=False, opacity=1, background_color=[0,0,0,.2])
        # next_btn.bind(on_press=self.main_menu.dismiss)
        next_btn.bind(on_release=partial(popup.dismiss, popup))
        next_btn.bind(on_release=partial(self.tutorial_grid, popup))
        popup.open()

    def tutorial_grid(self, popup, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        try:
            popup.dismiss()
        except:
            pass

        playground = '''Click to add a single spawn.\n\nDrag your finger to add multiple spawns.\n\nYou can do this before or during play.\n\nBe aware , cells in clusters of fewer than 3 will die!\n'''
        choose_mode = Label(text=playground, font_size=mysize)

        content = BoxLayout()
        content.add_widget(choose_mode)

        next_btn = Button(text='Next', size_hint_x=.2, size_hint_y=.25, font_size=mysize)

        content.add_widget(next_btn)

        popup = Popup(title="Main play area", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.95, .45),title_align='center', auto_dismiss=False, opacity=1, background_color=[0,0,0,.2])
        # next_btn.bind(on_press=self.main_menu.dismiss)
        next_btn.bind(on_release=partial(popup.dismiss, popup))
        next_btn.bind(on_release=partial(self.tutorial_top, popup))
        popup.open()

    def tutorial_top(self, popup, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        try:
            popup.dismiss()
        except:
            pass

        playground = '''Use this area to track your stats in Game Mode.\n\nStart with 100 spawns.\n\nGain more spawns by activating cells!\n\nYour current Score, High Score, and game status will be displayed.\n'''
        choose_mode = Label(text=playground, font_size=mysize)

        content = BoxLayout()
        content.add_widget(choose_mode)

        next_btn = Button(text='Next', size_hint_x=.2, size_hint_y=.25, font_size=mysize)

        content.add_widget(next_btn)

        popup = Popup(title="Top Score Bar", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.95, .45),title_align='center', auto_dismiss=False, opacity=1, background_color=[0,0,0,.2])
        # next_btn.bind(on_press=self.main_menu.dismiss)
        next_btn.bind(on_release=partial(popup.dismiss, popup))
        next_btn.bind(on_release=partial(self.tutorial_score, popup))
        popup.open()

    def tutorial_score(self, popup, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        try:
            popup.dismiss()
        except:
            pass

        playground = '''There are two game play modes, Creation and Survival.\n\nCreation: find the best patterns to create life and gain points.\n\nBonus points awarded for having more alive cells.\n\nSurvival: Stay alive amidst a viral outbreak.\n\nBonus point awarded once all black spaces are gone.\n\nTake a screenshot when you're done and upload to twitter using #GOLapp\n'''
        choose_mode = Label(text=playground, font_size=mysize)

        content = BoxLayout()
        content.add_widget(choose_mode)

        next_btn = Button(text='Next', size_hint_x=.2, size_hint_y=.14993, font_size=mysize)

        content.add_widget(next_btn)

        popup = Popup(title="Game Mode", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.95, .75),title_align='center', auto_dismiss=False, opacity=1, background_color=[0,0,0,.2])
        # next_btn.bind(on_press=self.main_menu.dismiss)
        next_btn.bind(on_release=partial(popup.dismiss, popup))
        next_btn.bind(on_release=partial(self.tutorial_end, popup))
        popup.open()

    def tutorial_end(self, popup, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        try:
            popup.dismiss()
        except:
            pass

        playground = '''If you like it, go give us a 5 star rating!\n\nGo back through the tutorial by clicking info.\n'''
        choose_mode = Label(text=playground, font_size=mysize)

        content = BoxLayout()
        content.add_widget(choose_mode)

        next_btn = Button(text='Play', size_hint_x=.2, size_hint_y=.25, font_size=mysize)

        content.add_widget(next_btn)

        popup = Popup(title="Have Fun!", separator_height=0, title_size=titlesize,
            content=content, size_hint=(.7, .4),title_align='center', auto_dismiss=False, opacity=1, background_color=[0,0,0,.2])
        # next_btn.bind(on_press=self.main_menu.dismiss)
        next_btn.bind(on_release=partial(popup.dismiss, popup))
        next_btn.bind(on_press=partial(self.main_menu.open, popup))
        popup.open()

    def loadimg(self, first_timer, *largs):

        content = Image(source='IMO_GOL2.png')
        popup = Popup(title='', content=content,
              auto_dismiss=False, separator_height=0,title_size=0, separator_color=[0.,0.,0.,0.], size=(Window.height,Window.width),
              # border=[20,20,20,20],
              background='black_thing.png',
              background_color=[0,0,0,1])
        content.bind(on_touch_down=popup.dismiss)


        popup.bind(on_dismiss=partial(self.open_main_menu, first_timer))
        popup.open()

    def open_main_menu(self, first_timer ,*largs):
        if first_timer.exists('tutorial'):
            Clock.schedule_once(self.main_menu.open,0)
        else:
            first_timer.put('tutorial', done=True)
            Clock.schedule_once(self.tutorial_main,0)

    def stop_music(self, *largs):
        try:
            sound.stop()
        except:
            pass

    def music_control(self, track, switch, on, *largs):
        select = {'options':'options_track.wav','main':'main_track.wav','score':'score_track.wav'}

        if bool(int(self.music)):
            if on == True and switch == False:
                sound = SoundLoader.load(select[track])
                global sound
                sound.loop = True
                sound.volume = 0.5
                sound.play()
            elif on == False and switch == False:
                sound.stop()

            if switch == True:
                try:
                    sound.stop()
                    sound.unload()
                except:
                    pass
                sound = None
                sound = SoundLoader.load(select[track])
                global sound
                sound.loop = True
                sound.volume = 0.5
                sound.play()



class score_frame(Widget):
    def draw_scorepad(self, *largs):
        # self.size = (Window.width/2., 50)
        # self.pos = (Window.width,Window.height-50)

        with self.canvas:
            border = Color(0.5,0.5,0.5, mode='rgb')
            Rect = Rectangle(size=((Window.width),50), pos=(0,Window.height-50))
            inner = Color(0,0,0,mode='rgb')
            Inner_rect = Rectangle(size=(Window.width/3.*2+50-10,50-5), pos=(Window.width/3.-50+5,Window.height-50))

class SettingScrollOptions(SettingOptions):

    def _create_popup(self, instance):
        content         = GridLayout(cols=1, spacing='5dp')
        scrollview      = ScrollView( do_scroll_x=False)
        scrollcontent   = GridLayout(cols=1,  spacing='5dp', size_hint=(1, None))
        scrollcontent.bind(minimum_height=scrollcontent.setter('height'))
        self.popup   = popup = Popup(content=content, title=self.title, title_align='center', size_hint=(0.5, 0.6),  auto_dismiss=False)

        popup.open()
        content.add_widget(Widget(size_hint_y=None, height=dp(2)))

        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid, height=dp(55), size_hint=(1, None))
            btn.bind(on_release=self._set_option)
            scrollcontent.add_widget(btn)

        scrollview.add_widget(scrollcontent)
        content.add_widget(scrollview)
        content.add_widget(Widget(size_hint=(1,0.02)))

        btn = Button(text='Cancel', size=(popup.width, dp(50)),size_hint=(0.9, None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

class GameApp(App):
    game_cells = None
    highscore = 0
    blinky = None

    def on_pause(self, *largs):
        return True

    def on_resume(self, *largs):
        self.game_cells.reset_interval
        pass

    # seconds = 0
    def intWithCommas(self, x, *largs):
        # if type(x) not in [type(0), type(0L)]:
        #     raise TypeError("Parameter must be an integer.")
        if x < 0:
            return '-' + intWithCommas(-x)
        result = ''
        while x >= 1000:
            x, r = divmod(x, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (x, result)

    # def update_score(self,cells, cs, place, *largs):
    def update_game(self, cells, cs, place, gen, game_end, *largs):
        if cells.game_mode:
            if cells.game_mode == 1:
                gen.text = str(cells.generations)
            elif cells.game_mode == 2:
                gen.text = str(cells.non_positive_gens)
            place.text = str(cells.spawn_count)
        else:
            gen.text = '∞'
            place.text = '∞'
        cs.text = self.intWithCommas(self.game_cells.score)


        if cells.generations == 0 or cells.game_over:
            cells.stop_interval()
            cells.music_control('score', True, True)
            game_end.open()

    def reset_labels(self, csval, gen, genval, placeval, hsval, cells,*largs):
        csval.text = "--"
        self.highscore = 0
        if cells.game_mode:
            if cells.game_mode == 1:
                gen.text = "Gens:"
                genval.text = "500"
                if self.highscorejson.exists('creation'):
                    self.highscore = self.highscorejson.get('creation')['best']
            elif cells.game_mode == 2:
                gen.text = "- "+ u'\u2206'+"Population:"
                genval.text = "10"
                if self.highscorejson.exists('survival'):
                    self.highscore = self.highscorejson.get('survival')['best']
            placeval.text = "100"
        else:
            if self.highscorejson.exists('creation'):
                self.highscore = self.highscorejson.get('creation')['best']
            genval.text = '∞'
            placeval.text = '∞'
        hsval.text = str(self.intWithCommas(self.highscore))

    def update_score_labels(self, myobject, final_score_label, high_score_label,cells, *largs):
        self.blinky = Clock.schedule_interval(lambda a:self.colorit(myobject),0.3)

        # global blinky
        if self.game_cells.score > self.highscore:
            self.highscore = cells.score
            if self.game_cells.game_mode == 1:
                self.highscorejson.put('creation', best=self.game_cells.score)
            elif self.game_cells.game_mode == 2:
                self.highscorejson.put('survival', best=self.game_cells.score)
            high_score_display = str(self.intWithCommas(self.highscore)) + " New Record!!"
        else:
            high_score_display = cells.game_over_message
        high_score_label.text = high_score_display
        final_score_label.text = "Final Score: " + str(self.intWithCommas(self.game_cells.score))
# REMOVE THIS LINE TO GET RID OF HIGH SCORE = 0
        # self.highscorejson.put('highscore', best=0)
        # self.highscore = 0
    def clear_text(self, high_score_label, *largs):
        high_score_label.text = ""

    def close_modals(self, start_patterns, restart_game, *largs):
        try:
            start_patterns.dismiss()
        except:
            pass
        try:
            restart_game.dismiss()
        except:
            pass

    def trigger_game_mode(self, main_menu, cells, grid, csval, gen, genval, placeval, hsval,btn_sett,mode,*largs):
        btn_sett.background_down = 'btn_solid.png'
        btn_sett.text = "---"
        btn_sett.disabled = True
        self.game_cells.lonely = 1
        self.game_cells.crowded = 4
        self.game_cells.birth = 3
        self.game_cells.wrap = 0
        if mode == 1:
            self.game_cells.speed = 0.05
            self.game_cells.cellcol = self.config._sections['initiate']['color']
        elif mode == 2:
            self.game_cells.speed = 0.1
            self.game_cells.cellcol = 'Green'
        main_menu.dismiss()
        cells.game_over = False
        cells.game_mode = mode
        cells.reset_counters()

        self.reset_labels(csval, gen, genval, placeval, hsval, cells)
        cells.reset_interval(grid, None)

    def trigger_playground_mode(self, popup, start_patterns, grid, cells, placeval, gen, genval,btn_sett, *largs):
        btn_sett.background_down = 'bttn_dn.png'
        btn_sett.text = "Settings"
        btn_sett.disabled = False
        cells.reset_counters()
        for item in self.config._sections:
            for x in self.config._sections[item]:
                if x == 'wrap':
                    self.game_cells.wrap = int(self.config._sections[item][x])
                if x == 'speed':
                    self.game_cells.speed = self.game_cells.speeds[self.config._sections[item][x]]
                if x == 'born':
                    self.game_cells.birth = self.config._sections[item][x]
                if x == 'lonely':
                    self.game_cells.lonely = self.config._sections[item][x]
                if x == 'crowded':
                    self.game_cells.crowded = self.config._sections[item][x]
        popup.dismiss()
        gen.text = 'Gens:'
        placeval.text = '∞'
        genval.text = '∞'
        cells.reset_interval(grid, start_patterns)
    def restart_btn_action(self, grid, start_patterns, cells, restart_game, csval, gen,genval, placeval,hsval,*largs):
        restart_game.dismiss()
        cells.reset_counters()
        self.reset_labels(csval, gen,genval, placeval, hsval, cells)
        if cells.game_mode:
            cells.game_over = False
            cells.reset_interval(grid,None)
        else:
            cells.reset_interval(grid, start_patterns)

    def colorit(self, myobject, *largs):
        myobject.color = [randint(0,1),randint(0,1),randint(0,1),1]
        # print myobject.color

    def unscheduleit(self, myobject, *largs):
        Clock.unschedule(self.blinky)

    def open_popup(self, to_open, to_close,*largs):
        to_close.dismiss()
        to_open.open()

    def settings(self, *largs):
        if self.game_cells.game_mode:
            pass
        else:
            self.open_settings()

    def build(self):
        global cellsize
        self.settings_cls = SettingsWithSpinner
        # dump(self.settings_cls)
        self.config.items('initiate')
        self.use_kivy_settings = False
        data_dir = getattr(self, 'user_data_dir')
        self.highscorejson = JsonStore(join(data_dir, 'highscore.json'))

        self.firsttimer = JsonStore(join(data_dir, 'tutorial.json'))
        if self.highscorejson.exists('creation'):
            if 'creation' in self.highscorejson.get('creation'):
                self.highscore = self.highscorejson.get('creation')['best']
            else:
                self.highscore = 0

        # Delete this once finalized
        # if Window.width < 1334 and Window.height < 750:
        #     Window.size = (1334,750)

        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*4
            mysize = Window.size[1]/100.*3.4

        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(Window.width, Window.height - 100), pos=(0,50))
        self.game_cells = cells = Cells(size=(Window.width - 20, Window.height - 120), pos=(11,61))

        board.add_widget(grid)
        board.add_widget(cells)
        cells.create_rectangles()
        # cells.draw_rectangles()
        # cells.add_instruction_groups()
        Clock.schedule_once(partial(cells.loadimg,self.firsttimer), 0)

        usrgridnum = cells.cellcount / 1000.0


        if bool(int(self.game_cells.music)):
            cells.music_control('options', False, True)
        else:
            pass

# Main Menu Components
        main_menu = cells.main_menu = Popup(title="Main Menu", background='black_thing.png', title_font='joystix', title_size=60, separator_height=0, size_hint=(1,1), pos_hint={'center':0.5,'center':0.5}, title_align="center",auto_dismiss=False)
        main_menu_layout = GridLayout(cols=3, spacing=20, size_hint_y=.9, size_hint_x=.1)
        holda = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')
        holdb = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')
        holdc = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')
        hold1 = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')
        playground_btn = Button(text="Playground Mode",font_size=mysize, font_name='joystix')
        hold2 = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')
        hold3 = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')
        game_btn = Button(text="Game Mode", font_name='joystix', font_size=mysize, size_hint_x=.5)
        hold4 = Button(text='', background_normal='black_thing.png', background_down='black_thing.png')

        main_men_btns = [holda,holdb,holdc,hold1,playground_btn,hold2,hold3,game_btn,hold4]
        for btn in main_men_btns:
            main_menu_layout.add_widget(btn)
        main_menu.add_widget(main_menu_layout)

# Set start patterns and internal scrolling layout
        start_patterns = Popup(title="Select Pattern", title_size=32, background='black_thing.png', title_font='joystix', separator_height=0 ,size_hint=(0.5,0.8),title_align='center' ,pos_hint={'center':0.5,'center':0.50})
        start_layout = GridLayout(cols=1, spacing='5dp')
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

# Set up buttons to go inside the scrolling portion
        patt_blank = Button(text='BLANK', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'blank'))
        patt_random = Button(text='RANDOM', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'random'))
        patt_gun = Button(text='GUN', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'gun'))
        patt_ten = Button(text='TEN', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'ten'))
        patt_binary = Button(text='BINARY', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'binary'))
        patt_face = Button(text='FACE', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'face'))
        patt_gol = Button(text='GOL', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'gol'))
        patt_pulsar = Button(text='PULSAR', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'pulsar'))
        patt_gliders = Button(text='GLIDERS', font_name='joystix' ,size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'gliders'))
        patt_imo_6 = Button(text='IMO 6', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.place_pattern, start_patterns, 'imo_6'))
        patt_omega = Button(text='RESISTANCE', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.place_pattern,start_patterns, 'omega'))
        patt_maze = Button(text='MAZE', font_name='joystix' , size_hint_y=None, height=50,on_press=partial(cells.place_pattern,start_patterns, 'maze'))

# attach buttons to scrolling layout
        patterns = [patt_blank, patt_imo_6, patt_omega, patt_gol,patt_random,patt_gun,patt_ten,patt_pulsar,patt_gliders,patt_face,patt_binary, patt_maze]
        for pattern in patterns:
            scroll_layout.add_widget(pattern)
        pattern_scroll = ScrollView(size_hint=(1, 1))
        pattern_scroll.add_widget(scroll_layout)
        start_layout.add_widget(Widget(size_hint_y=None, height=dp(2)))
        start_layout.add_widget(pattern_scroll)
        start_layout.add_widget(Widget(size_hint_y=None, height=dp(2)))
        sp_main_menu_button = Button(text="Main Menu", font_name='joystix', on_press=main_menu.open, size_hint=(1,None), height=dp(45))
        sp_main_menu_button.bind(on_release=partial(cells.music_control, 'options', True, True))
        start_layout.add_widget(sp_main_menu_button)
        start_patterns.add_widget(start_layout)
# setup restart game mode popup

        restart_game = Popup(title="Reset", title_font='joystix', title_size=56, background='black_thing.png', separator_height=0 ,size_hint=(1,1),title_align='center' ,pos_hint={'center':0.5,'center':0})
        restart_game_layout = BoxLayout(orientation='vertical')

        button_container = GridLayout(cols=3, spacing='5dp', size=(50,50))
        restart_btn = Button(text="Restart", font_size=mysize, font_name='joystix', size_hint=(1,None),height=dp(100))
        cancel_main_box = BoxLayout(size_hint=(0.5,0.1), height=dp(55), pos_hint={'center':.5, 'center':.1}, orientation='horizontal')
        cancel_restart_button = Button(text="Cancel", font_size=mysize, font_name='joystix',on_press=restart_game.dismiss,size_hint=(1,None), height=dp(100))
        r_main_menu_button = Button(text="Main Menu", font_size=mysize, font_name='joystix',on_press=main_menu.open,size_hint=(1,None), height=dp(45))
        r_main_menu_button.bind(on_release=partial(cells.music_control, 'options', True, True))

        # restart_game_layout.add_widget(restart_game_label)
        cmb = [restart_btn, cancel_restart_button]
        for btn in cmb:
            cancel_main_box.add_widget(btn)

        r1 = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        r2 = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        r3 = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        r4 = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        ra = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        rb = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        rc = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        rd = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        re = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        rf = Button(text='',background_down='black_thing.png', background_normal='black_thing.png')
        bc = [ra, rb, rc, rd, re, rf, r1, cancel_main_box, r2, r3, r_main_menu_button, r4]
        for btn in bc:
            button_container.add_widget(btn)

        restart_game_layout.add_widget(button_container)
        restart_game.add_widget(restart_game_layout)


# game buttons
        btn_start = Button(text='START', font_name='joystix' ,on_press=cells.start_interval,  background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_stop = Button(text='Stop', font_name='joystix' ,on_press=cells.stop_interval,  background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_step = Button(text='Step', font_name='joystix' ,on_press=partial(cells.step,0.01),  background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_reset = Button(text='Reset', font_name='joystix' ,
                           on_press=restart_game.open,  background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_reset.bind(on_press=cells.stop_interval)

        btn_sett = Button(text='Settings', font_name='joystix' ,on_press=self.settings,  background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_info = Button(text='Info', font_name='joystix' ,on_press=cells.info,  background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_sett.bind(on_press=cells.stop_interval)

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})

        board.bind(size=cells.create_rectangles)
        board.bind(size=partial(cells.reset_interval,grid,main_menu))

        controls =[btn_start,btn_stop,btn_step,btn_reset,btn_sett,btn_info]
        for btn in controls:
            buttons.add_widget(btn)

        # Clock.schedule_once(main_menu.open,0.5)
        # event = Clock.schedule_once(main_menu.open)

        main_menu.bind(on_open=partial(self.close_modals, start_patterns, restart_game))
        start_patterns.bind(on_open=partial(self.close_modals, None, restart_game))
        start_patterns.bind(on_dismiss=grid.draw_grid)
        start_patterns.bind(on_dismiss=cells.starting_cells)


        # Score Label Widgets
        top_buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'top':1})

        hs = Button(text='High Score:', font_name='Roboto',  font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png', border=[0,0,0,0])
        hsval = Button(text=self.intWithCommas(int(self.highscore)), font_name='Roboto',  font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])
        cs = Button(text='Score:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])
        csval = Button(text='--', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])

        place = Button(text='Spawns:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])
        placeval = Button(text='100', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])
        gen = Button(text='Gens:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])
        genval = Button(text='500', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])
        usrgrid = Button(text='Grid: '+ str(round(usrgridnum,1)), font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', background_down='black_thing.png',border=[0,0,0,0])


        btns_top = [place, placeval, gen, genval, usrgrid, cs, csval, hs, hsval]
        for btn in btns_top:
            top_buttons.add_widget(btn)

        game_end = Popup(title="Game Over", title_size = 42, title_color=[0,0,0], title_font='joystix', background='black_thing.png', separator_height=0, size_hint=(1,1),title_align='center' ,pos_hint={'center':0.5,'center':0.5},auto_dismiss=False)
        end_layout = GridLayout(cols=1, spacing=10, size_hint=(1,1))
        high_score_label = Label(text="", font_name='Roboto', bold=True, font_size=36, color=[1,.25,0,1],halign="center")
        final_score_label = Label(text=(""), font_name='Roboto', bold=True, font_size=36,halign="center")
        play_again = Button(text="Play Again", font_size=42,font_name='joystix', size_hint_y=.5, on_press=partial(self.restart_btn_action, grid,start_patterns, cells,game_end, csval, gen,genval, placeval,hsval))
        end_layout.add_widget(high_score_label)
        end_layout.add_widget(final_score_label)
        end_layout.add_widget(play_again)
        game_end.add_widget(end_layout)
        # setup main menu buttons
        playground_btn.bind(on_press=partial(self.trigger_playground_mode, main_menu, start_patterns, grid, cells,placeval,gen,genval,btn_sett))

        choose_game = Popup(title="Select Game Version", background='black_thing.png', title_font='joystix', title_size=50, separator_height=0, size_hint=(1,1), pos_hint={'center':0.5,'center':0.5}, title_align="center",auto_dismiss=False)
        choose_game_layout = GridLayout(rows=3, spacing=[20,5], size_hint_y=.9, size_hint_x=.7)
        creation_mode_btn = Button(text="Creation",font_size=mysize, font_name='joystix',size_hint_x=.3)
        survival_mode_btn = Button(text="Survival",font_size=mysize, font_name='joystix',size_hint_x=.3)
        for two_times in range(2):
            choose_game_layout.add_widget(Button(text='', background_normal='black_thing.png', background_down='black_thing.png',height=dp(5)))
        choose_game_layout.add_widget(creation_mode_btn)
        choose_game_layout.add_widget(survival_mode_btn)
        for two_more_times in range(2):
            choose_game_layout.add_widget(Button(text='', background_normal='black_thing.png', background_down='black_thing.png',height=dp(5)))
        choose_game.add_widget(choose_game_layout)
        creation_mode_btn.bind(on_press=partial(self.trigger_game_mode, choose_game, cells, grid, csval, gen,genval, placeval, hsval,btn_sett,1))
        survival_mode_btn.bind(on_press=partial(self.trigger_game_mode,choose_game, cells, grid, csval, gen,genval, placeval, hsval,btn_sett,2))
        game_btn.bind(on_press=partial(self.open_popup,choose_game,main_menu))
        # cells.bind(a_d_ratio=partial(self.update_score, cells, cs,place))
        cells.bind(generations=partial(self.update_game, cells, csval,placeval,genval, game_end))
        cells.bind(spawn_count=partial(self.update_game, cells, csval, placeval, genval, game_end))
        cells.bind(all_activated=partial(self.update_game, cells, csval, placeval, genval, game_end))
        cells.bind(spawn_adder=cells.add_spawns)
        start_patterns.bind(on_open=partial(self.reset_labels, csval, gen, genval, placeval, hsval,cells))
        restart_btn.bind(on_press=partial(self.restart_btn_action, grid,start_patterns, cells,restart_game, csval, gen,genval, placeval,hsval))

        game_end.bind(on_open=partial(self.update_score_labels, play_again, final_score_label,high_score_label, cells))
        game_end.bind(on_dismiss=partial(self.unscheduleit, play_again))
        game_end.bind(on_dismiss=partial(self.clear_text, high_score_label))


        board.add_widget(top_buttons)
        board.add_widget(buttons)
        return board

    def update(self,event):
        self.hs.text = randint(0,100)

    def build_config(self, config):
        config.setdefaults('initiate', {
            'Wrap': 0,
            'Speed': 'Fast',
            'Lonely': 1,
            'Crowded': 4,
            'Born': 3,
            'Color': 'Random',
            'Music': 1,
            })
        config_file = self.get_application_config()
        config.read(config_file)
        for item in config._sections:
            for x in config._sections[item]:
                if x == 'wrap':
                    Cells.wrap = int(config._sections[item][x])
                if x == 'speed':
                    Cells.speed = Cells.speeds[config._sections[item][x]]
                if x == 'color':
                    Cells.cellcol = config._sections[item][x]
                if x == 'born':
                    Cells.birth = config._sections[item][x]
                if x == 'lonely':
                    Cells.lonely = config._sections[item][x]
                if x == 'crowded':
                    Cells.crowded = config._sections[item][x]
                if x == 'music':
                    Cells.music = int(config._sections[item][x])



    def build_settings(self, settings):
        settings.register_type('scrolloptions', SettingScrollOptions)
        settings.add_json_panel('Game Settings', self.config, data=settings_json)


    def on_config_change(self, config, section, key, value):
        if key == 'Wrap':
            self.game_cells.wrap = int(value)
        if key == 'Speed':
            self.game_cells.speed = self.game_cells.speeds[value]
        if key == 'Color':
            self.game_cells.cellcol = value
            self.game_cells.set_canvas_color()
        if key == 'Born':
            self.game_cells.birth = int(value)
        if key == 'Lonely':
            self.game_cells.lonely = int(value)
        if key == 'Crowded':
            self.game_cells.crowded = int(value)
        if key == 'Music':
            self.game_cells.music = int(value)
            if self.game_cells.music == 1:
                self.game_cells.music_control('main', True, True)
            else:
                self.game_cells.stop_music()
        else:
            pass
        # print config, section, key, value

if __name__ == '__main__':
    GameApp().run()
