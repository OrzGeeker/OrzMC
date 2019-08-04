
from kivy.app import App
from kivy.uix.button import Button

class OrzMCL(App):
    def build(self):
        return Button(text='Hello World')


def run():
    OrzMCL().run()

if __name__ == "__main__":
    run()
