from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty

from kivy.core.window import Window
Window.size = (375, 667)

class MainApp(App):
    to_roman = BooleanProperty(False)
    result = StringProperty("")
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    roman_numerals = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C',
                    90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V',
                    4: 'IV', 1: 'I'}

    def roman_to_number(self, roman_numeral: str) -> int:
        number = 0
        prev_value = 0
        
        for char in reversed(roman_numeral):
            value = self.roman_dict.get(char, 0)
            if value < prev_value:
                number -= value
            else:
                number += value
            prev_value = value
            
        return number

    def number_to_roman(self, number: int) -> str:
        roman_numeral = ''
        
        for value, numeral in self.roman_numerals.items():
            while number >= value:
                roman_numeral += numeral
                number -= value
        
        return roman_numeral

    def is_valid_roman_numeral(self, roman_numeral: str):
        if not roman_numeral:
            return False
        
        prev_value = float('inf') 
        consecutive_occurrences = 0
        
        for char in roman_numeral:
            if char not in self.roman_dict.keys():
                return False
            
            value = self.roman_dict.get(char, 0)
            
            if value < prev_value:
                if consecutive_occurrences > 1:  # Check for consecutive occurrences
                    return False
                consecutive_occurrences = 0
            else:
                consecutive_occurrences += 1
                if consecutive_occurrences > 2:
                    return False
            prev_value = value
        
        return True

    def translate(self, text: str) -> None:
        self.root.ids.userinput.text = self.root.ids.userinput.text.upper()
        if self.to_roman:
            self.result = self.number_to_roman(int(text)) if text.isnumeric() else ""
        else:
            if text and not self.is_valid_roman_numeral(self.root.ids.userinput.text):
                self.root.ids.userinput.text = text[:-1]
            self.result = str(self.roman_to_number(self.root.ids.userinput.text))

    def invert(self) -> None:
        self.to_roman = not self.to_roman
        res = self.result
        self.root.ids.userinput.text = res
        self.translate(res)

if __name__ == "__main__":
    MainApp().run()