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
        {"username": ["id", "value"], "email": ["id", "value]"],
        "password": ["id", "value"], "roll": ["id", "value"],
        "course": ["id", "value"], "admission-data": ["id", "value"],
        "code": ["id", "value"]}
        '''

        self.data = {"username": [None, None],
                     "email": [None, None], 
                     "password": [None, None],
                     "roll": [None, None],
                     "courses": [None, None], 
                     "year-of-admission": [None, None],
                     "code": [None, None]}

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

        # clearing widgets from the parent class.
        if self.dropdown_controll_widget:
            self.dropdown_controll_widget.text = text

            # entry to the data
            self.data[self.current_dropdown_data_key] = \
                     [self.dropdown_controll_widget, text]
        
        if text == "Student" or text == "Professor":
            self.current_view.ids.roll_box.clear_widgets()
        
        # closing the drop-down instance when the value in selected for the
        # drop-down list.
        instance.dismiss()

        if text == "Student":
            '''
            Reset the professor data because user-had selected the student data
            after typing the professor data
            '''
            if self.data["code"][1]:
                self.data["code"] = [None, None]

            student_roll = Factory.StudentRoll()
            student_roll.master = self
            self.current_view.ids.roll_box.add_widget(student_roll)
        elif text == "Professor":
            '''
            Reset the student data because user-had selected the professor data
            after typing the student data
            '''
            if self.data["courses"][1] or self.data["year-of-admission"][1]:
                self.data["courses"] = self.data["year-of-admission"] = \
                    [None, None]

            professor_roll = Factory.ProfessorRoll()
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
                self.data["username"] = [instance, instance.text]
            else:
                self.data["username"] = [instance, None]

        # logic for valid email
        if text == "email":
            if "@gmail.com" in instance.text and \
             len(instance.text) > len("@gmail.com"):

                self.data["email"] = [instance, instance.text]
            else:
                self.data["email"] = [instance, None]

        if text == "code":
            if len(instance.text) > 2:
                self.data["code"] = [instance, instance.text]
            else:
                self.data["code"] = [instance, None]

    def check_password_strength(self, instance: object, text: str) -> None:
        '''
        :method: used for the checking the stength of the password beside
        this also able to provide the suggestion for imporving password.
        '''
        if len(text) > 0:
            result = zxcvbn(text, user_inputs=None)
            '''
            calculate the strength of the password, password strength between
            (0-4)
            '''
            score = float(result["score"]/4)
            self.current_view.ids.progressbar.value = score * 100
            progressbar_color = (1 - score, score, 0, 1)
            self.current_view.ids.progressbar.color = progressbar_color

            if score == 1.0:
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

                self.data["password"] = [instance, instance.text]
        else:
            instance.color_text = colors["Red"]["900"]
            self.current_view.ids.password_suggestion.text_color = \
                colors["Red"]["800"]
            self.current_view.ids.password_suggestion.text = """Password \
            should greater than 8 contain (A-Z/a-z/0-9/@!..)"""

            self.data["password"] = [instance, None]

    def submit(self) -> None:
        '''
        :method: is the last step-to-conform the form would be submit in the
        the surver or not. It makes sure all the entry field are fill with
        appropriate text. If not it would inform-the user before submiting
        the form.
        '''

        # checking if any field is remain empty after pressing button
        if self.data["username"][1]:
            if self.data["email"][1]:
                if self.data["password"][1]:
                    if self.data["roll"][1]:

                        # if student try to sign up
                        if self.data["roll"][1] == "Student":
                            if self.data["courses"][1]:
                                if self.data["year-of-admission"][1]:
                                    # move-to-next-level
                                    dump("Test/data.txt",
                                         value= self.create_submit_data(self.data))
                                elif self.data["year-of-admission"][0]:
                                    self.data["year-of-admission"][0].theme_text_color = \
                                         colors["Red"]["900"]
                            elif self.data["courses"][0]:
                                self.data["courses"][0].theme_text_color = \
                                 colors["Red"]["900"]
                        
                        # if professor trying to sign-up
                        elif self.data["roll"][1] == "Professor":
                            if self.data["code"][1]:
                                # move-to-next-level
                                dump("Test/data.txt", value=self.create_submit_data(
                                    self.data))
                            elif self.data["code"][0]:
                                self.data["code"][0].theme_text_color = \
                                     colors["Red"]["900"]
                    
                    elif self.data["roll"][0]:
                        self.data["roll"][0].theme_text_color = colors["Red"]["900"]
                elif self.data["password"][0]:
                    self.data["password"][0].hint_text_color = colors["Red"]["900"]
            elif self.data["email"][0]:
                self.data["email"][0].hint_text_color = colors["Red"]["900"]
        elif self.data["username"][0]:
            self.data["username"][0].hint_text_color = colors["Red"]["900"]

    def create_submit_data(self, data: dict) -> dict:
        '''
        :method: created a new data which would be read to save to the server,
        because this method extract/elemenate all the object from the data.

        :param data: a dict of a data that would be modified.

        :return: a dict of new data which should be save over the server.
        '''
        data = {}
        # TODO: FIND ERROR WHY THE DICT ITEM IS NOT REATURING ANY THINGS
        print(data.items())

        for key, value in data.items():
            print(key, value)
            data[key] = value[1]

        return data

    def view_term_and_policy(self, instance, value) -> None:
        print(value)

    # EVENT
    # TODO: ADD THE CODE FOR CLOSING POP-UP
    # LET SUPPOSE SOME ONE OPEN POP-UP BUT WITHOUT CLOSING IT THEY BACKED FROM
    # THE GIVE SCREEN IN THAT SITUATION WE MENUALLY HAVE TO CLOSE THE POP-UP
    def on_leave(self):
        print("Leave")
