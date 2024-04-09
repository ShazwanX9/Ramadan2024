from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import random

from kivy.properties import (
    StringProperty, BooleanProperty, 
    NumericProperty, ObjectProperty
)

from kivy.core.window import Window
Window.size = (375, 667)

class MetricConversionToolApp(App):
    conversion_type = {
        "Length": {
            "Meter": 1,
            "KiloMeter": .001,
            "CentiMeter": 100,
            "MiliMeter": 10,
            "MicroMeter": 1000000,
            "NanoMeter": 100000000,
            "Mile": 0.000621371,
            "Yard": 1.09361,
            "Foot": 3.28084,
            "Inch": 39.3701,
            "Light Year": 0.0000000000000001057,
        },

        "Weight": {},
        "Area": {},
        "Volume": {},
        "Temperature": {},
    }

    def option_selected(self, layout, selection_text) -> None:
        layout.selected = selection_text
        for child in layout.children:
            child.disabled = child.text==selection_text
        self.convert_value(self.root.userinput.text)

    def type_selected(self, selection_text) -> None:
        self.root.userinput.text = ""
        self.root.selected = selection_text
        self.root.to_option.clear_widgets()
        self.root.from_option.clear_widgets()
        for data in self.conversion_type.get(selection_text, []):
            self.root.to_option.add_widget(Button(text=data, on_release=lambda btn, data=data: self.option_selected(self.root.to_option, data)))
            self.root.from_option.add_widget(Button(text=data, on_release=lambda btn, data=data: self.option_selected(self.root.from_option, data)))

    def invert_selection(self) -> None:
        temp = self.root.from_option.selected
        self.option_selected(self.root.from_option, self.root.to_option.selected)
        self.option_selected(self.root.to_option, temp)

    def convert_value(self, value) -> None:
        conversion_type = self.conversion_type.get(self.root.selected, {})
        si = float(value or 0)/conversion_type.get(self.root.from_option.selected, 1)
        result = si*conversion_type.get(self.root.to_option.selected, 1)
        self.root.result.text = f"{result:.18}"

if __name__ == "__main__":
        MetricConversionToolApp().run()