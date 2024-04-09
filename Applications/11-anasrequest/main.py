from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors.button import ButtonBehavior

import random

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty, ListProperty
)

from kivy.core.window import Window
Window.size = (375, 667)

class Liquid(Label):
    value = NumericProperty(0)

    default_color = [.2, .2, .2, 1]
    color_mapping = {
        0:  default_color,
        1:  [1,0,0,1],
        2:  [0,1,0,1],
        3:  [0,0,1,1],
        4:  [0,1,1,1],
        5:  [1,0,1,1],
    }

class Bottle(ButtonBehavior, BoxLayout):
    max_capacity = NumericProperty(5)
    index = NumericProperty(-1)
    select_fx = ObjectProperty(-1)

    def on_release(self):
        self.select_fx(self)
        return super().on_release()

class GameMechanics(StackLayout):
    selected_layout = NumericProperty(-1)
    liquid_index = NumericProperty(-1)
    isgame = BooleanProperty(False)
    max_capacity = NumericProperty(5)

    def is_winning(self) -> None:
        return all(all(data==row[0] or data==0 for data in row) for row in self.gamedata)

    def refresh_layout(self) -> None:
        self.clear_widgets()
        for i,data in enumerate(self.gamedata):
            bottle = Bottle()
            bottle.index = i
            bottle.select_fx = self.select_layout
            bottle.max_capacity = self.max_capacity
            self.add_widget(bottle)

            for j,value in enumerate(data):
                liquid = Liquid()
                liquid.value=value
                bottle.add_widget(liquid, index=j)

    def get_top_most(self, index) -> int:
        idx = len(self.gamedata[index])-1
        while idx>=0 and not self.gamedata[index][idx]:
            idx-=1
        return idx

    def has_space(self, index) -> bool:
        return len(self.gamedata[index])-1>self.get_top_most(index)

    def select_layout(self, layout: Bottle) -> None:
        if self.isgame:
            if self.selected_layout==-1 and self.get_top_most(layout.index)>=0:
                layout.isselected = True
                self.selected_layout = layout.index
                self.liquid_index = self.get_top_most(layout.index)
            else:
                if self.selected_layout>-1 and self.selected_layout!=layout.index and self.has_space(layout.index):
                    value = self.gamedata[self.selected_layout][self.liquid_index]
                    # Change move only if topmost empty or same value
                    if self.gamedata[layout.index][self.get_top_most(layout.index)] == value or self.gamedata[layout.index][self.get_top_most(layout.index)]==0:
                        self.gamedata[layout.index][self.get_top_most(layout.index)+1] = value
                        self.gamedata[self.selected_layout][self.liquid_index] = 0

                if self.is_winning(): self.isgame = False
                self.refresh_layout()
                self.selected_layout = -1
        if not self.isgame:
            for data in self.children:
                data.disabled = True

    def create_game(self, gamedata) -> None:
        self.isgame = True
        self.gamedata = gamedata
        self.refdata = [data[:] for data in gamedata]
        self.max_capacity = len(self.gamedata)
        self.refresh_layout()

    def reset_game(self) -> None:
        self.isgame = True
        self.gamedata = [data[:] for data in self.refdata]
        self.refresh_layout()

class AnasGameApp(App):
    def __init__(self, gamedatas:list[list[list]]=[], **kwargs):
        super().__init__(**kwargs)
        self.gamedatas = gamedatas
        # Clock.schedule_once(self.start_game, 1)

    def reset_game(self) -> None:
        self.root.game_mechanics.reset_game()

    def new_game(self) -> None:
        # deepcopy
        self.cur_gamedata = [data[:] for data in random.choice(self.gamedatas)]
        self.start_game()

    def start_game(self, dt=-1) -> None:
        self.root.game_mechanics.create_game(self.cur_gamedata)

if __name__ == "__main__":
    AnasGameApp(gamedatas=[
        [
            [1,1,3],
            [2,2,3],
            [0,0,0],
        ],
        [
            [2,1,3,4,5],
            [1,1,3,4,5],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ]
    ]).run()