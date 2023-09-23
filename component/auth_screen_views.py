'''
# version: 1.0.0
:about: This moudle contain all the different type class (Views), i.e:
(MobileView, TabletView, DesktopView) for the :class: `CreateAuth`,
:class: `SignUP, :class: `SignIn`

:class:
    [AuthScreenMobileView, AuthScreenTabletView, AuthScreenDesktopView]
'''

__all__ = ("AuthScreenMobileView", "AuthScreenTabletView",
           "AuthScreenDesktopView")

from kivymd.uix.boxlayout import MDBoxLayout

from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color

# -----------------------------COMMAND-FUNCTION-----------------------


# ------------------------------AUTHSCREEN-VIEWS---------------------


class AuthScreenMobileView(MDBoxLayout):
    def __init__(self, master: object, *args, **kw):
        super().__init__(*args, **kw)
        self.master = master


class AuthScreenTabletView(MDBoxLayout):
    def __init__(self, master: object, *args, **kw):
        super().__init__(*args, **kw)
        self.master = master


class AuthScreenDesktopView(MDBoxLayout):
    def __init__(self, master: object, *args, **kw):
        super().__init__(*args, **kw)
        self.master = master


# ------------------------ SIGN-UP-SCREEN-VIEWS-----------------------------


class SignUpScreenMobileView(MDBoxLayout):
    def __init__(self, master: object, *args, **kw):
        super().__init__(*args, **kw)
        self.master = master


class SignUpScreenTabletView(MDBoxLayout):
    def __init__(self, master: object, *args, **kw):
        super().__init__(*args, **kw)
        self.master = master


class SignUpScreenDesktopView(MDBoxLayout):
    def __init__(self, master: object, *args, **kw):
        super().__init__(*args, **kw)
        self.master = master

# ------------------------ SIGN-IN-SCREEN-VIES------------------------------
