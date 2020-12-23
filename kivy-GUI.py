from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

from CheckersClasses import Board

Builder.load_file('checkers.kv')


class CheckersLayout(Widget):
    def __init__(self):
        super(CheckersLayout, self).__init__()

    def new_game(self, checkbox_1, checkbox_2):
        """
            When clicked initialize new game. According to player choice puts black or white mens
            on bottom part of the board.

        """

        if checkbox_1.active:
            # black color
            print('black')
            game_board = Board()
            # print(game_board)
        elif checkbox_2.active:
            print('white')
        else:
            print('choose a color.')

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