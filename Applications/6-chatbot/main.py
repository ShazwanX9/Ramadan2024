from kivy.app import App
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

import json
import random
from functools import partial

from kivy.properties import BooleanProperty

URL = "https://raw.githubusercontent.com/curiousily/simple-quiz/master/script/statements-data.json"

class ChatBotApp(App):
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
        self.addchat(text, ChatBotApp.BOT)
        self.isdisablebtn = False

    def robotchat(self, text) -> None:
        self.isdisablebtn = True
        Clock.schedule_once(partial(self.robottext, text), 1.5)

    def appendQuestion(self) -> None:
        if self.question_list:
            self.cur_question = random.choices(self.question_list)[0]
            self.robotchat(self.cur_question[0])
        else: 
            self.isgame = False
            self.robotchat("Apologies, there appears to be an issue with my system. Unable to proceed with the question sequence. Initiating system diagnostics.")

    def startgame(self) -> None:
        self.isgame = True
        self.addchat("Hey, I'm bored! Let's play a game!")
        self.robotchat("Affirmative! Initiating question sequence. Let's test your knowledge...")
        self.appendQuestion()

    def btn_response(self, isTrue: bool) -> None:
        self.addchat(str(isTrue))
        if (isTrue == self.cur_question[1]):
            self.robotchat("Your response is accurate. Proceeding to the next question.")
        else:
            self.robotchat("Apologies, your response is incorrect. Initiating the next question sequence.")
        Clock.schedule_once(lambda dt:self.appendQuestion(), 1.5)

    def on_start(self):
        def on_success(req, result):
            self.question_list = json.loads(result)
        UrlRequest(URL, on_success)

if __name__ == "__main__":
    ChatBotApp().run()