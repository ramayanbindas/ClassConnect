'''
# version: 1.0.0
:about: This module build the authentication system layout and functionality,

:class:
    [CreateAuth, SignUpScreen, SignInScreen]
'''

from kivymd.color_definitions import colors
from kivymd.uix.list.list import OneLineListItem

from kivy.uix.dropdown import DropDown
from kivy.factory import Factory

from zxcvbn import zxcvbn

# import in-built module
from .utils import Base
from .auth_screen_views import (AuthScreenMobileView, AuthScreenTabletView,
                                AuthScreenDesktopView)

from .auth_screen_views import (SignUpScreenMobileView, SignUpScreenTabletView,
                                SignUpScreenDesktopView)

from .support import dump
from .settings import *

# all screens
AUTH_SCREEN = "auth_screen"
SIGNUP_SCREEN = "signup_screen"
SIGNIN_SCREEN = "signin_screen"

COURSES = ["BSc. Comp(H)", "Bsc. Math(H)"]
YEAR_OF_ADDMISSION = ["2023-2024", "2022-2023"]

# -------------------------- AUTHSCREEN-CLASS ------------------------


class CreateAuth(Base):
    def __init__(self, screenmanager: object = None, *args, **kw):
        super().__init__(name=AUTH_SCREEN, screenmanager=screenmanager,
                         *args, **kw)

        # Set-up all the different type of layouts for the Login Screen.
        self.load_kv_file(["auth_screen_mobile", "auth_screen_tablet",
                          "auth_screen_desktop"])

        self.mobile_view = AuthScreenMobileView(master=self)
        self.tablet_view = AuthScreenTabletView(master=self)
        self.desktop_view = AuthScreenDesktopView(master=self)

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
            self.manager.current = SIGNUP_SCREEN


# -------------------------- SIGNUPSCREEN-CLASS ------------------------


class SignUpScreen(Base):
    """:about: class handles the sign in process for the application."""
    USERNAME_MIN_LIMIT = 6

    def __init__(self, screenmanager: object = None, *args, **kwargs):
        super().__init__(SIGNUP_SCREEN, screenmanager, *args, **kwargs)
        
        # loading a customizable view
        self.mobile_view = SignUpScreenMobileView(master=self)
        self.tablet_view = SignUpScreenTabletView(master=self)
        self.desktop_view = SignUpScreenDesktopView(master=self)

        '''
        {"name_of_field": value_of_the_field}
        '''

        self.data = {"username": None,
                     "email": None, 
                     "password": None,
                     "roll": None,
                     "courses": None, 
                     "year-of-admission": None,
                     "code": None}

        self.dropdown = DropDown()
        '''
        Stote the instance which is currently controlling the dropdown
        '''
        self.dropdown_controll_widget = None
        '''
        Store the current key of the data used for the entry to the main
        data
        '''
        self.current_dropdown_data_key = None
        self.dropdown.bind(on_select=self.set_item_and_close_dropdown)

    # creating drop-down for the form
    def drop_down(self, instance: object, text: str) -> None:
        ''':method: is used in creating the drop-down menu items used for
            selecting profession, courses, year-of-admission.
           
           :param instance: object of the caller of the drop down menu.
           :param text: text should be amoung the data key, which value
           could be loaded in the drop-down items list.
        '''
        data = {"roll": ["Student", "Professor"], "courses": COURSES, 
                "year-of-admission": YEAR_OF_ADDMISSION}

        # clear widget if their is a widget in the dropdown
        if self.dropdown.children:
            self.dropdown.clear_widgets()

        # creating a list for the dropdown
        for item in data[text]:
            widget = OneLineListItem(
                text=item,
                bg_color=(1, 1, 1, 1),
                on_release=lambda x, item=item: self.dropdown.select(item)
                )
            self.dropdown.add_widget(widget)
        
        # attaching the dropdown with the instance
        self.dropdown_controll_widget = instance
        self.current_dropdown_data_key = text
        self.dropdown.open(instance)

    def set_item_and_close_dropdown(self, instance: object, text: str) -> None:
        '''
        :method: use to set text to the caller or the dropdown, and also used
        for closing the drop-down menu. This function is only used by the 
        instance whom are used for creating drop-down menu.

        :param instance: dropdown instance
        :param text: text which should be display over the caller instance.
        '''

        '''
        Add a text to the dropdown caller widget as any item is selected from
        the the list
        '''
        if self.dropdown_controll_widget:
            self.dropdown_controll_widget.text = text

            # entry a text of item select in the data
            self.data[self.current_dropdown_data_key] = text

        '''
        First check if the roll_box[MDBoxLayout] contains any child, then clear
        and add a new selection of widgets according to the user-roll selected.
        '''
        if text == "Student" or text == "Professor":
            self.current_view.ids.roll_box.clear_widgets()
        
        # closing the drop-down instance when the value in selected 
        # from the drop-down list.
        instance.dismiss()

        if text == "Student":
            '''
            Reset the professor data because user-had selected the student data
            after typing the professor data
            '''
            if self.data["code"]:
                self.data["code"] = None

            student_roll = Factory.StudentRoll()
            '''
            Assigning a screen instance [SignUpScreen] to the kv file class,
            allowing them to access this class methods to call.
            '''
            student_roll.master = self
            self.current_view.ids.roll_box.add_widget(student_roll)
        elif text == "Professor":
            '''
            Reset the student data because user-had selected the professor data
            after typing the student data
            '''
            if self.data["courses"] or self.data["year-of-admission"]:
                self.data["courses"] = self.data["year-of-admission"] = None

            professor_roll = Factory.ProfessorRoll()
            '''
            Assigning a screen instance [SignUpScreen] to the kv file class,
            allowing them to access this class methods to call.
            '''
            professor_roll.master = self
            self.current_view.ids.roll_box.add_widget(professor_roll)

    def check_input_validation(self, instance: object, text: str) -> None:
        '''
        :method: takes care of TextField present in the sign-up form, it
        contains logic, and also take care of visual responce accordingly.

        :param instance: of the TextInput object.
        :param text: aviable of option ("username", "email").
        In short the key value of the `self.data` varaibel.
        '''
        
        # entry to the data
        if text == "username":
            if len(instance.text) > 2:
                self.data["username"] = instance.text

        # logic for valid email
        if text == "email":
            if "@gmail.com" in instance.text and \
             len(instance.text) > len("@gmail.com"):
                self.data["email"] = instance.text

        # logic for the code type by the professor
        if text == "code":
            self.data["code"] = instance.text

    def check_password_strength(self, instance: object, text: str) -> None:
        '''
        :method: used for the checking the stength of the password beside
        this also able to provide the suggestion for imporving password.
        '''
        # turning the password text color into red
        self.current_view.ids.password.text_color_focus = colors["Red"]["900"]

        if len(text):
            result = zxcvbn(text, user_inputs=None)
            '''
            calculate the strength of the password, password strength between
            (0-1)
            '''
            score = float(result["score"]/4)
            self.current_view.ids.progressbar.value = score * 100
            '''
            progressbar color changes accroding to the score [RED-GREEN]
            '''
            progressbar_color = (1 - score, score, 0, 1)
            self.current_view.ids.progressbar.color = progressbar_color

            # providing a suggestion for making the password strong
            if result["feedback"]["warning"]:
                self.current_view.ids.password_suggestion.text = \
                 str(result["feedback"]["warning"])
                self.current_view.ids.password_suggestion.text_color = \
                    colors["Red"]["800"]
            
            elif result["feedback"]["suggestions"]:
                self.current_view.ids.password_suggestion.text = \
                    str(result["feedback"]["suggestions"][0])
                self.current_view.ids.password_suggestion.text_color = \
                    (0.5, 0.5, 0, 1)

            if score == 1.0:
                # if the password have the higest score 1 then it would be accepted.
                self.data["password"] = instance.text

                # Reset the colors
                self.current_view.ids.password.text_color_focus = colors["Green"]["900"]

        else:
            '''
            If the length of text is zero then a message is show.
            '''
            self.current_view.ids.password_suggestion.text_color = \
                colors["Red"]["800"]
            self.current_view.ids.password_suggestion.text = \
                """Password should greater than 8 contain (A-Z/a-z/0-9/@!..)"""

    def submit(self) -> None:
        '''
        :method: is the last step-to-conform the form would be submit in the
        the surver or not. It makes sure all the entry field are fill with
        appropriate text. If not it would inform-the user before submiting
        the form.
        '''
        '''
        making sure that all the field are enter porperly, by a value and if 
        not a pop up would be shown to user to fill the value. If yes we are
        ready for the next step
        '''
        if self.conform_data(self.data):
            # move to the next step
            dump("Test/data.txt", mode="a", value=self.data)
        else:
            # show pop-up
            print("Please fill all the field in the form!")

    def conform_data(self, data: dict) -> bool:
        '''
        :method: used to conform a data that all the value are correctly 
        extracted from the the appication.

        :param dict: a dict of data where to check the value.

        :return: True if the value are collected correctly else False
        '''

        # fileds
        # {"username", "email", "password", "roll", "courses",
        # "year-of-admission", "code"}

        # rolls
        # {"Student", "Professor"}

        student_data_keys = {"username", "email", "password", "courses", "year-of-admission"}
        professor_data_keys = {"username", "email", "password", "code"}

        if data["roll"] == "Student":
            # conform student data
            for key in student_data_keys:
                if not data[key]:
                    return False

            return True
        
        elif data["roll"] == "Professor":
            # conform Professor data
            for key in professor_data_keys:
                if not data[key]:
                    return False

            return True

        else: return False  # if either of them are not selected  # noqa: E701

    def view_term_and_policy(self, instance, value) -> None:
        print(value)

    # EVENT
    # TODO: ADD THE CODE FOR CLOSING POP-UP
    # LET SUPPOSE SOME ONE OPEN POP-UP BUT WITHOUT CLOSING IT THEY BACKED FROM
    # THE GIVE SCREEN IN THAT SITUATION WE MENUALLY HAVE TO CLOSE THE POP-UP
    def on_leave(self):
        print("Leave")
