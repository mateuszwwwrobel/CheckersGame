from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('checkers.kv')


class CheckersLayout(Widget):
    def __init__(self):
        super(CheckersLayout, self).__init__()

    def new_game(self):
        pass

    def checkbox_active(self, checkbox_1, checkbox_2):
        if checkbox_1.active:
            checkbox_2.active = False
            print(f'The checkbox {checkbox_1}={checkbox_1.active} and {checkbox_2}={checkbox_2.active}')
        else:
            print(f'The checkbox {checkbox_1}={checkbox_1.active} and {checkbox_2}={checkbox_2.active}')

    def board_field_clicked(self):
        pass

    def men_move(self):
        pass

    def king_move(self):
        pass


class CheckersApp(App):
    def build(self):
        Window.size = (800, 800)
        Window.clearcolor = (.655, .682, .682, 1)
        return CheckersLayout()


if __name__ == '__main__':
    CheckersApp().run()