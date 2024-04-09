from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.clock import Clock

# Get number of dice
# Change src of each image 

import random

class RandomDiceApp(App):
    DICE_MAX = 6

    button_text = StringProperty("Rolling for 1 Dice")
    amount_text = StringProperty("Enter Number of Dice: ")
    result_text = StringProperty("Result = ")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_pool = []

        for _ in range(RandomDiceApp.DICE_MAX):
            image = Image(
                source="./asset/dice/Dice 1.png", 
                size_hint=[.45, None],
                size_hint_max = [150, 150]
            )
            image.height = image.width
            self.image_pool.append(image)
        Clock.schedule_once(self.prep_dice, -1)

    def slider_changes(self) -> None:
        amount = self.get_dice_amount()
        self.button_text = f"Rolling for {amount} of Dice{(amount>1)*'s'}"
        self.amount_text = f"Enter Number of Dice: {amount}"
        self.prep_dice()

    def prep_dice(self, dt=-1) -> None:
        layout = self.root.ids.right_side
        layout.clear_widgets()
        for i in range(self.get_dice_amount()):
            self.image_pool[i].source = "./asset/dice-roling.zip"
            self.image_pool[i]._coreimage._anim_index = i
            layout.add_widget(self.image_pool[i])
        self.root.ids.start_button.disabled = False

    def roll_button_click_fx(self) -> None:
        amount = self.get_dice_amount()
        ref = []
        for i in range(amount):
            num = self.get_dice_value()
            ref.append(num)
            self.image_pool[i].source = f"./asset/dice/Dice {num}.png"
        self.result_text = f"Result = {sum(ref)}"
        self.root.ids.start_button.disabled = True

    def get_dice_value(self) -> int:
        return random.randint(1, 6)

    def get_dice_amount(self) -> int:
        return self.root.ids.slider.value

if __name__ == '__main__':
    RandomDiceApp().run()