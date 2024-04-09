from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

import random

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty
)

from kivy.core.window import Window
Window.size = (375, 667)

class GameUI(BoxLayout):
    moneyvalue = NumericProperty(10000)
    betvalue = NumericProperty(0)
    iswinning = BooleanProperty(False)
    isgame = BooleanProperty(False)

    bot = ObjectProperty()
    player = ObjectProperty()
    card_source = [
        "./asset/baby1.png",
        "./asset/baby2.png",
    ]

    def start_game(self) -> None:
        self.isgame = True
        self.bot.cardvalue = 0
        self.player.cardvalue = 0
        self.drawn_card(self.bot)
        self.drawn_card(self.bot)
        self.drawn_card(self.player)
        self.drawn_card(self.player)

    def drawn_card(self, player) -> None:
        card = random.randint(1,2)
        player.cardvalue += card
        player.hand.add_widget(Image(
            source=self.card_source[card-1],
            size_hint = [None, None],
            size = [55, 75]
        ))

    def clear_hand(self, player) -> None:
        player.hand.clear_widgets()

    def player_hit(self) -> None:
        self.drawn_card(self.player)
        if self.player.cardvalue > 5:
            self.compute_game()

    def bot_hit(self, dt=-1) -> None:
        if self.player.cardvalue<=5 and self.player.cardvalue>=self.bot.cardvalue:
            self.drawn_card(self.bot)
        if self.player.cardvalue<=5 and self.player.cardvalue>=self.bot.cardvalue:
            Clock.schedule_once(self.bot_hit, 1)
        else:
            self.iswinning = (
                self.player.cardvalue<=5 and 
                (self.bot.cardvalue>5 or 
                self.player.cardvalue>=self.bot.cardvalue)
            )
            Clock.schedule_once(self.stop_game, 1)

    def compute_game(self) -> None:
        self.isgame = False
        self.bot_hit()

    def stop_game(self, dt=-1) -> None:
        # Update Money
        self.moneyvalue += self.betvalue*2*self.iswinning
        self.betvalue = 0
        self.clear_hand(self.bot)
        self.clear_hand(self.player)

    def clear_bet(self) -> None:
        self.moneyvalue += self.betvalue
        self.betvalue = 0

    def bet(self, value: int) -> None:
        self.betvalue += value
        self.moneyvalue -= value

class BabyBlackjackApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return GameUI()

if __name__ == "__main__":
    BabyBlackjackApp().run()