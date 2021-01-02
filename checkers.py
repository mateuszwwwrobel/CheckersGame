from constants import BLACK, WHITE


class Board:
    """ Checkers Board class which is 8x8(64 fields) board to play checkers created...
        It is played on an 8×8 chequered board with 12 pieces per side.

        - self.board store a field code as a string, for example: '1A'
        - self.field store a field status, could be: None, Men or King.

    """

    def __init__(self, color):
        self.bottom_color = color
        if self.bottom_color == WHITE:
            self.upper_color = BLACK
        else:
            self.upper_color = WHITE
        self.board = {}
        self.field = {}
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0

        self.init_board()

    def __str__(self):
        board_field_code = []
        board_field_status = []

        for field_code in self.board.values():
            board_field_code.append(field_code)

        for field_status in self.field.values():
            board_field_status.append(field_status)

        printable_field_list = []
        for code, status in zip(board_field_code, board_field_status):
            printable_field = str(code) + ':' + str(status)
            printable_field_list.append(printable_field)

        row_line = 110 * '-'

        row_1 = str(printable_field_list[:8])
        row_2 = str(printable_field_list[8:16])
        row_3 = str(printable_field_list[16:24])
        row_4 = str(printable_field_list[24:32])
        row_5 = str(printable_field_list[32:40])
        row_6 = str(printable_field_list[40:48])
        row_7 = str(printable_field_list[48:56])
        row_8 = str(printable_field_list[56:64])

        printable_board = ( row_line + '\n' + row_1 + '\n' +
                            row_line + '\n' + row_2 + '\n' +
                            row_line + '\n' + row_3 + '\n' +
                            row_line + '\n' + row_4 + '\n' +
                            row_line + '\n' + row_5 + '\n' +
                            row_line + '\n' + row_6 + '\n' +
                            row_line + '\n' + row_7 + '\n' +
                            row_line + '\n' + row_8 + '\n' +
                            row_line
                             )

        return printable_board

    def init_board(self):
        """ Initialize 8x8 board for english draughts(checkers) variation.

        """

        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        rows = ['1', '2', '3', '4', '5', '6', '7', '8']

        positions = [(row, column)for row in reversed(rows) for column in columns]

        for field_number, position in zip(range(1, 65), positions):
            self.field[''.join(position)] = None
            self.board[field_number] = ''.join(position)

        # Initialize a starting positions for white and black men.
        upper_starting_fields = []
        [upper_starting_fields.append(field) for field in self.field.keys()]
        upper_starting_fields = (upper_starting_fields[1:8:2] +
                                 upper_starting_fields[8:16:2] +
                                 upper_starting_fields[17:24:2]
                                 )

        bottom_starting_fields = []
        [bottom_starting_fields.append(field) for field in self.field.keys()]
        bottom_starting_fields = (bottom_starting_fields[40:48:2] +
                                  bottom_starting_fields[49:56:2] +
                                  bottom_starting_fields[56:64:2]
                                  )

        for upper_field, bottom_field in zip(upper_starting_fields, bottom_starting_fields):

            if self.bottom_color == WHITE:
                self.field[upper_field] = Pawn(BLACK)
                self.field[bottom_field] = Pawn(WHITE)
            else:
                self.field[upper_field] = Pawn(WHITE)
                self.field[bottom_field] = Pawn(BLACK)

    def move_pawn(self, current_position, new_position, color):
        self.field[current_position] = None

        current_field_number = list(self.board.keys())[list(self.board.values()).index(current_position)]
        new_field_number = list(self.board.keys())[list(self.board.values()).index(new_position)]

        if Pawn.get_all_allowed_bottom_moves(current_field_number, new_field_number) and self.field[new_position] is None:
            if color == WHITE:
                self.field[new_position] = Pawn(WHITE)
            else:
                self.field[new_position] = Pawn(BLACK)

    def win(self):
        """
            Return white or black string value to determine if player win.
        """

        if self.white_left <= 0:
            return WHITE
        elif self.black_left <= 0:
            return BLACK

        return None

    def delete_pawn_or_king(self, field_number):
        """
            Delete pawn or king from a board.
        """
        field_code = self.board[field_number]

        self.field[field_code] = None
        return field_code

    def change_pawn_to_king(self, field_number, color):
        """
            Change pawn to king.
        """
        field_code = self.board[field_number]
        self.field[field_code] = King(color)


class Pawn:
    """
        Create a men which could be either black or white. Can be assign to a self.field variable.

    """

    color = [BLACK, WHITE]

    def __init__(self, pawn_color):
        if pawn_color in self.color:
            self.color = pawn_color
        else:
            self.color = ''

    def __str__(self):
        return f"{self.color.capitalize()} Pawn"

    @staticmethod
    def get_all_allowed_bottom_moves(current_field_number, new_field_number):
        allowed_moves = []

        right_border = [8, 16, 24, 32, 40, 48, 56, 64]
        left_border = [1, 9, 17, 25, 33, 41, 49, 57]

        if current_field_number in left_border:
            allowed_moves.append(current_field_number - 7)
            allowed_moves.append(current_field_number - 14)
        elif current_field_number in right_border:
            allowed_moves.append(current_field_number - 9)
            allowed_moves.append(current_field_number - 18)
        else:
            allowed_moves.append(current_field_number - 7)
            allowed_moves.append(current_field_number - 9)
            allowed_moves.append(current_field_number - 14)
            allowed_moves.append(current_field_number - 18)

        if new_field_number in allowed_moves:
            return allowed_moves
        else:
            return allowed_moves

    @staticmethod
    def get_all_allowed_upper_moves(current_field_number, new_field_number):
        allowed_moves = []

        right_border = [8, 16, 24, 32, 40, 48, 56, 64]
        left_border = [1, 9, 17, 25, 33, 41, 49, 57]

        if current_field_number in left_border:
            allowed_moves.append(current_field_number + 9)
            allowed_moves.append(current_field_number + 18)
        elif current_field_number in right_border:
            allowed_moves.append(current_field_number + 7)
            allowed_moves.append(current_field_number + 14)
        else:
            allowed_moves.append(current_field_number + 7)
            allowed_moves.append(current_field_number + 14)
            allowed_moves.append(current_field_number + 9)
            allowed_moves.append(current_field_number + 18)

        if new_field_number in allowed_moves:
            return allowed_moves
        else:
            return allowed_moves


class King(Pawn):
    """
        Create a king which could be either black or white. Can be assign to a self.field variable.

    """

    color = [BLACK, WHITE]

    def __init__(self, king_color):
        super().__init__(king_color)

    def __str__(self):
        return f"{self.color.capitalize()} King"

    def get_all_allowed_moves(self, current_position):
        allowed_moves = []

        top_row = [1, 2, 3, 4, 5, 6, 7, 8]
        bottom_row = [57, 58, 59, 60, 61, 62, 63, 64]

        pass


if __name__ == '__main__':
    print("\nHello Checkers!\n")
    board = Board('black')

    white_men = Pawn('white')
    # print(white_men)
    black_men = Pawn('black')
    # print(black_men.color)
    # print(type(black_men.color))
    # print(white_men.color)
    # print(black_men)

    board.move_pawn('3A', '4B', black_men.color)
    # board.make_men_move_on_board('3A', '4B', black_men.color)
    # board.make_men_move_on_board('6H', '5G', white_men.color)
    # board.make_men_move_on_board('4B', '5C', black_men.color)
    # board.make_men_move_on_board('5C', '6D', black_men.color)
    # board.change_pawn_to_king('4B', BLACK)

    board.delete_pawn_or_king(34)

    print(board)

    # black_King = King('white')
    # print(black_King)