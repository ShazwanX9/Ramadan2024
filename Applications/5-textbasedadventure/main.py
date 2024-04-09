from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.audio import SoundLoader

import random

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty
)

class ScoreScreen(BoxLayout):
    _coinpath = StringProperty("./asset/coin.zip")
    _drinkpath = StringProperty("./asset/drink.zip")

    def reset(self) -> None:
        for image in self.ids.drinkimages.children:
            image.reload()

class GameGrid(GridLayout):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

    NOT_WALKABLE = 0
    WALKABLE = 1
    MONSTER = 2
    TREASURE = 3
    PLAYER = 8
    UNKNOWN = 9

    _vinespath = "./asset/vines.zip"
    _coinpath = "./asset/coin.zip"
    _playerpath = "./asset/player.zip"
    _monsterpath = "./asset/monster.zip"
    _unknownpath = "./asset/unknown.png"
    _normalpath = "./asset/normal.png"

    imagemap = {
        WALKABLE: _normalpath,
        NOT_WALKABLE: _vinespath,
        MONSTER: _monsterpath,
        TREASURE: _coinpath,
        PLAYER: _playerpath,
        UNKNOWN: _unknownpath,
    }

    refmap = []
    gamemap = []
    player_x = NumericProperty(0)
    player_y = NumericProperty(0)

    GRID_SIZE = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def stop(self) -> None:
        self.refmap.clear()
        self.clear_widgets()

    def setup(self, gamemap:list[list[int]]) -> None:
        self.rows = len(gamemap)
        self.cols = len(gamemap[0])
        self.gamemap = gamemap

        self.stop()
        for i, row in enumerate(self.gamemap):
            self.refmap.append([])
            for item in row:
                image = Image(
                    source=self._unknownpath, 
                    anim_delay=-1, 
                    size_hint=[None, None], 
                    size=[self.GRID_SIZE,self.GRID_SIZE]
                )
                image.anim_index=random.randint(0,1)
                self.add_widget(image)
                self.refmap[i].append(image)

        self.set_player_pos(0, 0)
        self.move_player_pos(0, 0)

    def get_player_heading(self, direction) -> list[int,int]:
        if direction == self.UP:
            x,y = self.player_x, self.player_y-1
        elif direction == self.RIGHT:
            x,y = self.player_x+1, self.player_y
        elif direction == self.DOWN:
            x,y = self.player_x, self.player_y+1
        elif direction == self.LEFT:
            x,y = self.player_x-1, self.player_y
        return x,y

    def is_possiblepath(self, row: int, col: int) -> bool:
        return row<self.rows and col<self.cols \
            and (
                self.is_item(row, col, self.WALKABLE) \
                    or self.refmap[row][col].source==self._unknownpath
            )

    def is_player_possiblepath(self, direction: str) -> bool:
        x,y = self.get_player_heading(direction)
        return x>=0 and y>=0 and self.is_possiblepath(y,x)

    def get_item(self, row: int, col: int) -> int:
        if row<self.rows and col<self.cols:
            return self.gamemap[row][col]

    def is_item(self, row: int, col: int, item: int) -> bool:
        return row<self.rows and col<self.cols and self.gamemap[row][col] == item

    def reveal(self, row: int, col: int) -> None:
        image = self.imagemap.get(self.gamemap[row][col])
        self.refmap[row][col].source = image

        if image == self._vinespath: self.refmap[row][col].anim_delay = -1
        if image == self._coinpath: self.refmap[row][col].anim_delay = 1/12
        if image == self._monsterpath: self.refmap[row][col].anim_delay = 1/4
        if image == self._normalpath: self.refmap[row][col].anim_delay = -1

    def get_player_pos(self) -> list[int, int]:
        return self.player_x, self.player_y

    def set_player_pos(self, row: int, col: int) -> None:
        self.player_x = col
        self.player_y = row

    def move_player_pos(self, row: int, col: int, block=False) -> None:
        self.refmap[self.player_y][self.player_x].source = [self._normalpath, self._vinespath][block]
        self.set_player_pos(row, col)
        self.refmap[self.player_y][self.player_x].source = self._playerpath
        self.refmap[self.player_y][self.player_x].anim_delay = 1/4

class ControllerLayout(BoxLayout):
    north_text = StringProperty("North")
    west_text = StringProperty("West")
    east_text = StringProperty("East")
    south_text = StringProperty("South")

    north_btn_fx = ObjectProperty()
    west_btn_fx = ObjectProperty()
    east_btn_fx = ObjectProperty()
    south_btn_fx = ObjectProperty()

    north_active = BooleanProperty(False)
    west_active = BooleanProperty(False)
    east_active = BooleanProperty(False)
    south_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._gamegrid = None

    def set_btn_fx(self, btn_fx, fx) -> None:
        setattr(self, btn_fx, fx)

class GameUI(RelativeLayout):
    _lose_life = "\n\nLOSE 1 ENERGY DRINK"
    _gain_gold = "\n\nGAIN 1000 GOLD COIN"

    player_dialog_list = {
        "0": [
            "These vines look thick and tangled. I cannot cut through them.",
            "The vines block my path like a living barrier. I'll have to find a way around or over them.",
            "Ah, these vines seem to have a mind of their own, twisting and turning to block my way.",
            "The vines are dense and thorny, need to find the other way.",
            "Looks like I'll have to hack my way through these vines if I want to continue forward. Or perhaps I should reconsider my path..."
        ],
        "1": [
            "The path seems clear ahead. Let's keep moving forward.",
            "I don't see any obstacles in my way. Onward I go!",
            "moves like smooth sailing from here. Time to press on.",
            "No walls blocking my path. I'll just keep walking.",
            "Seems like I'm on the right track. Better keep going."
        ],
        "2": [
            "By the ancient trees! A green forest slime blocks my path! I must flee before it engulfs me!"+_lose_life,
            "Yikes, a forest slime! Its gelatinous form oozes with danger. I must avoid it!"+_lose_life,
            "A lone forest slime awaits! I must find another route to avoid its acidic touch."+_lose_life,
            "I've stumbled upon a forest slime. Time to retreat and regroup before it catches me!"+_lose_life,
            "A vile forest slime stands in my way. I must flee to safety before it devours me!"+_lose_life
        ],
        "3": [
            "By the ancient gods! I've found a mystical staff! Onward to more riches!"+_gain_gold,
            "Hooray! I've uncovered a jewel-encrusted sword. Now, where's the next one?"+_gain_gold,
            "At last, a magical bow! My quest is off to a great start. More riches await!"+_gain_gold,
            "I've struck gold! Literally! Time to stash away this loot."+_gain_gold,
            "Treasure! A chest filled with magical artifacts! My journey has just begun!"+_gain_gold
        ]
    }

    game_available_text = "Behold! Let the adventure commence!"
    game_not_available_text = "Alas! There is no map to embark upon our epic quest!"
    win_text = "I believe I've had my fill of adventure for today! But fear not, for the tales of my triumph shall echo through the ages."
    gameover_text = "Alas, my energy wanes like the dying embers of a once-blazing fire... Perhaps this is the end of my adventure for today."

    gamegrid = ObjectProperty(GameGrid)
    controller = ObjectProperty(ControllerLayout)
    scorescreen = ObjectProperty(GameGrid)

    isgame = BooleanProperty(False)
    player_health = NumericProperty(3)
    player_score = NumericProperty(0)
    total_treasure = NumericProperty(0)
    treasure_value = NumericProperty(1000)
    player_dialog = StringProperty("The Player is on Adventure!")

    sound = SoundLoader.load('./asset/bgm.mp3')

    def __init__(self, gamemaps, **kwargs):
        super().__init__(**kwargs)
        self.gamemaps=gamemaps
        self.player_dialog =  self.game_available_text if gamemaps else self.game_not_available_text

    def start_game(self) -> None:
        if self.gamemaps:
            self.isgame = True
            self.player_dialog = "The Player is on Adventure!"

            curgame = random.choice(gamemaps)
            gamemap = curgame.get("gamemap")
            self.total_treasure = curgame.get("total_treasure")

            self.player_health = 3
            self.player_score = 0
            self.scorescreen.reset()

            self.sound.play()
            self.setup_controller()
            self.gamegrid.setup(gamemap)
            self.check_possible_move()

    def stop_game(self) -> None:
        self.isgame = False
        self.sound.stop()
        self.gamegrid.stop()
        self.scorescreen.reset()
        self.player_dialog = self.game_available_text if gamemaps else self.game_not_available_text

    def disable_controller(self) -> None:
        controller: ControllerLayout = self.controller
        controller.north_active = False
        controller.east_active = False
        controller.south_active = False
        controller.west_active = False

    def check_possible_move(self) -> None:
        gamegrid: GameGrid = self.gamegrid
        controller: ControllerLayout = self.controller
        controller.north_active = gamegrid.is_player_possiblepath(gamegrid.UP)
        controller.east_active = gamegrid.is_player_possiblepath(gamegrid.RIGHT)
        controller.south_active = gamegrid.is_player_possiblepath(gamegrid.DOWN)
        controller.west_active = gamegrid.is_player_possiblepath(gamegrid.LEFT)

    def check_game_over(self) -> None:
        if self.player_health<=0:
            self.player_dialog = self.gameover_text
            self.disable_controller()
        if self.player_score==self.total_treasure:
            self.player_dialog = self.win_text
            self.disable_controller()

    def move_player(self, direction) -> None:
        gamegrid: GameGrid = self.gamegrid

        # disable controller
        self.disable_controller()

        # get player heading
        x,y = gamegrid.get_player_heading(direction)

        # reveal direction player move
        gamegrid.reveal(y, x)

        # if necessary move player
        self.player_dialog = random.choice(self.player_dialog_list[str(gamegrid.get_item(y, x))])

        if gamegrid.is_item(y, x, GameGrid.WALKABLE):
            gamegrid.move_player_pos(y,x)

        elif gamegrid.is_item(y, x, GameGrid.MONSTER):
            self.player_health -= 1

        elif gamegrid.is_item(y, x, GameGrid.TREASURE):
            self.player_score += 1
        
        # check next possible movement
        self.check_possible_move()
        self.check_game_over()

    def setup_controller(self) -> None:
        controller: ControllerLayout = self.controller
        controller.set_btn_fx("north_btn_fx", lambda: self.move_player(GameGrid.UP))
        controller.set_btn_fx("east_btn_fx", lambda: self.move_player(GameGrid.RIGHT))
        controller.set_btn_fx("south_btn_fx", lambda: self.move_player(GameGrid.DOWN))
        controller.set_btn_fx("west_btn_fx", lambda: self.move_player(GameGrid.LEFT))

class TextBasedAdventure(App):
    def __init__(self, gamemaps, **kwargs):
        super().__init__(**kwargs)
        self.gamemaps = gamemaps

    def build(self):
        return GameUI(self.gamemaps)

if __name__ == "__main__":
    import json

    gamemaps = []
    with open("gamemap.json", 'r') as f:
        gamemaps = json.load(f).get("maps", [])
    TextBasedAdventure(gamemaps[:1]).run()