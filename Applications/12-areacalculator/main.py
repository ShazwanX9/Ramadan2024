from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.properties import BooleanProperty, StringProperty, ObjectProperty, NumericProperty

from kivy.core.window import Window
Window.size = (375, 667)

class AreaCalculator(MDRelativeLayout):
    isThirdFieldActive = BooleanProperty()
    shape = StringProperty()
    image = StringProperty()
    formula = StringProperty()
    result = NumericProperty(0.0)
    textfield0 = ObjectProperty()
    textfield1 = ObjectProperty()
    textfield2 = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button_click(self.ids.trapezoid_btn)

    def button_click(self, btn) -> None:
        self.isThirdFieldActive = btn==self.ids.trapezoid_btn
        data = {
            self.ids.rectangle_btn: {
                "name": "rectangle",
                "image": "./asset/rectangle.png",
                "formula": "A = w * l", 
                "hinttext0": "Enter Width [ w ]:", 
                "hinttext1": 
                "Enter Length [ l ]:", 
            },
            self.ids.triangle_btn: {
                "name": "triangle",
                "image": "./asset/triangle.png",
                "formula": "A = h * b / 2", 
                "hinttext0": "Enter Height [ h ]:", 
                "hinttext1": "Enter Base [ b ]:", 
            },
            self.ids.parallelogram_btn: {
                "name": "parallelogram",
                "image": "./asset/parallelogram.png",
                "formula": "A = h * b", 
                "hinttext0": "Enter Height [ h ]:", 
                "hinttext1": "Enter Base [ b ]:", 
            },
            self.ids.trapezoid_btn: {
                "name": "trapezoid",
                "image": "./asset/trapezoid.png",
                "formula": "A = ( t + b ) * h / 2", 
                "hinttext0": "Enter Height [ h ]:", 
                "hinttext1": "Enter Base [ b ]:", 
                "hinttext2": "Enter Top [ t ]:", 
            },
            self.ids.circle_btn: {
                "name": "circle",
                "image": "./asset/circle.png",
                "formula": "A = πr[sup]2[/sup]", 
                "hinttext0": "Enter PI [ π ]:", 
                "value0": "3.141592653589793", 
                "hinttext1": "Enter Radius [ r ]:", 
            },
        }

        btn_data = data.get(btn)

        self.animation = []
        if self.shape!="circle":
            self.animation.append(f"./asset/{self.shape}_circle.zip", )
        if btn_data.get("name")!="circle":
            self.animation.append(f"./asset/circle_{btn_data.get('name')}.zip", )
        self.animation.append(btn_data.get("image"))

        self.shape = btn_data.get("name")
        self.image = self.animation[0]
        self.formula = btn_data.get("formula")
        self.textfield0.hint_text = btn_data.get("hinttext0")
        self.textfield0.text = btn_data.get("value0", "")
        self.textfield1.hint_text = btn_data.get("hinttext1")
        self.textfield2.hint_text = btn_data.get("hinttext2", "")
        self.textfield1.text = ""
        self.textfield2.text = ""

    def calculate(self, textfield, value) -> None:
        v0 = float(self.textfield0.text or 0)
        v1 = float(self.textfield1.text or 0)
        v2 = float(self.textfield2.text or 0)

        self.result = {
            "rectangle": v0*v1,
            "triangle": v0*v1/2,
            "parallelogram": v0*v1,
            "trapezoid": (v1+v2)*v0/2,
            "circle": v0*v1
        }.get(self.shape)

    def animate_image(self, img) -> None:
        if self.animation and img._coreimage.anim_index + 1 == len(img._coreimage.image.textures):
            # one animation loop complete
            img.loop_count += 1
            if img.loop_count == img.anim_loop:
                img.anim_count += 1
                img.loop_count = 0
                if img.anim_count<len(self.animation):
                    self.image = self.animation[img.anim_count]
                else:
                    img.anim_count = 0


class MainApp(MDApp):
    def build(self):
        return AreaCalculator()

if __name__ == "__main__":
    MainApp().run()