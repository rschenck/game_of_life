from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import runTouchApp
from functools import partial


class PopupApp(App):
    def dismiss_modal(modal, *largs):
        modal.dismiss()

    def build(self):
        board = FloatLayout(size=(Window.width, Window.height))
        popup = Popup(title="test popup", size_hint=(0.3,0.8), pos_hint={'x':0.35,'top':0.95})
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40, on_press=popup.dismiss)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(1, 1))
        root.add_widget(layout)
        popup.add_widget(root)
        # board.add_widget(popup)
        # popup.open()
        b1 = Button(text="open",size_hint=(0.2,None),height=45, pos_hint={'x':0.4})
        # content = GridLayout(cols=1,spacing=10,size_hint_y=None)
        # button = Button(text="dismiss")
        # content.add_widget(button)
        # popup = Popup(title="test popup", content=content,size_hint=(0.3,0.9))
        # button.bind(on_press=popup.dismiss)
        board.add_widget(b1)
        b1.bind(on_press=popup.open)

        return board

if __name__ == '__main__':
    PopupApp().run()
