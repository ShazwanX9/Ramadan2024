from kivy.app import App
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

import json
import random
from functools import partial

from kivy.properties import BooleanProperty

URL = "https://raw.githubusercontent.com/Kaydonbob03/kaydonbot/master/truthordare.json"

class TruthOrDareApp(App):
    YOU = "You"
    BOT = "Bot"

    isgame = BooleanProperty(False)
    isdisablebtn = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.question_list = []
        self.cur_question = []

    def addchat(self, text, user="You") -> None:
        self.root.chatlist += f"\n{user}: {text}"

    def robottext(self, text, dt) -> None:
        self.addchat(text, TruthOrDareApp.BOT)
        self.isdisablebtn = False

    def robotchat(self, text) -> None:
        self.isdisablebtn = True
        Clock.schedule_once(partial(self.robottext, text), 1.5)

    def startgame(self) -> None:
        self.isgame = True
        self.addchat("Hey, I'm bored! Let's play a game!")
        self.robotchat("Affirmative! Initiating question sequence. Truths or Dares...?")

    def btn_response(self, isTruth: bool) -> None:
        userinput = "truths" if isTruth else "dares"
        self.addchat(userinput.capitalize())
        self.robotchat(random.choices(self.question_list[userinput])[0])

    def on_start(self):
        def on_success(req, result):
            self.question_list = json.loads(result)
        UrlRequest(URL, on_success)

if __name__ == "__main__":
    TruthOrDareApp().run()