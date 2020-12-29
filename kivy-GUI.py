from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread

from kivy.core.window import Window

from CheckersClasses import Board, Pawn


class CheckersLayout(Widget):

    def __init__(self):
        self.board = None
        self.bottom_color = None
        self.upper_color = None
        self.last_clicked_button = None
        self.board_button = {}
        self.init_buttons()
        self.turn = 'white'
        super(CheckersLayout, self).__init__()

    @mainthread
    def init_buttons(self):
        """
            Method which initialize 64 buttons which create a 8x8 board for checkers game.
        """
        white_fields = [1, 3, 5, 7, 10, 12, 14, 16, 17, 19, 21, 23, 26, 28, 30, 32,
                        33, 35, 37, 39, 42, 44, 46, 48, 49, 51, 53, 55, 58, 60, 62, 64]
        for button_number in range(1, 65):
            if button_number in white_fields:
                button = Button()
                button.background_normal = 'img/white_blank.png'
                button.background_down = 'img/clicked.png'
            else:
                button = Button(text=f'{button_number}')
                button.background_normal = 'img/black_blank.png'
                button.color = (1, 1, 1, 0)
                button.background_down = 'img/clicked.png'
            self.ids.buttons_widget.add_widget(button)
            self.board_button[button_number] = button

    def new_game(self, checkbox_1, checkbox_2):
        """
            When clicked initialize new game. Validate which color has been chosen. According to player
            choice puts black or white mens on bottom and upper part of the board.
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
        """
            Method which creates a backend board according to Board classes. Creates a frontend board
            in Kivy GUI and bind a self.board_field_clicked method to each button.
        """

        # Initialize backend board and reset turn.
        self.turn = 'white'
        self.board = Board(self.bottom_color)

        # Initialize frontend board.
        upper_starting_fields = [2, 4, 6, 8, 9, 11, 13, 15, 18, 20, 22, 24]
        bottom_starting_fields = [41, 43, 45, 47, 50, 52, 54, 56, 57, 59, 61, 63]
        middle_fields = [25, 27, 29, 31, 34, 36, 38, 40]

        if self.bottom_color == 'black':
            for field_number in bottom_starting_fields:
                self.board_button[field_number].background_normal = 'img/black_black_men.png'
                self.board_button[field_number].bind(on_press=self.board_field_clicked)
            for field_number in upper_starting_fields:
                self.board_button[field_number].background_normal = 'img/black_white_men.png'
                self.board_button[field_number].bind(on_press=self.board_field_clicked)

        else:
            for field_number in bottom_starting_fields:
                self.board_button[field_number].background_normal = 'img/black_white_men.png'
                self.board_button[field_number].bind(on_press=self.board_field_clicked)
            for field_number in upper_starting_fields:
                self.board_button[field_number].background_normal = 'img/black_black_men.png'
                self.board_button[field_number].bind(on_press=self.board_field_clicked)

        for field_number in middle_fields:
            self.board_button[field_number].background_normal = 'img/black_blank.png'
            self.board_button[field_number].bind(on_press=self.board_field_clicked)

    def board_field_clicked(self, button_instance):
        """
            Method validate:
                - if our move is in Men class method 'get_allowed_player_moves',
                - if selected button has been clicked,
                - if chosen move can be done according to self.last_button_clicked variable,

            After validation it makes a move on backend Board class using Board.make_men_move_on_board method.
        """

        button_number = int(button_instance.text)
        button_code = self.board.board[button_number]
        button_instance = self.board.field[button_code]

        if isinstance(button_instance, Pawn) and self.last_clicked_button is None:
            if button_instance.color == self.turn:
                if self.turn == 'black':
                    print('first black')
                    self.last_clicked_button = button_number
                    self.board_button[button_number].background_normal = 'img/trans_black.png'
                else:
                    print('first white')
                    self.last_clicked_button = button_number
                    self.board_button[button_number].background_normal = 'img/trans_white.png'

        elif self.last_clicked_button is not None:
            if isinstance(button_instance, Pawn):
                if self.turn == 'black':
                    print('middle black')
                    self.board_button[self.last_clicked_button].background_normal = 'img/black_black_men.png'
                    self.last_clicked_button = None
                else:
                    print('middle white')
                    self.board_button[self.last_clicked_button].background_normal = 'img/black_white_men.png'
                    self.last_clicked_button = None
            else:
                if self.turn == self.bottom_color:
                    print('allowed bottom')
                    allowed_moves = Pawn.get_allowed_bottom_moves(self.last_clicked_button, button_number)
                else:
                    print('allowed top')
                    allowed_moves = Pawn.get_allowed_upper_moves(self.last_clicked_button, button_number)

                if button_number in allowed_moves:
                    current_code = self.board.board[self.last_clicked_button]
                    new_code = self.board.board[button_number]
                    self.board.make_pawn_move_on_board(current_code, new_code, self.turn)

                    if self.turn == 'black':
                        self.board_button[button_number].background_normal = 'img/black_black_men.png'
                        print('end black')
                    else:
                        self.board_button[button_number].background_normal = 'img/black_white_men.png'
                        print('end white')

                    self.board_button[self.last_clicked_button].background_normal = 'img/black_blank.png'
                    self.last_clicked_button = None
                    self.change_turn()
                    print('end')

    def get_board(self):
        return self.board

    # def ai_move(self, board):
    #     self.board = board

    def change_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

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