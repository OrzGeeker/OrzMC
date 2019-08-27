# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# os.environ['KIVY_TEXT'] = 'pil'
from kivy.app import App
from kivy.core.window import Window
Window.size = (480, 270)

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Color, Rectangle

from OrzMC.Mojang import Mojang
from OrzMC.Config import Config
from OrzMC.Game import Game


class MCInfoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MCInfoWidget,self).__init__(**kwargs)

        release_versions = []
        try:
            release_versions = Mojang.get_release_version_id_list(update = True)
        except:
            self.infoLabel.text = 'Network is Invalid!!!'
        finally:
            pass

        versionsDropDownList = DropDown()
        for version in release_versions:
            item = Button(
                text = version,
                size_hint_y = None, 
                height = 50,
                background_color = [1,1,0,1]
            )
            item.bind(on_release = lambda item: versionsDropDownList.select(item.text))
            
            versionsDropDownList.add_widget(item)

        self.versionsButton = Button(
            text = release_versions[0] if len(release_versions) > 0 else 'FAILED!',
            color = [1,1,1,1] if len(release_versions) > 0 else [1, 0, 0, 1],
            size_hint = (0.2, 1)
        )
        self.versionsButton.bind(on_release = versionsDropDownList.open)
        versionsDropDownList.bind(on_select = lambda item, text: setattr(self.versionsButton, 'text', text))
        self.add_widget(self.versionsButton)

        self.usernameTextInput = TextInput(
            multiline = False,
            hint_text = 'input a username',
            size_hint = (0.6, 1),
            halign = 'center'
        )
        self.add_widget(self.usernameTextInput)

        self.startButton = Button(
            text = 'Start',
            size_hint = (0.2, 1),
        )
        self.add_widget(self.startButton)

class Content(BoxLayout):
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        
        self.mcInfoWidget = MCInfoWidget(
            size_hint_y = None,
            height = 70,
            spacing = 20,
            padding = [20, 20, 20, 0]
        )
        self.mcInfoWidget.startButton.bind(on_release = self.startGame)
        self.add_widget(self.mcInfoWidget)

        
        self.infoLabel = Label(
            text = 'Info Label'
        )
        self.add_widget(self.infoLabel)

        progressBar = ProgressBar(
            value = 50,
            max = 100,
            size_hint_y = None,
            height = 5
        )
        self.add_widget(progressBar)

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
        self.content = Content(orientation='vertical')
        return self.content

def run():
    OrzMCLApp().run()

if __name__ == "__main__":
    run()