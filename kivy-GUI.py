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
        self.board = None
        super(CheckersLayout, self).__init__()

    def new_game(self, checkbox_1, checkbox_2):
        """
            When clicked initialize new game. According to player choice puts black or white mens
            on bottom part of the board.

        """

        if checkbox_1.active:
            self.put_men_on_board('black')

        elif checkbox_2.active:
            self.put_men_on_board('white')

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

    def put_men_on_board(self, color):
        # Initialize backend board.
        self.board = Board(color)

        # Initialize frontend board.
        bottom_starting_fields = [self.ids.board_button_41,
                                  self.ids.board_button_43,
                                  self.ids.board_button_45,
                                  self.ids.board_button_47,
                                  self.ids.board_button_50,
                                  self.ids.board_button_52,
                                  self.ids.board_button_54,
                                  self.ids.board_button_56,
                                  self.ids.board_button_57,
                                  self.ids.board_button_59,
                                  self.ids.board_button_61,
                                  self.ids.board_button_63,
                                  ]

        upper_starting_fields = [self.ids.board_button_2,
                                 self.ids.board_button_4,
                                 self.ids.board_button_6,
                                 self.ids.board_button_8,
                                 self.ids.board_button_9,
                                 self.ids.board_button_11,
                                 self.ids.board_button_13,
                                 self.ids.board_button_15,
                                 self.ids.board_button_18,
                                 self.ids.board_button_20,
                                 self.ids.board_button_22,
                                 self.ids.board_button_24,
                                 ]

        if color == 'black':
            for upper_field, bottom_field in zip(upper_starting_fields, bottom_starting_fields):
                bottom_field.background_normal = 'img/black_black_men.png'
                upper_field.background_normal = 'img/black_white_men.png'
        else:
            for upper_field, bottom_field in zip(upper_starting_fields, bottom_starting_fields):
                bottom_field.background_normal = 'img/black_white_men.png'
                upper_field.background_normal = 'img/black_black_men.png'

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
    icon = 'img/icon.png'

    def build(self):
        Window.size = (1100, 1100)
        Window.clearcolor = (.655, .682, .682, 1)

        return CheckersLayout()


if __name__ == '__main__':
    CheckersApp().run()