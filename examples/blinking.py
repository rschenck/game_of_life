from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.clock import Clock
import random

class RootWidget(GridLayout):
    pass

class MainApp(App):

    def build(self):
        parent = GridLayout(cols=6)
        for i in (1,2,3,4,5,6):
            for j in (1,2,3,4,5,6):
                parent.add_widget(Button(text='%s%s'%(i,j)))

        Clock.schedule_interval(lambda a:self.update(parent),1)

        return parent

    def update(self,obj):
        print "I am update function"
        for child in obj.children:
            c=[0,random.random(),1,random.random()]
            child.color=c


if __name__ == '__main__':
    MainApp().run()