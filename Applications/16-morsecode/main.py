from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty

from kivy.core.window import Window
Window.size = (375, 667)

class MainApp(App):
    to_morsecode = BooleanProperty(False)
    result = StringProperty("")

    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
        '7': '--...', '8': '---..', '9': '----.',
        
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', ':': '---...',
        ';': '-.-.-.', '"': '.-..-.', '-': '-....-', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
        '&': '.-...', '@': '.--.-.', '=': '-...-',
        
        ' ': '$',
        '\n': ' ',
    }

    # Reverse mapping for decoding
    reverse_morse_code = {value: key for key, value in morse_code.items()}

    def translate(self, text) -> None:
        if self.to_morsecode:
            self.result = ' '.join(self.morse_code.get(l, "#") for l in text.upper())
        else:
            self.result = ''.join(self.reverse_morse_code.get(l, "#") for l in text.split())

    def invert(self) -> None:
        self.to_morsecode = not self.to_morsecode
        res = self.result
        self.root.ids.userinput.text = res
        self.translate(res)

if __name__ == "__main__":
    MainApp().run()