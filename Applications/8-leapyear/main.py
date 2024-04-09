from kivy.app import App

class LeapYearApp(App):
    def calc(self, text) -> None:
        text = text[:4]
        self.root.textinput.text=text
        self.root.userinput=int(text or 0)
        year = int(text or 0)
        self.root.isleapyear= int(((not year%4) and (year%100)) or (not year%400))

if __name__ == "__main__":
    LeapYearApp().run()