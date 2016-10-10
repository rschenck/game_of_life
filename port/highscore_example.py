from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.storage.jsonstore import JsonStore

from kivy.properties import NumericProperty

from functools import partial

from os.path import join


class TestApp(App):
    def build(self):
        data_dir = getattr(self, 'user_data_dir')
        self.highscorejson = JsonStore(join(data_dir, 'highscore.json'))
        self.score = 0  # Default value for current score
        if self.highscorejson.exists('highscore'):  # Checking if 'highscore' exists in your cache file
            self.score = int(self.highscorejson.get('highscore')['best'])

        f = FloatLayout()
        self.btn = Button(text=str(self.score),
                          font_size=150)
        self.btn.bind(on_press=partial(some_function, self))
        f.add_widget(self.btn)

        return f
        print highscore


def some_function(q, *args):
    print q.score
    q.score += 1
    q.highscorejson.put('highscore', best=q.score)
    q.btn.text = str(q.score)


if __name__ == "__main__":
    TestApp().run()
