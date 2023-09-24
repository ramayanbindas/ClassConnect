'''
# version: 1.0.0
:about: This module build for creating and adding screen easily to the main
screen manager and beside this it able to manage different layout for the
different system i.e (phone, tablet, desktop). Main purpose of the class is
to provide the above functionality to the child class as well as make help
to keep the logic for all the layout same into a singe controller class.,

:class:
    [BaseScreen]
'''

from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout

from kivy.lang import Builder

from os.path import join

from .settings import BASEFILEPATH


class BaseScreen(MDScreen, MDResponsiveLayout):
    ''':class: is used with the screen manager(MDScreenManager/ScreenManger).
            This class in inherited from `MDScreen` and `MDResponsizeLayout`
            .For creating instance of this class you need to pass a screen name
            for this screen object which is unique(This first screen is called
            Primary Screen). Over This Primary Screen you can add kivy-widgets.
            
            [Note: This Primary screen is automatically added to the given 
            screen manager object if it not passed during instancing this class 
            than you have to do manually add screen, by calling the 
            :method set_manager:]

        Usage: This class is built because, to make easy to apply the
            responsive layout widget through entire application (conclusion: 
            easy to handle or create responsive layouts.) For using this class 
            effectively:
            
            You can instance this class in your own controller class,
            which would be the communication medium between your logic
            and the class which and defining in kv file and are now visible
            in the screen. By this single class.
        
        i.e:
            from kivymd.app import MDApp
            from kivymd.uix.floatlayout import MDFloatLayout
            from kivymd.uix.screenmanager import MDScreenManager

            from kivy.lang import Builder

            from component.utils import BaseScreen

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

            class MyController(BaseScreen):
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

        :class: BaseScreen: cls_variables:
            [screenmanager=None]

        :class: BaseScreen: cls_methods:
            [set_manager`, `load_kv_files`]

        :class: BaseScreen: params: [name, screenmanager]

    '''
    __all__ = []  # Store all the instances created by this BaseScreen class
    '''
    :attr screenmanager: is a internal variable, used for storing the 
    main screenmanager object(i.e: MDScreenManager). Which is used
    for directly adding this screen object to the parent class without
    assigning the parent screen object repeatedly to add this screen
    object to it.
    i.e Once the screen manager object it passes through one of its child class
    it ready to add the other child over the same screen manager without
    assigning the screen object repeatedly.
    '''
    screenmanager = None
    '''
    :attr: store the object of the main builder of this entrie application.
    '''
    app_builder_obj = None

    def __init__(self, name: str, screenmanager: object = None,
                 app_builder_obj: object = None, *args, **kw):
        MDScreen.__init__(self, *args, **kw)
        MDResponsiveLayout.__init__(self, *args, **kw)

        self.name = name  # name of the screen
        '''
        :attr current_view: store the view object which are
        assign in (self.mobile_view/self.tablet_view/self.destop_view) objects.

        Note:- This attribute should be used to fetch ids, available in the
        current used view.
        '''
        self.current_view = None
        self.bind(on_change_screen_type=self.set_current_view)

        # assigning value to the class variable
        BaseScreen.__all__.append(self)
        if screenmanager:
            BaseScreen.screenmanager = screenmanager
        if app_builder_obj:
            BaseScreen.app_builder_obj = app_builder_obj
        
        # fired internal methods
        self.add_screen_to_parent()

    # Methods
    def add_screen_to_parent(self) -> None:
        ''' :method: [internal method] used to add the screen to the main
             screen manager of the application.
        '''
        if BaseScreen.screenmanager:
            BaseScreen.screenmanager.add_widget(self)

    def set_current_view(self, *args) -> None:
        '''
        :method: select among view (i.e mobile_view, tablet_view..) which
        is currently being used according to the device and store that
        view object is :attr self.current_view:
        '''
        if self.real_device_type == "mobile":
            self.current_view = self.mobile_view
        
        elif self.real_device_type == "tablet":
            self.current_view = self.mobile_view
        
        elif self.real_device_type == "desktop":
            self.current_view = self.mobile_view

    @classmethod
    def set_manager(cls, screenmanager: object) -> None:
        ''':classmethod: used to set the :cls_variable screenmanager:
            to the given screenmanager object.

            :param screenmanager: ScreenManager object i.e(MDScreenManager.)

            Note: [After assigning the screen manager it automatically add
            this screen to the given screen manager object.]
        '''
        cls.screenmanager = screenmanager
        cls.add_screen_to_parent()  # adding this class to the give screenmanager.

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

    # Magic Methods
    def __repr__(self):
        return f"({self.__class__.__name__}: [{self.name}, {BaseScreen.screenmanager}])"  # noqa: E501
