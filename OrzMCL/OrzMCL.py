#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
# os.environ['KIVY_TEXT'] = 'pil'
from kivy.app import App
from kivy.core.window import Window
Window.size = (480, 270)

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Color, Rectangle

from OrzMC.Mojang import Mojang
from OrzMC.Config import Config
from OrzMC.Game import Game


class MCInfoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MCInfoWidget,self).__init__(**kwargs)

        versionsDropDownList = DropDown()
        release_versions = Mojang.get_release_version_id_list(update = True)
        for version in release_versions:
            item = Button(
                text = version,
                size_hint_y = None, 
                height = 50
            )
            item.bind(on_release = lambda item: versionsDropDownList.select(item.text))
            versionsDropDownList.add_widget(item)

        self.versionsButton = Button(
            text = release_versions[0] if len(release_versions) > 0 else 'Get Versions Failed!',
            size_hint = (0.3, 1)
        )
        self.versionsButton.bind(on_release = versionsDropDownList.open)
        versionsDropDownList.bind(on_select = lambda item, text: setattr(self.versionsButton, 'text', text))
        self.add_widget(self.versionsButton)

        self.usernameTextInput = TextInput(
            multiline = False,
            hint_text = 'input a username',
            size_hint = (0.7, 1)
        )
        self.add_widget(self.usernameTextInput)

class Content(FloatLayout):
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        
        self.mcInfoWidget = MCInfoWidget(
            pos_hint = {'x': 0, 'y': .8 },
            size_hint_y = None,
            height = 90,
            spacing = 20,
            padding = 20   
        )
        self.add_widget(self.mcInfoWidget)
        
        startButton = Button(
            text = 'Start',
            size = (140, 60),
            size_hint = (None, None),
            pos_hint = {'center_x': .5, 'center_y': 0.1}
        )
        startButton.bind(on_release = self.startGame)
        self.add_widget(startButton)

        self.infoLabel = Label(
            pos_hint = {'center_x': .5, 'center_y': .5},
            size_hint_y = None
        )
        self.add_widget(self.infoLabel)

    def startGame(self, instance):
        version = self.mcInfoWidget.versionsButton.text
        username = self.mcInfoWidget.usernameTextInput.text

        if len(version) > 0 and len(username) > 0 :
            config = Config(
                is_client = True,
                version = version,
                username = username,
                game_type = 'pure',
                mem_min = '512M',
                mem_max = '2G',
                debug = False,
                force_upgrade = False,
                backup = False,
                optifine = False
            )
            Game(config).startClient()
            self.infoLabel.text = ''
        else:
            self.infoLabel.text = 'username or version is empty'


class OrzMCLApp(App):
    def build(self):
        return Content()    


def run():
    OrzMCLApp().run()

if __name__ == "__main__":
    run()
