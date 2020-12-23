from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('checkers.kv')


class CheckersLayout(Widget):
    def __init__(self):
        super(CheckersLayout, self).__init__()

    def board_field_clicked(self):
        pass

    def men_move(self):
        pass

    def king_move(self):
        pass


class CheckersApp(App):
    def build(self):
        Window.clearcolor = (.655, .682, .682, 1)
        return CheckersLayout()


if __name__ == '__main__':
    CheckersApp().run()