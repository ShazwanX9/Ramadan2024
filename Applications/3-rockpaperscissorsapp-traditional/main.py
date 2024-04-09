from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random
from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty
)

class RockPaperScissorsApp(App):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    SPOCK = "spock"
    LIZARD = "lizard"
    LOADING = "loading"

    ROCK_PAPER_SCISSORS = 0
    ROCK_PAPER_SCISSORS_SPOCK_LIZARD = 1

    win_count = NumericProperty(0)
    draw_count = NumericProperty(0)
    lose_count = NumericProperty(0)

    p1_text = StringProperty("")
    p2_text = StringProperty("")
    p1_source = StringProperty("")
    p2_source = StringProperty("")
    player_turn_text = StringProperty("")
    player_turn_source = StringProperty("")

    _game_mode = NumericProperty(0)
    default_layout = ObjectProperty()

    _combination = [
        [
            (PAPER, ROCK),
            (ROCK, SCISSORS),
            (SCISSORS, PAPER)
        ],
        [
            (PAPER, ROCK),
            (ROCK, SCISSORS),
            (SCISSORS, PAPER),
            (ROCK, LIZARD),
            (LIZARD, SPOCK),
            (SPOCK, SCISSORS),
            (SCISSORS, LIZARD),
            (LIZARD, PAPER),
            (PAPER, SPOCK),
            (SPOCK, ROCK),
        ]
    ]
    _player_choice = [
        [ ROCK, PAPER, SCISSORS ],
        [ ROCK, PAPER, SCISSORS, SPOCK, LIZARD ],
    ]

    def __init__(self, gamemode=0, **kwargs):
        super().__init__(**kwargs)
        self._game_mode = gamemode
        self.default_layout = BoxLayout(orientation="vertical")
        self.default_layout.add_widget(
            Button(text="Change Mode", on_release=lambda _: self.change_mode(int(not self._game_mode)))
        )
        self.default_layout.add_widget(
            Button(text="Quit Game", on_release=self.stop)
        )
        Clock.schedule_once(self._load_item, 1)
        Clock.schedule_once(self._loading, 1)

    def button_fx(self, action: str) -> None:
        for button in self.root.ids.button_holder.children:
            if button!=self.default_layout:
                button.disabled = True

        self.p1_text = action
        self.p2_text = random.choice(self._player_choice[self._game_mode])
        self._setup()

        win = int(self.p1_text!=self.p2_text)
        if win: win = (-1, 1)[(self.p1_text, self.p2_text) in RockPaperScissorsApp._combination[self._game_mode]]

        self.win_count += win==1
        self.draw_count += win==0
        self.lose_count += win==-1

        Clock.schedule_once(self._loading, 2)

    def _loading(self, dt=-1) -> None:
        for button in self.root.ids.button_holder.children:
            if button!=self.default_layout:
                button.disabled = False
        self.p1_text = RockPaperScissorsApp.LOADING
        self.p2_text = RockPaperScissorsApp.LOADING
        self._setup()

    def _setup(self) -> None:
        # Im too lazy for the images lol
        p1extension = [".png", ".jpg"][self.p1_text in (RockPaperScissorsApp.SPOCK, RockPaperScissorsApp.LIZARD)]
        p2extension = [".png", ".jpg"][self.p2_text in (RockPaperScissorsApp.SPOCK, RockPaperScissorsApp.LIZARD)]
        self.p1_source = "./asset/"+self.p1_text+p1extension
        self.p2_source = "./asset/"+self.p2_text+p2extension

    def change_mode(self, mode: int) -> None:
        self._game_mode = mode
        self._load_item()

    def _load_item(self, dt=-1) -> None:
        self.root.ids.button_holder.clear_widgets()
        for choice in self._player_choice[self._game_mode]:
            btn = Button(text=choice, on_release=lambda _, choice=choice: self.button_fx(choice))
            self.root.ids.button_holder.add_widget(btn)
        self.root.ids.button_holder.add_widget(self.default_layout)

if __name__ == '__main__':
    RockPaperScissorsApp().run()