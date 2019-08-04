
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle

class OrzMCL(App):
    def build(self):
        layout = BoxLayout(padding=10)
        button = Button(text='Hello World', size_hint = (0.5, 0.5))
        layout.add_widget(button)
        return layout


def run():
    OrzMCL().run()

if __name__ == "__main__":
    run()
