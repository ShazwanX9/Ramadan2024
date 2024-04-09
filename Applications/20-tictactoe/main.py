from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty

from kivy.core.window import Window
Window.size = (375, 667)

class MainApp(App):
    isgame = BooleanProperty(False)
    isplayer1 = BooleanProperty(True)
    isplayer_vs_player = BooleanProperty(False)
    win_text = StringProperty("")

    PLAYER1 = "X"
    PLAYER2 = "O"
    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    def check_win(self, board, player):
        # Check rows and columns
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
            all(board[j][i] == player for j in range(3)):
                return True

        # Check diagonals
        if all(board[i][i] == player for i in range(3)) or \
        all(board[i][2-i] == player for i in range(3)):
            return True

        return False

    def check_draw(self, board) -> None:
        return not any(any(col=="" for col in row) for row in board)

    def click(self, btn, coor) -> None:
        player = self.PLAYER1 if self.isplayer1 else self.PLAYER2
        btn.text = player
        self.board[coor[0]][coor[1]] = player

        if self.check_win(self.board, player):
            self.win_text = f"{player} Win!"
            self.stop_game()
        if self.check_draw(self.board):
            self.win_text = f"Game Draw!"
            self.stop_game()

        self.isplayer1 = not self.isplayer1

    def start_game(self) -> None: 
        self.isgame = True
        for layout in self.root.ids.tictactoe.children:
            for btn in layout.children:
                btn.text = ""
        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.win_text = ""

    def stop_game(self) -> None: 
        self.isgame = False

if __name__ == "__main__":
    MainApp().run()