from kivy.app import App
from kivy.properties import NumericProperty

class MainApp(App):
    wordcount = NumericProperty(0)
    lettercount = NumericProperty(0)
    def count(self, word) -> None:
        self.lettercount = len(word)
        self.wordcount = len(word.split())

if __name__ == "__main__":
    MainApp().run()