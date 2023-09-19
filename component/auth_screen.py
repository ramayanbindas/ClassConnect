'''
# version: 1.0.0
:about: This module build the authentication system layout and functionality,

:class:
    [CreateAuth, SignUpScreen, SignInScreen]
'''

from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

# import in-built module
from .utils import Base
from .auth_screen_views import (AuthScreenMobileView, AuthScreenTabletView,
                                AuthScreenDesktopView)
from .auth_screen_views import (SignUpScreenMobileView, SignUpScreenTabletView,
                                SignUpScreenDesktopView)

# all screens
AUTH_SCREEN = "auth_screen"
SIGNUP_SCREEN = "signup_screen"
SIGNIN_SCREEN = "signin_screen"

# -------------------------- AUTHSCREEN-CLASS ------------------------


class CreateAuth(Base):
    def __init__(self, screenmanager: object = None, *args, **kw):
        super().__init__(name=AUTH_SCREEN, screenmanager=screenmanager,
                         *args, **kw)

        # Set-up all the different type of layouts for the Login Screen.
        self.load_kv_file(["auth_screen_mobile", "auth_screen_tablet",
                          "auth_screen_desktop"])

        self.mobile_view = AuthScreenMobileView(master=self)
        self.tablet_view = AuthScreenDesktopView(master=self)
        self.desktop_view = AuthScreenTabletView(master=self)
    
    def create_screen(self, screen_name: str) -> None:
        """:method: create a screen with a given screen_name and
            add to the main screenmanager. This method is manily used
            in response to the sign-up and sign-in button.

            :param screen_name: name of the screen.
        """
      
        if screen_name.lower() == "sign in":
            print("sign in")
        elif screen_name.lower() == "sign up":
            print("sign up")
            SignUpScreen()  # create a sign in screen
            self.screenmanager.current = SIGNUP_SCREEN


# -------------------------- SIGNUPSCREEN-CLASS ------------------------


class SignUpScreen(Base):
    """:about: class handles the sign in process for the application."""
    def __init__(self, screenmanager: object = None, *args, **kwargs):
        super().__init__(SIGNUP_SCREEN, screenmanager, *args, **kwargs)

        # loading a customizable view
        self.mobile_view = SignUpScreenMobileView(master=self)
        self.tablet_view = SignUpScreenTabletView(master=self)
        self.desktop_view = SignUpScreenDesktopView(master=self)

    def on_submit_info(self, instance: object):
        print(instance.text)

# class SignUpCommanMethods():
#   def __init__(self):
#       # store the information about the sign up.
#       '''data = {"username": None, "email": None, "password": None, "profession": None,
#       "code": None, "year": None, "course": None}'''
#       self.data = {}

#       # creating the profession drop down list
#       self.dropdown = ProfessionDropDown()
#       self.yeardropdown = YearDropDown()
#       self.coursedropdown = CourseDropDown()

#       # track the binding status of dropdown, basically this boolen ensure that it showing
#       # the appropriate selected text at with (widget) it attached.
#       self.dropdown_is_bind = False

#   def on_submit(self) -> None:
#       """:method: """
#       print(self.children)

#   def open_profession_drop_down(self, widget_object: object) -> None:
#       """"""
#       self.dropdown.open(widget_object)

#       if not self.dropdown_is_bind:
#           self.dropdown.bind(on_select= lambda instance, x: setattr(widget_object, "text", x))
#           self.dropdown.bind(on_select= self.on_open_profession_drop_down)
#           self.dropdown_is_bind = True

#   def on_open_profession_drop_down(self, widget_object: object, data: str) -> None:
#       """"""
#       selected_profession = data
#       # attaching appropriate field according to the select profession
#       if selected_profession == "STUDENT":
#           # create a drop down for couse selection
#           label1 = Label(text="Course :")
#           btn1 = Button(text="select course")
#           btn1.bind(on_press=self.coursedropdown.open)
#           self.coursedropdown.bind(on_select= lambda instance, x: setattr(btn1, "text", x))
            
#           # create a drop down for year selection
#           label2 = Label(text="Year")
#           btn2 = Button(text="select admission year")
#           btn2.bind(on_press=self.yeardropdown.open)
#           self.yeardropdown.bind(on_select= lambda instance, x: setattr(btn2, "text", x))

#           # adding the field to the sign_up_form
#           self.ids.sign_up_form.add_widget(label1)
#           self.ids.sign_up_form.add_widget(btn1)
#           self.ids.sign_up_form.add_widget(label2)
#           self.ids.sign_up_form.add_widget(btn2)

#       elif selected_profession == "PROFESSOR":
#           print("PROFESSOR")
#       elif selected_profession == "ADMIN":
#           print("ADMIN")

# class SignUpScreenMobileView(SignUpCommanMethods, MDBoxLayout):
#   def __init__(self, *args, **kwargs):
#       SignUpCommanMethods.__init__(self)
#       MDBoxLayout.__init__(self, *args, **kwargs)

# class ProfessionDropDown(DropDown):
#   pass

# class YearDropDown(DropDown):
#   """"""
#   def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)

#       self.add_year(current_year=2023, highest_semister=8)

#   def add_year(self, current_year: int, highest_semister: int) -> None:
#       """:param heighest_semester: height ongoing semester number (eg: 8) in the college for calculation
#           total year should be present in the drop down list.
#       """
#       for i in range(0, highest_semister + 1):
#           text = str(current_year - i)
#           btn = Button(text=text, size_hint_y = None, height= dp(20))
#           btn.bind(on_release = lambda instance: self.select(instance.text))
#           self.add_widget(btn)

# class CourseDropDown(DropDown):
#   def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#       self.courses = {"BSc. Comp (Hons.)", "Bsc. Math (Hons.)"}

#       self.add_course()

#   def add_course(self):
#       """"""
#       for course in self.courses:
#           btn = Button(text=course, size_hint_y = None, height= dp(20))
#           btn.bind(on_release = lambda instance: self.select(instance.text))
#           self.add_widget(btn)
