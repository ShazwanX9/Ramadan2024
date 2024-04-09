from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.uix.button import Button

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty, ListProperty
)

import json
import random

from kivy.core.window import Window
from kivy.core.window import Keyboard
Window.size = (375, 667)

URL = "https://raw.githubusercontent.com/le717/PHP-Hangman/master/words/word-list.json"

class MainApp(App):
    guesscount = NumericProperty(0)
    isgame = BooleanProperty(False)
    isuserguessing = BooleanProperty(False)
    content_word = StringProperty("Content Word here")
    content_hint = StringProperty("Content Hint here")

    key_pressed = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = []
        self.load_content()
        Window.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_once(self.load_keyboard, 1)

    def keycode_to_string(self, value):
        '''Convert a keycode number to a string according to the
        :attr:`Keyboard.keycodes`. If the value is not found in the
        keycodes, it will return ''.
        '''
        keycodes = list(Keyboard.keycodes.values())
        if value in keycodes:
            return list(Keyboard.keycodes.keys())[keycodes.index(value)]
        return ''

    def on_keyboard_up(self, window, keycode, *args):
        char = self.keycode_to_string(keycode)
        if char in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
            self.key_press(char)

    def key_press(self, letter) -> None:
        if self.isgame and not self.isuserguessing and letter.upper() not in self.key_pressed:
            self.key_pressed.append(letter.upper())
            self.update_keyboard()
            result = self.content_current.get("word").upper()
            self.content_word = self.reveal_word(result)

            if self.content_word == result:
                self.stop_game()

            if letter.upper() not in self.content_word:
                self.guesscount += 1

    def update_keyboard(self) -> None:
        for i in range(3):
            for btn in self.root.ids.keyboard.children[i].children:
                btn.disabled = (not self.isgame) or (btn.text in self.key_pressed)

    def load_keyboard(self, dt=-1) -> None:
        for i in range(3):
            for char in ["zxcvbnm", "asdfghjkl", "qwertyuiop"][i]:
                self.root.ids.keyboard.children[i].add_widget(
                    Button(
                        text=char.upper(),
                        on_release=lambda btn, char=char: self.key_press(char),
                        disabled= char in self.key_pressed
                    )
                )
        self.update_keyboard()

    def load_content(self) -> None:
        def success_fx(request, result) -> None:
            self.content = json.loads(result)
        self.req = UrlRequest(url=URL, on_success=success_fx)

    def choose_content(self, index=-1) -> dict:
        if self.content:
            return self.content[index]
        return {"word": "", "hint": ""}

    def random_content(self) -> dict:
        return random.choice(self.content) or {"word": "", "hint": ""}

    def reveal_word(self, word) -> str:
        reveal = "_"*len(word)
        for i,letter in enumerate(word):
            if letter in self.key_pressed:
                reveal = reveal[:i] + letter + reveal[i+1:]
        return reveal

    def guess(self) -> None:
        if self.root.ids.userguess.text.upper() == self.content_current.get("word").upper():
            self.stop_game()
        else:
            self.guesscount += 1

    def start_game(self) -> None:
        self.isgame = True
        self.key_pressed.clear()
        self.update_keyboard()
        self.root.ids.userguess.text = ""

        self.guesscount = 0
        self.content_current = self.random_content()
        self.content_hint = self.content_current.get("hint", "")
        self.content_word = self.reveal_word(self.content_current.get("word").upper())
        print(self.content_current.get("word").upper())

    def stop_game(self, dt=-1) -> None:
        self.isgame = False
        self.key_pressed.clear()
        self.update_keyboard()
        self.root.ids.userguess.text = ""
        self.content_word = self.content_current.get("word").upper()

if __name__ == "__main__":
    MainApp().run()