"""
# Author: Ramayan Mardi
# Author-email: ramayanmardi@gmail.com
# version: 1.1.0
# name: ClassConnect
# kivy version: 2.2.0
# kivymd version: 1.1.1
# License: MIT
# Required: (kivy, kivymd)

ABOUT :module: Summary: Make the college time-table scheduling easy, by
    allowing professor, student and college administration come to same
    place and discuss their class schedule, manage student report,
    observe student progress etc.

"""
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window

# import in-built-module
from component.auth_screen import CreateAuth

Window.size = (320, 620)


class AppScreenManager(MDScreenManager):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adding login screen
        CreateAuth(screenmanager=self)
        
        # opening the start-up screen
        # self.current = "auth_screen"

    def add_screen(self, screen_object: object) -> None:
        """"""
        self.add_widget(screen_object)


class ClassConnectApp(MDApp):
    def build(self):
        # self.theme_cls.theme_style_switch_animation = True
        # self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.accent_hue = "200"
        return AppScreenManager()


if __name__ == '__main__':
    ClassConnectApp().run()
