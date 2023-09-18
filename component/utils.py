'''
# version: 1.0.0
:about: This module build for creating and adding screen easily to the main
screen manager and beside this it able to manage different layout for the
different system i.e (phone, tablet, desktop). Main purpose of the class is
to provide the above functionality to the child class as well as make help
to keep the logic for all the layout same into a singe controller class.,

:class:
    [Base]
'''

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screenmanager import MDScreenManager

from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from os.path import join

from .settings import BASEFILEPATH


class Base(MDScreen, MDResponsiveLayout):
    ''':class: is used with the screen manager(MDScreenManager/ScreenManger).
            This class in inherited from `MDScreen` and `MDResponsizeLayout`
            .For creating instance of this class you need to pass a screen name
            for this screen object which is unique(This first screen is called
            Primary Screen). Over This Primary Screen you can add kivy-widgets.
            
            [Note: This Primary screen is automatically added to the given 
            screen manager object if it passed during instancing this class 
            else you have to do manually by calling the add_screen_to_parent 
            takes the screen_object as argument.]

        Usage: This class is built because, to make easy to apply the
            responsive layout widget to every class (conclusion: easy to handle
            or create responsive layouts.) For using this class effectively:
            You can instance this class in your own, created class where you
            need a screen to be able to responsive. The class you create is
            used for defining comman method or logic for your different layout.
            Just you have to passed self object to that layouts.
        
        i.e:
            from kivymd.app import MDApp
            from kivymd.uix.floatlayout import MDFloatLayout
            from kivymd.uix.screenmanager import MDScreenManager

            from kivy.lang import Builder

            from component.utils import Base

            Builder.load_string("""
            <CommanButton@MDRaisedButton>:
                pos_hint: {"ceneter_x": 0.5, "center_y": 0.5}

            <MobileView>:
                <CommanButton>:
                    text: "mobile"
                    on_press: root.master.comman_function(self)

            <TabletView>:
                <CommanButton>:
                    text: "tablet"
                    on_press: root.master.comman_function(self)

            <DesktopView>:
                <CommanButton>:
                    text: "desktop"
                    on_press: root.master.comman_function(self)
            """)
            class MobileView(MDFloatLayout):
                def __init__(self, master, **kw):
                    super().__init__(**kw)
                    self.master = master

            class TabletView(MDFloatLayout):
                def __init__(self, master, **kw):
                    super().__init__(**kw)
                    self.master = master

            class DesktopView(MDFloatLayout):
                def __init__(self, master, **kw):
                    super().__init__(**kw)
                    self.master = master

            class MyController(Base):
                def __init__(self, screenmanager, *args, **kw):
                    super().__init__("my_fist_screen", screenmanager)

                    self.mobile_view = MobileView()
                    self.tablet_view = TabletView()
                    self.desktop_view = DesktopView()

                def comman_function(self, instance):
                    print(instance.text)

            class MyScreenManager(MDScreenManager):
                def __init__(self, **kw):
                    super().__init__(**kw)

                    MyController(self)

            class TestApp(MDApp):
                def build(self):
                    return MyScreenManager()

            if __name__ == "__main__":
                TestApp().run()

        :inherited: [kivymd.uix.screen.MDScreen,
         kivymd.uix.responsivelayout.MDResponsiveLayout]

        :class: Base: cls_variables:
            [screenmanager=None, [MobileView, TabletView, DesktopView] =
            ObjectPropert()]

        :class: Base: cls_methods:
            [`add_screen_to_parent`, `remove_screen_to_parent`, set_manager`,
            `load_kv_files`]

        :class: Base: params: 
            [name, screenmanager]
        
        Note: screenmanager of the class variable would be set during the
        creating, a own class by assigning `ScreenManager (object)` to the
        screenmanager attribute of the `Base Class` or by manually set `i.e
        Base.screenmanager = ScreenManger`,

        [It recommended to use one screenmanager to the whole application]

    '''
    __all__ = []  # Store all the instances created by this base class
    '''
    Screenmanager Object used to be add this class. [# refer: :method
    `add_screen_to_parent`]
    '''
    screenmanager = None
    
    '''
    Instance of the class(Kivy-Widget) which should be callable. Used the
    instance to be added on this screen(inhareted from the MDScreen)
    '''
    # MobileView, TabletView, DesktopView = ObjectProperty(), ObjectProperty(),
    # ObjectProperty()

    def __init__(self, name: str, screenmanager: object = None, *args, **kw):
        MDScreen.__init__(self, *args, **kw)
        MDResponsiveLayout.__init__(self, *args, **kw)
        
        self.name = name  # name of the screen

        # assigning value to the class variable
        Base.__all__.append(self)
        if isinstance(screenmanager, MDScreenManager):
            Base.screenmanager = screenmanager
        else:
            Exception("Please Assign a `ScreenManager` object")

        # fired internal methods
        self.add_screen_to_parent(screen_object=self)

    # Methods
    def add_screen_to_parent(self, screen_object: object = None):
        ''' :method: used to add the screen to the main screen manager of the
                application.

            :param screen_object: object of the screen which should be given,
                to the screen object.
                
                [Note: The screen name is only added when the screenmanger
                object is there and the screen manager dosn't hold this
                screen name before.]
        '''
        if Base.screenmanager:
            if screen_object not in Base.screenmanager.children:
                if isinstance(screen_object, MDScreen):
                    Base.screenmanager.add_widget(self)
                else:
                    Exception("`screen_object`: must be a Screen object")
        else:
            Exception("Please Assign a `ScreenManager` object first.")

    def remove_screen_to_parent(self, screen_object: object):
        ''' :method: used to remove the screen to the parent(ScreenManager)
            :param screen_object: object of the screen which should be removed.
        '''
        if Base.screenmanager:
            Base.screenmanager.remove_widget(self)
        else:
            Exception("Please Assign a `ScreenManager` object first.")

    @classmethod
    def set_manager(cls, screenmanager: object) -> None:
        ''':classmethod: used to change the manager of the application.
            :param screenmanager: ScreenManager object of the application.
            Note: It is preferred to be used one manager in the application, if
                application manager change than change it.
        '''
        cls.screenmanager = screenmanager

    @staticmethod
    def load_kv_file(kv_file_name: list, kv_file_path: str = join(BASEFILEPATH,
                     "resources/kv_files")) -> None:
        ''':method: used to load the file for the kv_file_path by the name
                kv_file_name
            :param kv_file_name: list of the kv file name without extension.
                i.e: demo
            :param kv_file_path: Path of the kv file directory
        '''
        for name in kv_file_name:
            Builder.load_file(join(kv_file_path, name + ".kv"))

    # Events
    # def on_enter(self): # fired when the screen is called
    #   self.mobile_view = self.MobileView
    #   self.tablet_view = self.TabletView
    #   self.desktop_view = self.DesktopView

    #   print("fired", self.MobileView)

    # Magic Methods
    def __repr__(self):
        return f"({self.__class__.__name__}: [{self.name}, {Base.screenmanager}])"  # noqa: E501
