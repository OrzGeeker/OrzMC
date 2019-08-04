
from kivy.app import App
from kivy.uix.button import Button

class OrzMC(App):
    def build(self):
        return Button(text='Hello World')


def run():
    OrzMC().run()

if __name__ == "__main__":
    run()
