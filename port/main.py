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
from time import time
from presets import presets

# def song(music):
#     sound = SoundLoader.load('img/emotion.wav')
#     if sound and music:
#         sound.loop = True
#         sound.play()
#
def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
        pass


class Grid(Widget):
    def draw_grid(self, *largs):
        self.size = (Window.width, Window.height - 100) # Should be fine to draw off window size
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
    'White': (0,0,1),
    'Grey': (0,0,0.25),
    'Blue': (0.6666,1,1),
    'Green': (0.3333,1,1),
    'Black':(0,0,0),
    'Red': (1,1,1)
    }
    # speed, cellcol, birth, lonely, crowded = .1, 'White', 3, 1, 4
    # update_count = 0
    update_time = 0
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
    # alive_cell_instructions = InstructionGroup()
    # alive_color_instruction = InstructionGroup()
    # was_cell_instructions = InstructionGroup()
    # was_cell_instructions.add(Color(0.25,0.25,0.25,mode='rgb'))
    all_activated = NumericProperty(0)
    score = NumericProperty(0)
    bonus_multiplier = 1
    spawn_count = NumericProperty(50)
    generations = NumericProperty(500)
    all_died = NumericProperty(0)
    game_over = False
    active_cell_count = NumericProperty(0)
    game_mode = False
    spawn_adder = NumericProperty(0)
    cell_color = (0,0,0)

    # update_time = 0




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
            for x in range(0,self.dimensions[0]/10):
                for y in range(0,self.dimensions[1]/10):
                    # assign 25% chance of life
                    if randint(0,3) == 1:
                        self.on_board[x,y] = {'alive':1, 'was':0}
        else:
            for coor in presets[selection]:
                self.on_board[( self.mid_x + int(coor[0]), self.mid_y + int(coor[1]) )] = {'alive':1, 'was':0}

        self.music_control('main', True, True)
        modal.dismiss()




    # Setup functions
    # Create all possible rectangles for the given window size
    def create_rectangles(self, *largs):
        self.rectangles_dict.clear()
        self.dimensions = (Window.width - 20, Window.height - 120)
        self.pos = (11,61)
        for x in range(0,self.dimensions[0]/10):
            for y in range(0,self.dimensions[1]/10):
                rect = Rectangle(pos=(self.x + x * 10, self.y + y *10), size=(9,9))
                color = Color(0,0,0,mode="hsv")
                self.rectangles_dict[x,y] = {"rect":rect,"color":color}



    # def add_instruction_groups(self, *largs):
    #     # self.canvas.add(self.alive_color_instruction)
    #     self.canvas.add(self.alive_cell_instructions)
    #     self.canvas.add(self.was_cell_instructions)
    def draw_rectangles(self, *largs):
        for x_y in self.rectangles_dict:
            self.rectangles_dict[x_y]["color"].hsv = (0,0,0)
            self.canvas.add(self.rectangles_dict[x_y]["color"])
            self.canvas.add(self.rectangles_dict[x_y]["rect"])



    # set canvas_color, self.pos and cells midpoint
    def setup_cells(self, *largs):
        self.set_canvas_color()
        self.pos = (11,61)
        self.mid_x,self.mid_y = self.dimensions[0]/20, self.dimensions[1]/20




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
        # self.draw_rectangles()
        for x_y in self.on_board:
            self.rectangles_dict[x_y]["color"].hsv = self.cell_color
            self.canvas.add(self.rectangles_dict[x_y]["color"])
            self.canvas.add(self.rectangles_dict[x_y]["rect"])
        self.should_draw = True
        self.accept_touches = True # Only first time matters



    # game logic for each iteration
    def get_cell_changes(self, *largs):
        then = time()
        for x in range(0,int(self.dimensions[0]/10)):
            for y in range(0,int(self.dimensions[1]/10)):
                over_x,over_y = (x + 1) % (self.dimensions[0]/10), (y + 1) % (self.dimensions[1]/10)
                bel_x, bel_y = (x - 1) % (self.dimensions[0]/10), (y - 1) % (self.dimensions[1]/10)
                alive_neighbors = self.on_board[bel_x,bel_y]['alive'] + self.on_board[bel_x,y]['alive'] + self.on_board[bel_x,over_y]['alive'] + self.on_board[x,bel_y]['alive'] + self.on_board[x,over_y]['alive'] + self.on_board[over_x,bel_y]['alive'] + self.on_board[over_x,y]['alive'] + self.on_board[over_x,over_y]['alive']

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
        # print "Get Cell Changes Runtime: ", time() - then



    # loops through changes from ^^ and adds the rectangles
    def update_canvas_objects(self,*largs):
        # print "time since last call: ", time() - self.update_time
        # self.update_time = time()
        then = time()
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
        self.changes_dict.clear()
        self.all_activated += plus
        self.spawn_adder = self.all_activated / 1000
        self.score += (plus * self.bonus_multiplier)
        self.all_died += minus
        # print "Update Canvas Objects Runtime: ", time() - then




    # Our start/step scheduled function
    def update_cells(self,*largs):
        # print "Time since last update: ", time() - self.update_time
        self.update_time = time()
        then = time()
        # self.update_count += 1
        then = time()
        if self.cellcol == 'Random':
            self.set_canvas_color(on_request=True)
        self.get_cell_changes()
        self.update_canvas_objects()
        self.update_counters()
        # print "Update Cells Complete Runtime: ", time() - then

    def add_spawns(self, *largs):
        # print "Adding Spawns: all_activate:", self.all_activated,"; spawn_count:", self.spawn_count
        self.spawn_count += 5

    def update_counters(self,*largs):
        if self.game_mode:
            self.generations -= 1
        if self.active_cell_count < 1000:
            self.bonus_multiplier = 1
        elif self.active_cell_count >= 1000:
            self.bonus_multiplier = 1 + (self.active_cell_count / 1000)


    def start_interval(self, events, *largs):
        # self.update_time = time()
        self.should_draw = False
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        events.append(Clock.schedule_interval(self.update_cells,float(self.speed)))

    def stop_interval(self, events, *largs):
        self.should_draw = True
        if len(events) > 0:
            events[-1].cancel()
            events.pop()

    def step(self, events, *largs):
        self.should_draw = True
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        Clock.schedule_once(self.update_cells, 1.0/60.0)

    def reset_interval(self, events, grid, modal,*largs):
        for x in largs:
            if type(x) == Popup:
                x.dismiss()
        self.should_draw = False
        if len(events) > 0:
            events[-1].cancel()
            events.pop()
        self.on_board.clear()
        self.changes_dict.clear()
        grid.canvas.clear()
        # self.alive_cell_instructions.clear()
        # self.was_cell_instructions.clear()
        # self.was_cell_instructions.add(Color(0.25,0.25,0.25,mode='rgb'))
        self.canvas.clear()
        self.setup_cells()
        self.game_over = False
        # self.reset_counters()
        if modal:
            modal.open()
            self.game_mode = False
        else:
            self.assign_blank(None)
            grid.draw_grid()
            self.starting_cells()
            self.game_mode = True

    def reset_counters(self):
        self.all_activated = 0
        self.all_died = 0
        self.generations = 500
        self.active_cell_count = 0
        self.spawn_count = 100
        self.score = 0
        self.bonus_multiplier = 1


    # Touch Handlers
    # Add rectangles and positive values to on_board when the animation is stopped.
    # Add values to changes_dict otherwise, rects added on next iteration
    def on_touch_down(self, touch):
        pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
        # print (touch.pos), self.accept_touches
        pos_x = int(math.floor(pos_x / 10.0))
        pos_y = int(math.floor(pos_y / 10.0))
        in_bounds = (0 <= pos_x < (self.dimensions[0] / 10)) and (0 <= pos_y < (self.dimensions[1] / 10))
        # sign_x = "+" if pos_x - self.mid_x >= 0 else ""
        # sign_y = "+" if pos_y - self.mid_y >= 0 else ""
        # print "self.on_board[(self.mid_x" + sign_x, pos_x - self.mid_x,",self.mid_y"+sign_y,pos_y-self.mid_y,")] = {'alive':1, 'was':0}"
        if self.accept_touches and in_bounds and self.spawn_count > 0:
        # if self.accept_touches and in_bounds:
            try:
                if not self.on_board[pos_x,pos_y]['alive']:
                    if self.should_draw:
                        self.on_board[pos_x,pos_y]['alive'] = 1
                        self.rectangles_dict[pos_x,pos_y]["color"].hsv = self.cell_color
                        if not self.on_board[pos_x,pos_y]['was']:
                            self.canvas.add(self.rectangles_dict[pos_x,pos_y]["color"])
                            self.canvas.add(self.rectangles_dict[pos_x,pos_y]["rect"])
                    else:
                        self.changes_dict[(pos_x,pos_y)] = 1
                    if self.game_mode:
                        self.spawn_count -= 1
            except KeyError:
                pass
        else:
            pass

    def on_touch_move(self, touch):
        self.mouse_positions.append(touch.pos)
        # print(touch.pos), self.accept_touches
        for pos in self.mouse_positions:
            pos_x, pos_y = touch.pos[0] - self.x, touch.pos[1] - self.y
            pos_x = int(math.floor(pos_x / 10.0))
            pos_y = int(math.floor(pos_y / 10.0))

            in_bounds = (0 <= pos_x < (self.dimensions[0] / 10)) and (0 <= pos_y < (self.dimensions[1] / 10))

            # print "touch_move in bounds?", in_bounds
            # print "pos_x, pos_y", pos_x ,",",pos_y
            # print "canvas width and height", self.width, self.height
            # print "self.on_board[(", pos_x, ",",pos_y,")] = {'alive':1, 'was':0}"
            if self.accept_touches and in_bounds and self.spawn_count > 0:
            # if self.accept_touches and in_bounds:
                try:
                    if not self.on_board[pos_x,pos_y]['alive']:
                        if self.should_draw:
                            self.on_board[pos_x,pos_y]['alive'] = 1
                            self.rectangles_dict[pos_x,pos_y]["color"].hsv = self.cell_color
                            if not self.on_board[pos_x,pos_y]['was']:
                                self.canvas.add(self.rectangles_dict[pos_x,pos_y]["color"])
                                self.canvas.add(self.rectangles_dict[pos_x,pos_y]["rect"])
                        else:
                            self.changes_dict[(pos_x,pos_y)] = 1
                        if self.game_mode:
                            self.spawn_count -= 1
                except KeyError:
                    pass
        self.mouse_positions = []

    def on_rotate(self):
        self.loadimg
        self.reset_interval

    def on_flip(self):
        self.loadimg
        self.reset_interval

    # Need to add some placement options...
    def place_option(self, events, *largs):
        pass

    def info(self, events, *largs):
        if Window.width < Window.height:
            titlesize = 18
            mysize = 18
        else:
            titlesize = Window.size[1]/100.*3.4
            mysize = Window.size[1]/100.*3

        info1 = '''Rules:\n      If a cell has 0-1 neighbors, it dies.\n      If a cell has 4 or more neighbors, it dies.\n      If a cell has 2-3 neighbors, it survives.\n      If a space is surrounded by 3 neighbors, a cell is born.\n\n'''
        info2 = '''Controls:\n      Click or draw to add cells.\n       Modify the default rules and more in settings.\n'''
        info3 = '''\nCreated by:\n      Steven Lee-Kramer\n      Ryan O Schenck'''
        popup = Popup(title="John Conway's Game of Life", separator_height=0, title_size=titlesize,
            content=Label(text=''.join([info1,info2,info3]),font_size=mysize),
            size_hint=(.8, .8),title_align='center',)
        popup.bind(on_dismiss=partial(self.music_control, 'main', True, True))
        self.music_control('options', True, True)
        popup.open()

    def loadimg(self, events, *largs):
        content = Image(source='IMO_GOL2.png')
        popup = Popup(title='', content=content,
              auto_dismiss=False, separator_height=0,title_size=0, separator_color=[0.,0.,0.,0.], size=(Window.height,Window.width),
              # border=[20,20,20,20],
              background='black_thing.png',
              background_color=[0,0,0,1])
        content.bind(on_touch_down=popup.dismiss)
        popup.open()

    def stop(self, *largs):
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
                except NameError:
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
    events = []
    game_cells = None
    # restart_menu = None
    highscore = 0
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

    # def update_score(self,cells,adrat, cs, place, *largs):
    def update_game(self, cells, adrat, cs, place, gen, game_end, *largs):
        if cells.game_mode:
            gen.text = str(cells.generations)
            place.text = str(cells.spawn_count)
        else:
            gen.text = '∞'
            place.text = '∞'
        cs.text = self.intWithCommas(cells.score)
        adrat.text = str(cells.all_activated - cells.all_died)

        if cells.generations == 0 or cells.game_over:
            cells.stop_interval(self.events)
            cells.music_control('score', True, True)
            game_end.open()

    def reset_labels(self, adratval, csval, genval, placeval, hsval, cells,*largs):
        adratval.text = "--"
        csval.text = "--"
        hsval.text = str(self.intWithCommas(self.highscore))
        if cells.game_mode:
            genval.text = "500"
            placeval.text = "100"
        else:
            genval.text = '∞'
            placeval.text = '∞'


    def update_score_labels(self, myobject, final_score_label, high_score_label,cells, *largs):
        blinky = Clock.schedule_interval(lambda a:self.colorit(myobject),0.3)
        global blinky
        if cells.score > self.highscore:
            self.highscore = cells.score
            self.highscorejson.put('highscore', best=cells.score)
            high_score_display = str(self.intWithCommas(self.highscore)) + " New Record!!"
        else:
            high_score_display = "You've done better!"
        high_score_label.text = high_score_display
        final_score_label.text = "Final Score: " + str(self.intWithCommas(cells.score))
# REMOVE THIS LINE TO GET RID OF HIGH SCORE = 0
        # self.highscorejson.put('highscore', best=0)
        # self.highscore = 0



    def close_modals(self, start_patterns, restart_game, *largs):
        try:
            start_patterns.dismiss()
        except:
            pass
        try:
            restart_game.dismiss()
        except:
            pass
    def nothing(self,*largs):
        pass
    def trigger_game_mode(self, main_menu, cells, grid, adratval, csval, genval, placeval, hsval,btn_sett,*largs):
        btn_sett.background_down = 'btn_solid.png'
        btn_sett.text = "---"
        self.game_cells.lonely = 1
        self.game_cells.crowded = 4
        self.game_cells.birth = 3
        self.game_cells.speed = 0.05
        main_menu.dismiss()
        cells.reset_counters()
        cells.game_mode = True
        self.reset_labels(adratval, csval, genval, placeval, hsval, cells)
        cells.reset_interval(self.events, grid, None)

    def trigger_playground_mode(self, popup, start_patterns, grid, cells, placeval, genval,btn_sett, *largs):
        btn_sett.background_down = 'bttn_dn.png'
        btn_sett.text = "Options"
        cells.reset_counters()
        for item in self.config._sections:
            for x in self.config._sections[item]:
                if x == 'speed':
                    self.game_cells.speed = self.config._sections[item][x]
                if x == 'born':
                    self.game_cells.birth = self.config._sections[item][x]
                if x == 'lonely':
                    self.game_cells.lonely = self.config._sections[item][x]
                if x == 'crowded':
                    self.game_cells.crowded = self.config._sections[item][x]
        popup.dismiss()
        placeval.text = '∞'
        genval.text = '∞'
        cells.reset_interval(self.events,grid, start_patterns)
    def restart_btn_action(self, grid, start_patterns, cells, restart_game, adratval, csval, genval, placeval,hsval,*largs):
        restart_game.dismiss()
        cells.reset_counters()
        self.reset_labels(adratval, csval, genval, placeval, hsval, cells)
        if cells.game_mode:
            cells.reset_interval(self.events,grid,None)
        else:
            cells.reset_interval(self.events, grid, start_patterns)

    def colorit(self, myobject, *largs):
        myobject.color = [randint(0,1),randint(0,1),randint(0,1),1]
        # print myobject.color

    def unscheduleit(self, myobject, *largs):
        Clock.unschedule(blinky)

    def settings(self, events, *largs):
        if self.game_cells.game_mode:
            pass
        else:
            self.open_settings()

    def build(self):
        self.settings_cls = SettingsWithSpinner
        # dump(self.settings_cls)
        self.config.items('initiate')
        self.use_kivy_settings = False
        data_dir = getattr(self, 'user_data_dir')
        self.highscorejson = JsonStore(join(data_dir, 'highscore.json'))
        if self.highscorejson.exists('highscore'):
            self.highscore = int(self.highscorejson.get('highscore')['best'])
        # Delete this once finalized
        # if Window.width < 1334 and Window.height < 750:
        #     Window.size = (1334,750)

        Window.size = (667*2,267*2)
        usrgridnum = Window.system_size[0]*Window.system_size[1]/100000.

        # make layout and additional widgets
        board = FloatLayout(size=(Window.width, Window.height))
        grid = Grid(size=(Window.width, Window.height - 100), pos=(0,50))
        self.game_cells = cells = Cells(size=(Window.width - 20, Window.height - 120), pos=(11,61))

        board.add_widget(grid)
        board.add_widget(cells)
        cells.create_rectangles()
        # cells.draw_rectangles()
        # cells.add_instruction_groups()
        Clock.schedule_once(cells.loadimg, 0)
        
        if bool(int(self.game_cells.music)):
            cells.music_control('options', False, True)
        else:
            pass

        main_menu = Popup(title="Main Menu", background='black_thing.png', title_font='joystix', title_size=60, separator_height=0, size_hint=(.5,.5), pos_hint={'center':0.5,'center':0.50}, title_align="center",auto_dismiss=False)
        main_menu_layout = GridLayout(cols=1, spacing=10, size_hint_y=.9, size_hint_x=.1)
        playground_btn = Button(text="Playground Mode",font_name='joystix', size_hint_x=.5)
        game_btn = Button(text="Game Mode", font_name='joystix', size_hint_x=.5)
        # main_menu_layout.add_widget(Widget(size_hint_y=None, height=dp(25)))
        main_menu_layout.add_widget(playground_btn)
        # main_menu_layout.add_widget(Widget(size_hint_y=None, height=dp(25)))
        main_menu_layout.add_widget(game_btn)
        main_menu.add_widget(main_menu_layout)

# Set start patterns and internal scrolling layout
        start_patterns = Popup(title="Select Pattern", title_size=32, background='popup.png', title_font='joystix', separator_height=0 ,size_hint=(0.5,0.8),title_align='center' ,pos_hint={'center':0.5,'center':0.50})
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
        restart_game = Popup(title="Reset", title_font='joystix', title_size=56, background='popup.png', separator_height=0 ,size_hint=(0.4,0.4),title_align='center' ,pos_hint={'center':0.5,'center':0.50})
        restart_game_layout = BoxLayout(size_hint=(1,1),orientation='vertical')
        # restart_game_label = Label(text="Are you sure you want to restart?")

        button_container = GridLayout(cols=1, spacing='5dp')
        restart_btn = Button(text="Restart", font_name='joystix', size_hint=(1,None),height=dp(50))
        cancel_main_box = BoxLayout(size_hint=(0.5,0.5), height=dp(55), orientation='horizontal')
        cancel_restart_button = Button(text="Cancel", font_name='joystix',on_press=restart_game.dismiss,size_hint=(1,None), height=dp(50))
        r_main_menu_button = Button(text="Main Menu", font_name='joystix',on_press=main_menu.open,size_hint=(1,None), height=dp(45))
        r_main_menu_button.bind(on_release=partial(cells.music_control, 'options', True, True))

        # restart_game_layout.add_widget(restart_game_label)
        cancel_main_box.add_widget(restart_btn)
        cancel_main_box.add_widget(cancel_restart_button)
        button_container.add_widget(cancel_main_box)
        button_container.add_widget(r_main_menu_button)
        restart_game_layout.add_widget(button_container)
        restart_game.add_widget(restart_game_layout)


# game buttons
        btn_start = Button(text='START', font_name='joystix' ,on_press=partial(cells.start_interval, self.events), background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_stop = Button(text='Stop', font_name='joystix' ,on_press=partial(cells.stop_interval, self.events), background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_step = Button(text='Step', font_name='joystix' ,on_press=partial(cells.step, self.events), background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_reset = Button(text='Reset', font_name='joystix' ,
                           on_press=restart_game.open, background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_reset.bind(on_press=partial(cells.stop_interval, self.events))
        btn_place = Button(text='Place', font_name='joystix' , on_press=partial(cells.place_option, self.events), background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='test.png')
        # dump(btn_place)
        btn_sett = Button(text='Options', font_name='joystix' ,on_press=partial(self.settings, self.events), background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_info = Button(text='Info', font_name='joystix' ,on_press=partial(cells.info, self.events), background_down='black_thing.png', background_normal='black_thing.png', border=[0,0,0,0], background_disabled_down='black_thing.png', background_disabled_normal='black_thing.png')
        btn_sett.bind(on_press=partial(cells.stop_interval, self.events))

        buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'y':0})

        board.bind(size=cells.create_rectangles)
        board.bind(size=partial(cells.reset_interval,self.events,grid,main_menu))

        controls =[btn_start,btn_stop,btn_step,btn_reset,btn_sett,btn_info]
        for btn in controls:
            buttons.add_widget(btn)
        
        Clock.schedule_once(main_menu.open,0)
        
        main_menu.bind(on_open=partial(self.close_modals, start_patterns, restart_game))
        start_patterns.bind(on_open=partial(self.close_modals, None, restart_game))
        start_patterns.bind(on_dismiss=grid.draw_grid)
        start_patterns.bind(on_dismiss=cells.starting_cells)


        # Score Label Widgets
        top_buttons = BoxLayout(size_hint=(1, None), height=50, pos_hint={'x':0, 'top':1})

        hs = Button(text='High Score:', font_name='Roboto',  font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        hsval = Button(text=self.intWithCommas(int(self.highscore)), font_name='Roboto',  font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        cs = Button(text='Score:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        csval = Button(text='--', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        adrat = Button(text='A/D (+/-):', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        adratval = Button(text='--', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        place = Button(text='Spawns:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        placeval = Button(text='100', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        gen = Button(text='Gens:', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        genval = Button(text='500', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        usrgrid = Button(text='Grid: ', font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])
        gridnum = Button(text=str(usrgridnum), font_name='Roboto', font_size=24, color=[1,.25,0,1], background_normal='black_thing.png', border=[0,0,0,0])

        btns_top = [place, placeval, gen, genval, adrat, adratval, usrgrid, gridnum, cs, csval, hs, hsval]
        for btn in btns_top:
            top_buttons.add_widget(btn)

        game_end = Popup(title="Game Over", title_size = 42, title_color=[0,0,0], title_font='joystix', background='black_thing.png', separator_height=0, size_hint=(1,1),title_align='center' ,pos_hint={'center':0.5,'center':0.5},auto_dismiss=False)
        end_layout = GridLayout(cols=1, spacing=10, size_hint=(1,1))
        high_score_label = Label(text="", font_name='Roboto', bold=True, font_size=36, color=[1,.25,0,1])
        final_score_label = Label(text=(""), font_name='Roboto', bold=True, font_size=36)
        play_again = Button(text="Play Again", font_size=42,font_name='joystix', size_hint_y=.5, on_press=partial(self.trigger_game_mode, game_end,cells, grid,adratval, csval, genval, placeval, hsval, btn_sett))
        end_layout.add_widget(high_score_label)
        end_layout.add_widget(final_score_label)
        end_layout.add_widget(play_again)
        game_end.add_widget(end_layout)
        # setup main menu buttons
        playground_btn.bind(on_press=partial(self.trigger_playground_mode, main_menu, start_patterns,grid, cells,placeval,genval,btn_sett))

        game_btn.bind(on_press=partial(self.trigger_game_mode, main_menu, cells, grid,adratval, csval, genval, placeval, hsval,btn_sett))
        # cells.bind(a_d_ratio=partial(self.update_score, cells, adrat, cs,place))
        cells.bind(generations=partial(self.update_game, cells, adratval, csval,placeval,genval, game_end))
        cells.bind(spawn_count=partial(self.update_game, cells, adratval, csval, placeval, genval, game_end))
        cells.bind(all_activated=partial(self.update_game, cells, adratval, csval, placeval, genval, game_end))
        cells.bind(spawn_adder=cells.add_spawns)
        start_patterns.bind(on_open=partial(self.reset_labels, adratval, csval, genval, placeval, hsval,cells))
        restart_btn.bind(on_press=partial(self.restart_btn_action, grid,start_patterns, cells,restart_game,adratval, csval, genval, placeval,hsval))

        game_end.bind(on_open=partial(self.update_score_labels, play_again, final_score_label,high_score_label, cells))
        game_end.bind(on_dismiss=partial(self.unscheduleit, play_again))


        board.add_widget(top_buttons)
        board.add_widget(buttons)
        return board

    def update(self,event):
        self.hs.text = randint(0,100)

    def build_config(self, config):
        config.setdefaults('initiate', {
            'Speed': 0.05,
            'Lonely': 1,
            'Crowded': 4,
            'Born': 3,
            'Color': 'White',
            'Music': 1,
            })
        config_file = self.get_application_config()
        config.read(config_file)
        for item in config._sections:
            for x in config._sections[item]:
                if x == 'speed':
                    Cells.speed = config._sections[item][x]
                if x == 'color':
                    Cells.cellcol = config._sections[item][x]
                if x == 'born':
                    Cells.birth = config._sections[item][x]
                if x == 'lonely':
                    Cells.lonely = config._sections[item][x]
                if x == 'crowded':
                    Cells.crowded = config._sections[item][x]
                if x == 'music':
                    Cells.music = config._sections[item][x]


    def build_settings(self, settings):
        settings.register_type('scrolloptions', SettingScrollOptions)
        settings.add_json_panel('Game Settings', self.config, data=settings_json)


    def on_config_change(self, config, section, key, value):
        if key == 'Speed':
            self.game_cells.speed = float(value)
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
                self.game_cells.stop()
        else:
            pass
        # print config, section, key, value

if __name__ == '__main__':
    GameApp().run()
