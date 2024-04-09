from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout

from kivy.properties import ObjectProperty
from kivymd.font_definitions import theme_font_styles

import json
from random import choice
from kivy.network.urlrequest import UrlRequest

from kivy.core.text import LabelBase

URL = "https://raw.githubusercontent.com/reggi/fortune-cookie/master/fortune-cookie.json"
# URL = "https://github.com/reggi/fortune-cookie/blob/master/fortune-cookies.txt"

class CookieLayout(MDFloatLayout):
    MAX_IMAGE_IDX = 5
    fortunecookie_image = ObjectProperty()
    label = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_cookie = False

    def load_fortune(self) -> str:
        fortune = ""
        def success_fx(request, result) -> None:
            nonlocal fortune
            fortune = choice(json.loads(result))

        req = UrlRequest(url=URL, on_success=success_fx)
        req.wait()
        return fortune

    def image_on_texture(self) -> None:
        if self.fortunecookie_image._coreimage.anim_index == CookieLayout.MAX_IMAGE_IDX:
            self.label.text = self.load_fortune()
        else:
            self.label.text = ""

    def read_cookie(self) -> None:
        if self.reset_cookie:
            self.fortunecookie_image.anim_delay = -1
            self.fortunecookie_image.reload()
        else:
            self.fortunecookie_image.anim_delay = 1/6

        self.reset_cookie = not self.reset_cookie

class FortuneCookieApp(MDApp):
    def build(self):

        LabelBase.register(
            name="Campana",
            fn_regular="./asset/CampanaScript_PERSONAL_USE_ONLY.otf")

        theme_font_styles.append('Campana')
        self.theme_cls.font_styles["Campana"] = [
            "Campana",
            64,
            False,
            0.15,
        ]

        return CookieLayout()

if __name__ == '__main__':
    FortuneCookieApp().run()
