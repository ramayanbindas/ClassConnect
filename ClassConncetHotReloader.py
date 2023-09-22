'''
# version: 1.0.0
:about: This script is written for ClassConnect hot reloading purpose
to design UI.

:Limitation: It can't detect the changes made in the .py file in windows.
as it says by the kivymd documentation. But it detects the changes made
in the entry-point class.

Note: When running this script don't class a builder method into the app.
if has make them comment for now. Because when you config the class and
provide the file it automatically load the file/directory file. 
'''

from kivymd.tools.hotreload.app import MDApp

from kivy.factory import Factory
from kivy.core.window import Window

# import desire class
from kivymd.uix.boxlayout import MDBoxLayout

Window.size = (320, 620)


class AuthScreenMobileView(MDBoxLayout):
    '''
    :class: name should be you entry point class name in kv file.
    customize this class as your need.
    '''
    pass


class SignUpScreenMobileView(MDBoxLayout):
    '''
    :class: name should be you entry point class name in kv file.
    customize this class as your need.
    '''
    pass


class ClassConnectHotReloaderApp(MDApp):
    # config hot reload
    DEBUG = True
    KV_FILES = ["resources/kv_files/auth_screen_mobile.kv"]
    # KV_DIRS = ["resources/kv_files"]
    KV_AUTOREALODER_PATHS = [(".", {"recursive": True})]
    # KV_AUTOREALODER_IGNORE_PATTERS = ["**.pyc", "__pycache__"]

    # CLASSES = {"HotReloadEntryPoint": "hotreloadentrypoint"}
    CLASSES = {"AppScreenManager": "ClassConnect"}

    def build_app(self, first=False): 
        # self.theme_cls.theme_style_switch_animation = True
        # self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.accent_hue = "200"

        # return Factory.HotReloadEntryPoint(self.KV_FILES, 
        #                                    SignUpScreenMobileView)

        return Factory.AppScreenManager()
  

if __name__ == "__main__":
    ClassConnectHotReloaderApp().run()
