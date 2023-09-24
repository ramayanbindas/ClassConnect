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

from kivy.lang import Builder
from kivy.core.window import Window
from kivy import platform

# import in-built-module
from component.auth_screen import CreateAuth

Window.size = (320, 620)


class AppScreenManager(MDScreenManager):
    """
    :class: is main screenmanager of the entire application, which holds
    all the screen used in the applicaion.
    """
    def __init__(self, app_builder_obj: object = None, *args, **kw):
        super().__init__(*args, **kw)

        # adding login screen
        CreateAuth(screenmanager=self, app_builder_obj=app_builder_obj)

        '''
        Binding the keyboard inputs with the application.
        '''
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

    def is_desktop(self) -> bool:
        ''':about: This method checks the current platform, in which platfrom the game is being runed.
           :return: return True or False if the platform is comfortable to run the game.
        '''
        if platform in ("linux", "win", "mac"):
            return True
        
        return False

    def keyboard_closed(self):
        '''
        :method: fired when the the window keyboard is closed
        '''
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        ''':about: method fired when any key on the keyboard is pressed.
        '''
        if keycode[0] == 1073742082:  # f11
            self.current = self.next()
        elif keycode[0] == 1073742083:  # f9
            self.current = self.previous()

    def on_keyboard_up(self, keyboard, keycode):
        '''
        :method: fired when any key on the keyboard realse 
        '''
        pass


class ClassConnectApp(MDApp):
    ''''''
    KV_FILES = ["resources/kv_files/mobile_dialog.kv"]
    
    def build(self):
        # self.theme_cls.theme_style_switch_animation = True
        # self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.accent_hue = "200"

        return AppScreenManager(app_builder_obj=self)

    def on_start(self):
        '''
        :method: is called when the application start. Do
        all the stuff which should be initialize while starting
        the application.
        '''

        '''
        here we loading all the files mentions in the :class attr: KV_FILES, if
        any file exist in the list.
        '''
        for file in self.KV_FILES:
            Builder.load_file(file)


if __name__ == '__main__':
    ClassConnectApp().run()
