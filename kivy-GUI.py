from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread

from kivy.core.window import Window

from CheckersClasses import Board, Men


class CheckersLayout(Widget):

    def __init__(self):
        self.board = None
        self.bottom_color = None
        self.upper_color = None
        self.last_clicked_button = None
        self.init_buttons()
        super(CheckersLayout, self).__init__()

    @mainthread
    def init_buttons(self):
        white_fields = [1, 3, 5, 7, 10, 12, 14, 16, 17, 19, 21, 23, 26, 28, 30, 32,
                        33, 35, 37, 39, 42, 44, 46, 48, 49, 51, 53, 55, 58, 60, 62, 64]
        for button in range(1, 65):
            if button in white_fields:
                button = Button(text=f'board_button_{str(button)}')
                button.background_normal = 'img/white_blank.png'
                button.background_down = 'img/clicked.png'
            else:
                button = Button(text=f'board_button_{str(button)}')
                button.background_normal = 'img/black_blank.png'
                button.background_down = 'img/clicked.png'
            self.ids.buttons_widget.add_widget(button)

    def new_game(self, checkbox_1, checkbox_2):
        """
            When clicked initialize new game. According to player choice puts black or white mens
            on bottom part of the board.

        """

        if checkbox_1.active:
            self.bottom_color = 'black'
            self.upper_color = 'white'
            self.popup_box_new_game()

        elif checkbox_2.active:
            self.bottom_color = 'white'
            self.upper_color = 'black'
            self.popup_box_new_game()

        else:
            info_button = Button(text='Please choose a color first.',
                                 font_size=22,
                                 bold=True,
                                 background_normal='img/white_blank.png',
                                 background_down='img/clicked.png',
                                 color=(.231, .353, .553, 1),
                                 )
            popup_message = self.popup_box_message('Color Error', info_button)
            popup_message.open()
            info_button.bind(on_press=popup_message.dismiss)

    def put_pawns_on_board(self):
        # Initialize backend board.
        self.board = Board(self.bottom_color)

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

        if self.bottom_color == 'black':
            for upper_field, bottom_field in zip(upper_starting_fields, bottom_starting_fields):
                bottom_field.background_normal = 'img/black_black_men.png'
                upper_field.background_normal = 'img/black_white_men.png'
            return True
        elif self.bottom_color == 'white':
            for upper_field, bottom_field in zip(upper_starting_fields, bottom_starting_fields):
                bottom_field.background_normal = 'img/black_white_men.png'
                upper_field.background_normal = 'img/black_black_men.png'
            return True
        else:
            raise AttributeError("Something went wrong. Try again.")

    def board_field_clicked(self, field_number):
        if self.board is None:
            info_button = Button(text='Please start a game first.',
                                 font_size=22,
                                 bold=True,
                                 background_normal='img/white_blank.png',
                                 background_down='img/clicked.png',
                                 color=(.231, .353, .553, 1),
                                 )
            popup_message = self.popup_box_message('Start Game Error', info_button)
            popup_message.open()
            info_button.bind(on_press=popup_message.dismiss)
        else:
            if self.last_clicked_button is None:
                self.last_clicked_button = field_number

                # change background of current 'field_number' field:

                field_code = self.board.board[field_number]



                self.ids.board_button_41.background_normal = 'img/clicked.png'
            else:
                # TODO: proper popup box to be done.
                print('You have selected a pawn. Where do you want to move it?')

    def pawn_move(self, field_number):
        if self.last_clicked_button is not None:
            allowed_moves = Men.get_allowed_player_moves(self.last_clicked_button, field_number)

            if field_number in allowed_moves:

                self.board.make_men_move_on_board('3A', '4B', self.bottom_color)

                if self.bottom_color == 'black':
                    self.ids.board_button_34.background_normal = 'img/black_black_men.png'
                else:
                    self.ids.board_button_34.background_normal = 'img/black_white_men.png'

                self.ids.board_button_41.background_normal = 'img/black_blank.png'

                self.last_clicked_button = None

                print(self.board)

            else:
                print('Illegal move. Try again.')
        else:
            print('Select pawn first.')



    def king_move(self):
        pass

    def popup_box_new_game(self):
        popup_widget = FloatLayout()

        popup_label = Label(text="Do you want to start a new game?",
                            font_size=25,
                            size_hint=(None, None),
                            pos_hint={'x': .37, 'y': .5}
                            )
        button_yes = Button(text="Yes",
                            size_hint=(None, None),
                            width=200,
                            height=50,
                            pos_hint={'x': 0, 'y': .25}
                            )
        button_no = Button(text="No",
                           size_hint=(None, None),
                           width=200,
                           height=50,
                           pos_hint={'x': .5, 'y': .25}
                           )
        popup_widget.add_widget(popup_label)
        popup_widget.add_widget(button_yes)
        popup_widget.add_widget(button_no)

        popup_message = self.popup_box_message('New Game', popup_widget)
        popup_message.open()

        button_no.bind(on_release=popup_message.dismiss)
        button_yes.bind(on_release=lambda x: self.put_pawns_on_board())
        button_yes.bind(on_release=popup_message.dismiss)

    @staticmethod
    def popup_box_message(title, content):
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