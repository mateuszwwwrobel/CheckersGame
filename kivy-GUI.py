from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.button import Button

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
            print('black')
            game_board = Board('black')
            print(game_board)

        elif checkbox_2.active:
            print('white')
            game_board = Board('white')
            print(game_board)

        else:
            info_button = Button(text='Please choose a color first.',
                                 font_size=22,
                                 bold=True,
                                 background_normal='img/white_blank.png',
                                 background_down='img/clicked.png',
                                 color=(.231, .353, .553, 1),
                                 )
            popup_message = self.popup_box('Color Error', info_button)
            popup_message.open()
            info_button.bind(on_press=popup_message.dismiss)

    def board_field_clicked(self):
        pass

    def men_move(self):
        pass

    def king_move(self):
        pass

    @staticmethod
    def popup_box(title, content):
        popup_box = Popup(title=title,
                          title_align='center',
                          content=content,
                          size_hint=(.4, .4),
                          size=(200, 200),
                          )
        return popup_box


class CheckersApp(App):
    def build(self):
        Window.size = (800, 800)
        Window.clearcolor = (.655, .682, .682, 1)
        return CheckersLayout()


if __name__ == '__main__':
    CheckersApp().run()