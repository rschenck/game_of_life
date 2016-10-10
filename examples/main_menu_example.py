from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import runTouchApp
from functools import partial
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.widget import Widget

class PopupApp(App):
    restart_menu = None

    def setup_popup(self, layout, popup,*largs):
        self.restart_menu.content = layout
        popup.dismiss()

    def dismiss_modal(modal, *largs):
        modal.dismiss()

    def build(self):
        board = FloatLayout(size=(Window.width, Window.height))
        # popup = main menu
        popup = Popup(title="Main Menu", size_hint=(0.3,0.45), pos_hint={'x':0.35,'top':0.80})
        layout = GridLayout(cols=1, spacing=10, size_hint_y=1)
        button1 = Button(text="Playground Mode", size_hint=(1,None), height=dp(50))
        button2 = Button(text="Game Mode",size_hint=(1,None), height=dp(50))
        layout.add_widget(Widget(size_hint_y=None, height=dp(25)))
        layout.add_widget(button1)
        layout.add_widget(Widget(size_hint_y=None, height=dp(25)))
        layout.add_widget(button2)
        popup.add_widget(layout)
        # b1 is bound to board to open restart menu
        b1 = Button(text="Restart",size_hint=(0.2,None),height=45, pos_hint={'x':0.4})

        # restart_menu is a popup
        self.restart_menu = Popup(title="Restart",size_hint=(0.3,0.45), pos_hint={'x':0.35,'top':0.80})

        # setup playground restart menu
        restart_playground_layout = GridLayout(cols=1, spacing='5dp')
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40, on_press=self.restart_menu.dismiss)
            scroll_layout.add_widget(btn)
        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(scroll_layout)
        restart_playground_layout.add_widget(Widget(size_hint_y=None, height=dp(2)))
        restart_playground_layout.add_widget(scrollview)
        restart_playground_layout.add_widget(Button(text="Main Menu",on_press=popup.open, size_hint=(1,None), height=dp(50)))
        popup.bind(on_open=self.restart_menu.dismiss)
        self.restart_menu.content = restart_playground_layout
        # setup game restart menu
        restart_game_layout = BoxLayout(size_hint=(1,1),orientation='vertical')
        restart_game_label = Label(text="Are you sure you want to restart?")
        button_container = BoxLayout(size_hint=(1,None), height=dp(50), orientation='horizontal')
        restart_game_button = Button(text="Restart",on_press=self.restart_menu.dismiss)
        main_menu_button = Button(text="Main Menu", on_press=popup.open)
        restart_game_layout.add_widget(restart_game_label)
        button_container.add_widget(restart_game_button)
        button_container.add_widget(main_menu_button)
        restart_game_layout.add_widget(button_container)

        # handle setup of restart menu
        button1.bind(on_press=partial(self.setup_popup, restart_playground_layout, popup))
        button2.bind(on_press=partial(self.setup_popup, restart_game_layout, popup))

        board.add_widget(b1)
        b1.bind(on_press=self.restart_menu.open)
        popup.open()
        return board

if __name__ == '__main__':
    PopupApp().run()
