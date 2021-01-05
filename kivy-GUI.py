from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread

from kivy.core.window import Window

from checkers import Board, Pawn, King
from constants import BLACK, WHITE, BLANK_WHITE, BLANK_DARK, WHITE_PAWN, BLACK_KING, WHITE_KING, \
                      BLACK_PAWN, CLICKED_BLACK_PAWN, CLICKED_WHITE_PAWN, CLICKED_BLANK, ICON, \
                      CLICKED_BLACK_KING, CLICKED_WHITE_KING, AVAILABLE_MOVE


class CheckersLayout(Widget):

    def __init__(self):
        """
        Constructor for CheckersLayout class.
        """
        self.board = None
        self.bottom_color = None
        self.upper_color = None
        self.last_clicked_button = None
        self.board_button = {}
        self.init_buttons()
        self.turn = WHITE
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
                button.background_normal = BLANK_WHITE
                button.background_down = CLICKED_BLANK
            else:
                button = Button(text=f'{button_number}')
                button.background_normal = BLANK_DARK
                button.color = (1, 1, 1, 0)
                button.background_down = CLICKED_BLANK
            self.ids.buttons_widget.add_widget(button)
            self.board_button[button_number] = button

    def new_game(self, checkbox_1, checkbox_2):
        """
        When clicked initialize new game. Validate which color has been chosen. According to player
        choice puts black or white mens on bottom and upper part of the board.
        """

        if checkbox_1.active:
            self.bottom_color = BLACK
            self.upper_color = WHITE
            self.popup_box_new_game()

        elif checkbox_2.active:
            self.bottom_color = WHITE
            self.upper_color = BLACK
            self.popup_box_new_game()

        else:
            info_button = Button(text='Please choose a color first.',
                                 font_size=22,
                                 bold=True,
                                 background_normal=BLANK_WHITE,
                                 background_down=CLICKED_BLANK,
                                 color=(.231, .353, .553, 1),
                                 )
            popup_message = self.popup_box_message('Color Error', info_button)
            popup_message.open()
            info_button.bind(on_press=popup_message.dismiss)

    def create_starting_board(self):
        """
        Method which creates a backend board according to Board classes. Creates a frontend board
        in Kivy GUI and bind a self.board_field_clicked method to each button.
        """

        # Initialize backend board and reset turn.
        self.turn = WHITE
        self.board = Board(self.bottom_color)

        # Initialize frontend board.
        upper_starting_fields = [2, 4, 6, 8, 9, 11, 13, 15, 18, 20, 22, 24]
        bottom_starting_fields = [41, 43, 45, 47, 50, 52, 54, 56, 57, 59, 61, 63]
        middle_fields = [25, 27, 29, 31, 34, 36, 38, 40]

        if self.bottom_color == BLACK:
            for field_number in bottom_starting_fields:
                self.board_button[field_number].background_normal = BLACK_PAWN
                self.board_button[field_number].bind(on_press=self.board_field_clicked)
            for field_number in upper_starting_fields:
                self.board_button[field_number].background_normal = WHITE_PAWN
                self.board_button[field_number].bind(on_press=self.board_field_clicked)

        else:
            for field_number in bottom_starting_fields:
                self.board_button[field_number].background_normal = WHITE_PAWN
                self.board_button[field_number].bind(on_press=self.board_field_clicked)
            for field_number in upper_starting_fields:
                self.board_button[field_number].background_normal = BLACK_PAWN
                self.board_button[field_number].bind(on_press=self.board_field_clicked)

        for field_number in middle_fields:
            self.board_button[field_number].background_normal = BLANK_DARK
            self.board_button[field_number].bind(on_press=self.board_field_clicked)

    def board_field_clicked(self, pawn_instance):
        # TODO: might be better to use try, except clause?
        """
        Method validate:
            - if our move is in Pawn class method 'get_allowed_player_moves',
            - if selected button has been clicked,
            - if chosen move can be done according to self.last_button_clicked variable,

        After validation it makes a move on backend Board class using Board.make_men_move_on_board method.
        """
        button_number = int(pawn_instance.text)
        button_code = self.board.board[button_number]
        pawn_instance = self.board.field[button_code]

        if type(pawn_instance) == Pawn and self.last_clicked_button is None:
            if pawn_instance.color == self.turn:
                self.last_clicked_button = button_number
                self.select_field_gui(button_number, pawn_instance)
                self.highlight_available_moves(pawn_instance)

        elif type(pawn_instance) == King and self.last_clicked_button is None:
            if pawn_instance.color == self.turn:
                self.last_clicked_button = button_number
                self.select_field_gui(button_number, pawn_instance)
                self.highlight_available_moves(pawn_instance)

        elif self.last_clicked_button is not None:
            if isinstance(pawn_instance, Pawn):
                self.unchecked_selected_field()
            elif isinstance(pawn_instance, King):
                self.unchecked_selected_field()

            else:
                field_code = self.board.board[self.last_clicked_button]
                field_instance = self.board.field[field_code]
                if self.turn == self.bottom_color:
                    if type(field_instance) == Pawn:
                        allowed_moves = self.board.get_all_bottom_moves(self.last_clicked_button, self.turn)
                    else:
                        allowed_moves = self.board.get_king_allowed_moves(self.last_clicked_button)
                else:
                    if type(field_instance) == Pawn:
                        allowed_moves = self.board.get_all_upper_moves(self.last_clicked_button, self.turn)
                    else:
                        allowed_moves = self.board.get_king_allowed_moves(self.last_clicked_button)

                if button_number in allowed_moves:
                    current_code = self.board.board[self.last_clicked_button]
                    new_code = self.board.board[button_number]

                    if type(field_instance) == Pawn:
                        self.board.move_pawn(current_code, new_code, self.turn)
                    elif type(field_instance) == King:
                        self.board.move_king(current_code, new_code, self.turn)

                    self.validate_color_position(button_number, field_instance)
                    self.board_button[self.last_clicked_button].background_normal = BLANK_DARK
                    self.win()
                    self.king_validation()
                    self.last_clicked_button = None
                    self.reset_fields_on_board()
                    self.change_turn()

    def win(self):
        if self.board.win() == BLACK:
            info_button = Button(text='Black player win!',
                                 font_size=22,
                                 bold=True,
                                 background_normal=BLANK_WHITE,
                                 background_down=CLICKED_BLANK,
                                 color=(.231, .353, .553, 1),
                                 )
            popup_message = self.popup_box_message('Congratulation!', info_button)
            popup_message.open()
            info_button.bind(on_press=popup_message.dismiss)
        elif self.board.win() == WHITE:
            info_button = Button(text='White player win!.',
                                 font_size=22,
                                 bold=True,
                                 background_normal=BLANK_WHITE,
                                 background_down=CLICKED_BLANK,
                                 color=(.231, .353, .553, 1),
                                 )
            popup_message = self.popup_box_message('Congratulation!', info_button)
            popup_message.open()
            info_button.bind(on_press=popup_message.dismiss)

    def select_field_gui(self, button_number, instance_type):
        """
        Function which change a appearance of selected field on board.
        """
        if self.turn == BLACK:
            if type(instance_type) == King:
                self.board_button[button_number].background_normal = CLICKED_BLACK_KING
            elif type(instance_type) == Pawn:
                self.board_button[button_number].background_normal = CLICKED_BLACK_PAWN
        else:
            if type(instance_type) == King:
                self.board_button[button_number].background_normal = CLICKED_WHITE_KING
            elif type(instance_type) == Pawn:
                self.board_button[button_number].background_normal = CLICKED_WHITE_PAWN

    def highlight_available_moves(self, instance_type):
        """
        Function that takes all possible moves from selected field and highlight all
        possible moves on board.
        """
        if type(instance_type) == King:
            allowed_moves = self.board.get_king_allowed_moves(self.last_clicked_button)
        else:
            if self.bottom_color == BLACK:
                if self.turn == BLACK:
                    allowed_moves = self.board.get_all_bottom_moves(self.last_clicked_button, self.turn)
                else:
                    allowed_moves = self.board.get_all_upper_moves(self.last_clicked_button, self.turn)
            else:
                if self.turn == WHITE:
                    allowed_moves = self.board.get_all_bottom_moves(self.last_clicked_button, self.turn)
                else:
                    allowed_moves = self.board.get_all_upper_moves(self.last_clicked_button, self.turn)

        for field_number in allowed_moves:
            field_code = self.board.board[field_number]
            field_instance = self.board.field[field_code]
            if field_instance is None:
                self.board_button[field_number].background_normal = AVAILABLE_MOVE
            else:
                continue

    def reset_fields_on_board(self):
        white_fields = [1, 3, 5, 7, 10, 12, 14, 16, 17, 19, 21, 23, 26, 28, 30, 32,
                        33, 35, 37, 39, 42, 44, 46, 48, 49, 51, 53, 55, 58, 60, 62, 64]

        for field_number in range(1, 64):
            if field_number in white_fields:
                continue
            else:
                field_code = self.board.board[field_number]
                field_instance = self.board.field[field_code]

                if field_instance is None:
                    self.board_button[field_number].background_normal = BLANK_DARK
                else:
                    continue

    def check_if_jump_is_available(self):
        pass

    def unchecked_selected_field(self):
        """
        Function unchecked selected field.
        """
        if self.turn == BLACK:
            self.board_button[self.last_clicked_button].background_normal = BLACK_PAWN
            self.last_clicked_button = None
            self.reset_fields_on_board()
        else:
            self.board_button[self.last_clicked_button].background_normal = WHITE_PAWN
            self.last_clicked_button = None
            self.reset_fields_on_board()

    def king_validation(self):
        """
        Function which checks if any pawns on top and bottom row meet condition to become a King.
        """
        top_row = [2, 4, 6, 8]
        bottom_row = [57, 59, 61, 63]

        for field_number in top_row:
            button_code = self.board.board[field_number]
            pawn_instance = self.board.field[button_code]
            if self.bottom_color == BLACK:
                if pawn_instance is None:
                    continue
                elif isinstance(pawn_instance, King):
                    continue
                elif pawn_instance.color == BLACK:
                    self.board.change_pawn_to_king(field_number, BLACK)
                    self.change_pawn_to_king_gui(field_number)
            else:
                if pawn_instance is None:
                    continue
                elif isinstance(pawn_instance, King):
                    continue
                elif pawn_instance.color == WHITE:
                    self.board.change_pawn_to_king(field_number, WHITE)
                    self.change_pawn_to_king_gui(field_number)

        for field_number in bottom_row:
            button_code = self.board.board[field_number]
            pawn_instance = self.board.field[button_code]
            if self.bottom_color == BLACK:
                if pawn_instance is None:
                    continue
                elif isinstance(pawn_instance, King):
                    continue
                elif pawn_instance.color == WHITE:
                    self.board.change_pawn_to_king(field_number, WHITE)
                    self.change_pawn_to_king_gui(field_number)
            else:
                if pawn_instance is None:
                    continue
                elif isinstance(pawn_instance, King):
                    continue
                elif pawn_instance.color == BLACK:
                    self.board.change_pawn_to_king(field_number, BLACK)
                    self.change_pawn_to_king_gui(field_number)

    def change_pawn_to_king_gui(self, field_number):
        """
        A function that changes the appearance of a pawn to a king.
        """
        if self.turn == BLACK:
            self.board_button[field_number].background_normal = BLACK_KING
        else:
            self.board_button[field_number].background_normal = WHITE_KING

    def validate_color_position(self, button_number, instance_type):
        """
        Function which validate which side there is white and black color.
        """
        if self.bottom_color == BLACK:
            if self.turn == BLACK:
                self.gui_field_appearance(instance_type, button_number, BLACK)
            else:
                self.gui_field_appearance(instance_type, button_number, WHITE)
            self.jump_check(button_number, instance_type)

        else:
            if self.turn == BLACK:
                self.gui_field_appearance(instance_type, button_number, BLACK)
            else:
                self.gui_field_appearance(instance_type, button_number, WHITE)
            self.jump_check(button_number, instance_type)

    def gui_field_appearance(self, instance_type, button_number, color):
        """
        Function which show King or Pawn on new field.
        """
        if type(instance_type) is Pawn:
            if color == BLACK:
                self.board_button[button_number].background_normal = BLACK_PAWN
            else:
                self.board_button[button_number].background_normal = WHITE_PAWN
        else:
            if color == BLACK:
                self.board_button[button_number].background_normal = BLACK_KING
            else:
                self.board_button[button_number].background_normal = WHITE_KING

    def jump_check(self, button_number, instance_type):
        """
        Function that checks whether the move made has jumped the pawn.
        """
        skipped = self.last_clicked_button - button_number

        if type(instance_type) == Pawn:
            if skipped == 18:
                self.board_button[self.last_clicked_button - 9].background_normal = BLANK_DARK
                self.board.delete_pawn_or_king(self.last_clicked_button - 9)
                self.board.subtract_piece_from_board()
            elif skipped == 14:
                self.board_button[self.last_clicked_button - 7].background_normal = BLANK_DARK
                self.board.delete_pawn_or_king(self.last_clicked_button - 7)
                self.board.subtract_piece_from_board()
            elif skipped == -18:
                self.board_button[self.last_clicked_button + 9].background_normal = BLANK_DARK
                self.board.delete_pawn_or_king(self.last_clicked_button + 9)
                self.board.subtract_piece_from_board()
            elif skipped == -14:
                self.board_button[self.last_clicked_button + 7].background_normal = BLANK_DARK
                self.board.delete_pawn_or_king(self.last_clicked_button + 7)
                self.board.subtract_piece_from_board()

        elif type(instance_type) == King:
            print(skipped)

            # x = skipped % 7
            # y = skipped % 9
            #
            # field_code = self.board.board[button_number + 9]
            # field_instance = self.board.field[field_code]
            # field_type = type(field_instance)
            # if field_type == Pawn or field_type == King:
            #     self.board.delete_pawn_or_king(button_number + 9)
            #     self.board.subtract_piece_from_board()

            diagonal = skipped % 9
            opposite_diagonal = skipped % 7

            if diagonal == 0:
                if skipped > 0:
                    field_code = self.board.board[button_number + 9]
                    field_instance = self.board.field[field_code]
                    field_type = type(field_instance)
                    if field_type == Pawn or field_type == King:
                        self.board.delete_pawn_or_king(button_number + 9)
                        self.board.subtract_piece_from_board()

                elif skipped < 0:
                    field_code = self.board.board[button_number - 9]
                    field_instance = self.board.field[field_code]
                    field_type = type(field_instance)
                    if field_type == Pawn or field_type == King:
                        self.board.delete_pawn_or_king(button_number - 9)
                        self.board.subtract_piece_from_board()

            if opposite_diagonal == 0:
                if skipped > 0:
                    field_code = self.board.board[button_number + 7]
                    field_instance = self.board.field[field_code]
                    field_type = type(field_instance)
                    if field_type == Pawn or field_type == King:
                        self.board.delete_pawn_or_king(button_number + 7)
                        self.board.subtract_piece_from_board()

                elif skipped < 0:
                    field_code = self.board.board[button_number - 7]
                    field_instance = self.board.field[field_code]
                    field_type = type(field_instance)
                    if field_type == Pawn or field_type == King:
                        self.board.delete_pawn_or_king(button_number - 7)
                        self.board.subtract_piece_from_board()

    def king_jump_check(self):
        # new position +- 7,9 ?
        pass

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

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
        button_yes.bind(on_release=lambda x: self.create_starting_board())
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
    icon = ICON

    def build(self):
        Window.size = (1100, 1100)
        Window.clearcolor = (.655, .682, .682, 1)

        return CheckersLayout()


if __name__ == '__main__':
    CheckersApp().run()