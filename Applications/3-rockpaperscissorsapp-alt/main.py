from kivy.app import App
from kivy.clock import Clock
import random
from datetime import datetime, timedelta
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

class RockPaperScissorsApp(App):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    LEFT = "left"
    RIGHT = "right"
    LOADING = "loading"

    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

    is_game = BooleanProperty(False)
    is_player_1 = BooleanProperty(True)
    round_value = NumericProperty(1)
    score_value = NumericProperty(0)
    right_value = NumericProperty(0)
    wrong_value = NumericProperty(0)

    time_text = StringProperty("Time Taken: 00:00")
    p1_text = StringProperty("")
    p2_text = StringProperty("")
    p1_source = StringProperty("")
    p2_source = StringProperty("")
    player_turn_text = StringProperty("")
    player_turn_source = StringProperty("")

    combination = [
        (PAPER, ROCK),
        (ROCK, SCISSORS),
        (SCISSORS, PAPER)
    ]
    _turn_choice = [LEFT, RIGHT]
    _player_choice = [
        ROCK, PAPER, SCISSORS
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.now = datetime.now()
        self.timer = None
        self.loading()

    def start_game(self) -> None:
        self.is_game = True
        self.score_value = 0
        self.round_value = 0
        self.right_value = 0
        self.wrong_value = 0
        self.shuffle()
        self.start_timer()

    def stop_game(self) -> None:
        self.is_game = False
        self.loading()
        self.stop_timer()

    def start_timer(self) -> None: 
        self.stop_timer
        self.reset_time()
        self.timer = Clock.schedule_interval(self.update_clock, 1)

    def stop_timer(self) -> None:
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def get_time_seconds(self) -> int:
        return self.now.timestamp() - self.now_timestamp

    def reset_time(self) -> None:
        self.now = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.now_timestamp = self.now.timestamp()
        self.time_text = "Time Taken: 00:00"

    def update_clock(self, dt=-1) -> None:
        self.now = self.now + timedelta(seconds = 1)
        self.time_text = f"Time Taken: {self.now.strftime('%M:%S')}"

    def loading(self) -> None:
        self.p1_text = RockPaperScissorsApp.LOADING
        self.p2_text = RockPaperScissorsApp.LOADING
        self.player_turn_text = RockPaperScissorsApp.LOADING
        self.setup()

    def shuffle(self) -> None:
        self.p1_text = random.choice(self._player_choice)
        self.p2_text = random.choice(self._player_choice)
        self.player_turn_text = random.choice(self._turn_choice)
        self.setup()

    def setup(self) -> None:
        self.p1_source = "./asset/"+self.p1_text+".png"
        self.p2_source = "./asset/"+self.p2_text+".png"
        self.player_turn_source = "./asset/"+self.player_turn_text+".png"
        self.is_player_1 = (self.player_turn_text==RockPaperScissorsApp.LEFT)

    def calculate_score(self, option) -> None:
        # Decide if draw or contest
        # Default 0 if draw
        win = int(self.p1_text!=self.p2_text)

        # Decide if Player 1 win or lose
        # self.p1_text vs self.p2_text
        if win: win = (-1, 1)[(self.p1_text, self.p2_text) in RockPaperScissorsApp.combination]

        # Invert the player if player 2
        if (not self.is_player_1) and win: win = -win

        points = (
            option == RockPaperScissorsApp.WIN and win == 1, 
            option == RockPaperScissorsApp.DRAW and win == 0, 
            option == RockPaperScissorsApp.LOSE and win == -1, 
        )

        scores = {
            0<=self.get_time_seconds()<3: 100,
            3<=self.get_time_seconds()<7: 50,
            7<=self.get_time_seconds()<15: 25,
        }

        score = scores.get(True, 0)
        self.score_value += any(points)*score
        self.right_value += any(points)
        self.wrong_value += not any(points)

    def decide(self, option) -> None:
        self.stop_timer()
        self.calculate_score(option=option)
        self.loading()
        self.reset_time()
        self.shuffle()
        self.start_timer()
        self.round_value += 1

if __name__ == '__main__':
    RockPaperScissorsApp().run()