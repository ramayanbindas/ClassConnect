'''
# version: 1.0.0
:about: This is the ClassConnectHotReloader Entry Point Class.
'''
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder


class HotReloadEntryPoint(MDScreen):
    """
    :class: Entry Point of the ClassConnectHotReloader class.
    """
    def __init__(self, kv_files: list, entry_point_class_name: str = None,
                 *args, **kw):
        super().__init__(*args, **kw)

        '''
        If you are using diffrent class in name in kv file then this class 
        name. then the name must be give as argument to make the class a child
        of this current class.
        '''
        self.entry_point_class_name = entry_point_class_name
        if entry_point_class_name:
            self.add_widget(entry_point_class_name())

        print(self.entry_point_class_name)