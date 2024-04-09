from kivy.app import App
import random
from kivy.clock import Clock

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty, ListProperty
)

from kivy.core.window import Window
Window.size = (375, 667)

class MainApp(App):
    DICE_MAX = 6
    DICE_DEFAULT = "./asset/dice-roling.zip"

    isgame = BooleanProperty(False)
    loading = BooleanProperty(False)

    my_number = NumericProperty(random.randint(0,10))
    number_of_guess = NumericProperty(0)

    dice_image_source = StringProperty(DICE_DEFAULT)
    label_indicator = StringProperty("")
    last_label_indicator = StringProperty("")

    def guess(self) -> None:
        self.loading = True

        userguess = int(self.root.ids.userguess_input.text or 0)
        dice = random.randint(1, MainApp.DICE_MAX)
        self.dice_image_source = f"asset/dice/Dice {dice}.png"

        if self.my_number == userguess:
            self.label_indicator = "You Guess it right!!!"
            self.isgame = False

        else:
            iswithin = userguess-dice <= self.my_number <= userguess+dice
            self.label_indicator = f"My number is within {dice} away!" if iswithin else "Nope! No Clue! Ha Huh!?"

        self.number_of_guess+=1
        Clock.schedule_once(self.next_guess, 2)

    def next_guess(self, dt=-1) -> None:
        self.last_label_indicator = self.label_indicator
        self.label_indicator = ""
        self.root.ids.userguess_input.text = ""
        self.loading = False
        self.dice_image_source = MainApp.DICE_DEFAULT

    def start_game(self) -> None:
        self.isgame = True
        self.loading = True
        self.number_of_guess = 0

        userinput = [
            int(self.root.ids.minimum_bound.text or 0), 
            int(self.root.ids.maximum_bound.text or 10)
        ]
        self.my_number = random.randint(min(userinput), max(userinput))
        self.label_indicator = "" if userinput[0]<userinput[1] else "You enter the range wrongly, but thats okay!"
        Clock.schedule_once(self.next_guess, 2)

    def stop_game(self) -> None:
        self.isgame = False

if __name__ == "__main__":
    MainApp().run()