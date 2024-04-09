from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest

import json
import random
from datetime import datetime, timedelta

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty
)

URL = "https://raw.githubusercontent.com/aaronnech/Who-Wants-to-Be-a-Millionaire/master/questions.json"

class WhoWantToBeAMillionairApp(App):
    GAMES = "games"
    CORRECT = "correct"
    CONTENT = "content"
    QUESTION = "question"
    QUESTIONS = "questions"

    is_game = BooleanProperty(False)
    question_number = NumericProperty(0)

    question_label = StringProperty("")
    answer_option0 = StringProperty("")
    answer_option1 = StringProperty("")
    answer_option2 = StringProperty("")
    answer_option3 = StringProperty("")

    prompt_message = StringProperty("")
    timer_label = StringProperty("Time Taken: 00:00")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game_data: list[list[dict]] = []
        self._cur_game_data: list[dict] = []
        self._cur_question_data: dict = {}

        self.btn_list: list[Button] = []
        self.now = datetime.now()
        self.timer = None

        UrlRequest(url=URL, on_success=self.load_game_data)
        Clock.schedule_once(self._setup, 1)

    def load_game_data(self, request, result) -> None:
        self._game_data = json.loads(result)["games"]

    def start_game(self) -> None:
        self.is_game = True
        self.question_number = 0
        self._cur_game_data = random.choice(self._game_data)[WhoWantToBeAMillionairApp.QUESTIONS]
        self._next_question()
        self.start_timer()

    def stop_game(self) -> None:
        self.is_game = False
        self._cur_question_data: dict = {}
        self.stop_timer()

    def get_total_question_number(self) -> int:
        return len(self._cur_game_data)

    def _has_next_question(self) -> bool:
        return self.question_number<self.get_total_question_number()

    def _next_question(self, dt=-1) -> None:
        self._cur_question_data = self._cur_game_data[self.question_number]
        self._setup()
        self.question_number += 1

    def _setup(self, dt=-1) -> None:
        content = [
            "First answer option will be prompt here", 
            "Second answer option will be prompt here", 
            "Third answer option will be prompt here", 
            "Fourth answer option will be prompt here", 
        ]

        self.question_label = self._cur_question_data.get(WhoWantToBeAMillionairApp.QUESTION, "Question will be prompt here")
        self.answer_option0 = self._cur_question_data.get(WhoWantToBeAMillionairApp.CONTENT, content)[0]
        self.answer_option1 = self._cur_question_data.get(WhoWantToBeAMillionairApp.CONTENT, content)[1]
        self.answer_option2 = self._cur_question_data.get(WhoWantToBeAMillionairApp.CONTENT, content)[2]
        self.answer_option3 = self._cur_question_data.get(WhoWantToBeAMillionairApp.CONTENT, content)[3]

        self.btn_list = [self.root.ids.btn_0, self.root.ids.btn_1, self.root.ids.btn_2, self.root.ids.btn_3]

        for i,button in enumerate(self.btn_list):
            if isinstance(button, Button):
                button.background_color=[1,1,1,1]
                button.disabled_color=[1,1,1,1]
        self.prompt_message=""

    def select_answer(self, answer: int) -> None:
        correct = self._cur_question_data.get(WhoWantToBeAMillionairApp.CORRECT, -1)

        if correct>-1 and answer == correct:
            if self._has_next_question():
                self._next_question()
            else:
                self.prompt_message = "Congrats!\nYou are a Millionair!"
                self.stop_game()
        elif correct==-1:
            self.prompt_message = "Data did not fetch properly"
            self.stop_game()
        else:
            self.prompt_message = "Its Wrong! Game Over!"
            for i,button in enumerate(self.btn_list):
                if isinstance(button, Button) and i==correct:
                    button.background_color=[1,0,0,1]
                    button.disabled_color=[1,0,0,1]

            self.stop_game()

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
        self.timer_label = "Time Taken: 00:00"

    def update_clock(self, dt=-1) -> None:
        self.now = self.now + timedelta(seconds = 1)
        self.timer_label = f"Time Taken: {self.now.strftime('%M:%S')}"


if __name__ == '__main__':
    WhoWantToBeAMillionairApp().run()