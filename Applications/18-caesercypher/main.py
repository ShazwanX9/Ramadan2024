from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty

from kivy.core.window import Window
Window.size = (375, 667)

class MainApp(App):
    to_encrypt = BooleanProperty(True)
    result = StringProperty("")

    def caesar_cipher_encrypt(self, plaintext, shift) -> str:
        encrypted_text = ""
        for char in plaintext:
            if char.isalpha():
                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                encrypted_text += chr(shifted)
            else:
                encrypted_text += char
        return encrypted_text

    def caesar_cipher_decrypt(self, ciphertext, shift) -> str:
        return self.caesar_cipher_encrypt(ciphertext, -shift)

    def max_len(self, len) -> None:
        self.root.ids.usershift.text = self.root.ids.usershift.text[:len]
        self.translate(self.root.ids.userinput.text)

    def translate(self, text: str) -> None:
        shift = int(self.root.ids.usershift.text or 0)
        if self.to_encrypt:
            self.result = self.caesar_cipher_encrypt(text, shift)
        else:
            self.result = self.caesar_cipher_decrypt(text, shift)

    def invert(self) -> None:
        self.to_encrypt = not self.to_encrypt
        res = self.result
        self.root.ids.userinput.text = res
        self.translate(res)

if __name__ == "__main__":
    MainApp().run()