import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label


class TestApp(App):
    def build(self):
        return Label(text='Hello World')
        # return Button(text='Hello World')
        
TestApp().run()
