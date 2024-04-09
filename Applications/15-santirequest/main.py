from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import random

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty, ListProperty
)

from kivy.core.window import Window
Window.size = (375, 667)

class Piece(Button):
    piecevalue = NumericProperty(0)
    pieceposition = ListProperty([-1, -1])
    isselected = BooleanProperty(False)

    default_color = [.2, .2, .2, 1]
    color_mapping = {
        0:  default_color,
        1:  [1,0,0,1],
        2:  [0,1,0,1],
        3:  [0,0,1,1],
        4:  [0,1,1,1],
        5:  [1,0,1,1],
    }

    def reset(self) -> None:
        self.isselected = False

    def on_release(self):
        self.isselected = not self.isselected
        App.get_running_app().select_piece(self.pieceposition)
        return super().on_release()

class MainApp(App):
    ROWS = 5
    COLS = 5
    PIECE_TYPES = 5

    score = NumericProperty(0)
    number_of_move = NumericProperty(0)

    isgame = BooleanProperty(False)
    isloading = BooleanProperty(False)
    selected_piece = ListProperty([-1, -1])

    def reset_piece(self) -> None:
        piece: Piece
        for piece in self.root.ids.game_layout.children:
            piece.reset()
        self.selected_piece = [-1, -1]

    def select_piece(self, pieceposition) -> None:
        default = [-1, -1]
        if self.selected_piece==default:
            self.selected_piece = pieceposition
        else:
            if self.check_swap_position(*self.selected_piece, *pieceposition):
                self.swap_position(self.board, *self.selected_piece, *pieceposition)
            self.reset_piece()
            self.isloading = True
            self.check_combo()
            self.number_of_move += 1
            self.isloading = False

    def check_combo(self) -> None:
        piece = self.remove_combo_pieces(self.board)
        if piece:
            self.fall_down_and_refill(piece)
            self.check_combo()
            self.score += len(piece)
        self.refresh_layout()

    def swap_position(self, board, row0, col0, row1, col1) -> None:
        temp = board[row0][col0]
        board[row0][col0] = board[row1][col1]
        board[row1][col1] = temp

    def check_swap_position(self, row0, col0, row1, col1) -> bool:
        # assuming r0, c0 is current position and r1, c1 is next
        if 0 <= row1 < self.ROWS and 0 <= col1 < self.COLS:
            clone = [row[:] for row in self.board]
            self.swap_position(clone, row0, col0, row1, col1)
            return bool(self.remove_combo_pieces(clone))
        return False

    def remove_combo_pieces(self, board) -> set:
        pieces_to_remove = set()

        # Check for horizontal matches
        for row in range(self.ROWS):
            for col in range(self.COLS - 2):
                if board[row][col] == board[row][col + 1] == board[row][col + 2]:
                    pieces_to_remove.add((row, col))
                    pieces_to_remove.add((row, col + 1))
                    pieces_to_remove.add((row, col + 2))
        
        # Check for vertical matches
        for col in range(self.COLS):
            for row in range(self.ROWS - 2):
                if board[row][col] == board[row + 1][col] == board[row + 2][col]:
                    pieces_to_remove.add((row, col))
                    pieces_to_remove.add((row + 1, col))
                    pieces_to_remove.add((row + 2, col))

        # Remove pieces from the board
        for row, col in pieces_to_remove:
            board[row][col] = 0

        return pieces_to_remove

    def fall_down_and_refill(self, pieces_to_remove: set):
        for col in range(self.COLS):
            # Find the lowest empty space in the column
            empty_row = self.ROWS - 1
            while empty_row >= 0 and self.board[empty_row][col] != 0:
                empty_row -= 1
            
            # Move pieces down from above the empty space
            for row in range(empty_row - 1, -1, -1):
                if (row, col) not in pieces_to_remove:
                    self.board[empty_row][col] = self.board[row][col]
                    empty_row -= 1
            
            # Refill the empty spaces with random pieces
            for row in range(empty_row, -1, -1):
                self.board[row][col] = random.randint(1, self.PIECE_TYPES)

    def refresh_layout(self) -> None:
        layout: GridLayout = self.root.ids.game_layout
        layout.clear_widgets()

        for row in range(MainApp.ROWS):
            for col in range(MainApp.COLS):
                layout.add_widget(
                    Piece(
                        piecevalue=self.board[row][col],
                        pieceposition=[row,col]
                    )
                )

    def reshuffle_item(self) -> None:
        self.board = []
        for row in range(MainApp.ROWS):
            self.board.append([])
            for col in range(MainApp.COLS):
                self.board[row].append(random.randint(1,self.PIECE_TYPES))

    def start_game(self) -> None:
        self.isgame = True
        self.score = 0
        self.number_of_move = 0
        self.reshuffle_item()
        self.refresh_layout()
        self.check_combo()
        # Wait till player make move and make a move

    def stop_game(self) -> None:
        self.isgame = False
        # Player cannot move anything anymore

if __name__ == "__main__":
    MainApp().run()