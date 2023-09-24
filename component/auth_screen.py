'''
# version: 1.0.0
:about: This module build the authentication system layout and functionality,

:class:
    [CreateAuth, SignUpScreen, SignInScreen]
'''

from kivymd.color_definitions import colors
from kivymd.uix.list.list import OneLineListItem
from kivymd.uix.button import MDRaisedButton

from kivy.uix.dropdown import DropDown
from kivy.factory import Factory

from zxcvbn import zxcvbn

# import in-built module
from .utils import BaseScreen
from .auth_screen_views import (AuthScreenMobileView, AuthScreenTabletView,
                                AuthScreenDesktopView)

from .auth_screen_views import (SignUpScreenMobileView, SignUpScreenTabletView,
                                SignUpScreenDesktopView)

from .auth_screen_views import (SignInScreenMobileView, SignInScreenTabletView,
                                SignInScreenDesktopView)

from .support import dump


# name of all the screen in the login process
AUTH_SCREEN_NAME = "auth_screen"
SIGNUP_SCREEN_NAME = "signup_screen"
SIGNIN_SCREEN_NAME = "signin_screen"

# variable for the sign-up-process.
ROLL = ["Student", "Professor"]
COURSES = ["BSc. Comp(H)", "BSc. Math(H)"]
YEAR_OF_ADDMISSION = ["2023-2024", "2022-2023"]


# -------------------------- AUTHSCREEN-CLASS ------------------------


class CreateAuth(BaseScreen):
    def __init__(self, *args, **kw):
        super().__init__(name=AUTH_SCREEN_NAME, *args, **kw)

        # Set-up all the different type of layouts for the Login Screen.
        self.load_kv_file(["auth_screen_mobile", "auth_screen_tablet",
                          "auth_screen_desktop"])

        self.mobile_view = AuthScreenMobileView(master=self)
        self.tablet_view = AuthScreenTabletView(master=self)
        self.desktop_view = AuthScreenDesktopView(master=self)

    def create_screen(self, screen_name: str) -> None:
        """:method: create a screen with a given screen_name and
            add to the main screenmanager. This method is mainly used
            in response to the sign-up and sign-in button.

            :param screen_name: name of the screen.
        """
      
        if screen_name.lower() == "sign in":
            SignInScreen()
            self.manager.current = SIGNIN_SCREEN_NAME
        elif screen_name.lower() == "sign up":
            SignUpScreen()  # create a sign in screen
            self.manager.current = SIGNUP_SCREEN_NAME


# -------------------------- SIGNUPSCREEN-CLASS ------------------------


class SignUpScreen(BaseScreen):
    """:about: class handles the sign in process, layout & logic
       for the application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(SIGNUP_SCREEN_NAME, *args, **kwargs)
        
        # loading a customizable view
        self.mobile_view = SignUpScreenMobileView(master=self)
        self.tablet_view = SignUpScreenTabletView(master=self)
        self.desktop_view = SignUpScreenDesktopView(master=self)

        # creating data for the app
        self.create_data()

        self.dropdown = DropDown()
        '''
        Stote the instance which is currently controlling the dropdown
        '''
        self.dropdown_controll_widget = None
        '''
        Store the current key of the data used to identify which dropdown
        is used by the application and also used for entry key to data.
        '''
        self.current_dropdown_data_key = None
        self.dropdown.bind(on_select=self.set_item_and_close_dropdown)

    def create_data(self) -> None:
        '''
        :method: create a data which work for this function.
            {"name_of_field": value_of_the_field}

        :Note: This data may not be same with the server data.
        '''
        self.student_data_keys = {"username", "email", "password", "courses",
                                  "year-of-admission"}

        self.professor_data_keys = {"username", "email", "password", "code"}

        self.data = {"username": None,
                     "email": None, 
                     "password": None,
                     "roll": None,
                     "courses": None, 
                     "year-of-admission": None,
                     "code": None}

    # creating drop-down for the form
    def drop_down(self, instance: object, text: str) -> None:
        ''':method: is used in creating the drop-down menu items used for
            selecting profession, courses, year-of-admission.
           
           :param instance: object of the caller of the drop down menu.
           :param text: text should be among the data key, which value
           could be loaded in the drop-down items list.
        '''
        data = {"roll": ROLL, "courses": COURSES, 
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
        if text in ROLL:
            self.current_view.ids.roll_box.clear_widgets()
        
        # closing the drop-down instance when the value in selected 
        # from the drop-down list.
        instance.dismiss()

        if text == ROLL[0]:
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
        elif text == ROLL[1]:
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
        contains logic, and also take care of visual response accordingly.

        :param instance: of the TextInput object.
        :param text: available of option ("username", "email").
        In short the key value of the `self.data` variable.
        '''
        
        # entry to the data
        if text == "username":
            if len(instance.text) > 2:
                # we only accept the data if the condition meet
                self.data["username"] = instance.text
            else:
                '''
                always clear the data if data not meet our condition,
                this is important because if the user type some-things
                then erase it, we need to erase the data too
                '''
                self.data["username"] = None

        # logic for valid email
        if text == "email":
            if not instance.error:
                self.data["email"] = instance.text
            else:
                '''
                always clear the data if data not meet our condition,
                this is important because if the user type some-things
                then erase it, we need to erase the data too
                '''
                self.data["email"] = None

        # logic for the code type by the professor
        if text == "code":
            if len(instance.text):
                self.data["code"] = instance.text
            else:
                self.data["code"] = instance.text

    def check_password_strength(self, instance: object, text: str) -> None:
        '''
        :method: used for the checking the strength of the password beside
        this also able to provide the suggestion for improving password.
        '''
        # turning the password text color into red
        self.current_view.ids.password.text_color_focus = colors["Red"]["900"]

        if len(text):
            result = zxcvbn(text, user_inputs=self.data.values())
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
        the server or not. It makes sure all the entry field are fill with
        appropriate text. If not it would inform-the user before submitting
        the form.
        '''
        '''
        making sure that all the field are enter properly, by a value and if 
        not a pop up would be shown to user to fill the value. If yes we are
        ready for the next step
        '''
        if self.conform_data(self.data):
            # move to the next step
            if self.data_submit_porcess(self.data):
                '''
                if the data is submit succesfully the application
                data get reset it not able to subit the same data
                again.
                '''
                self.create_data()
        else:
            # show pop-up
            btn = MDRaisedButton(text="OK")
            alertdialog = Factory.AlertDialog(title="Unable To Sign Up!",
                    text="Please fill all the field in the form.",
                    buttons=[btn])

            btn.bind(on_release=lambda instance: alertdialog.dismiss())
            alertdialog.open()

    def conform_data(self, data: dict) -> bool:
        '''
        :method: used to conform a data that all the value are correctly 
        extracted from the the application.

        :param dict: a dict of data where to check the value.

        :return: True if the value are collected correctly else False
        '''

        if data["roll"] == ROLL[0]:
            # conform student data
            for key in self.student_data_keys:
                if not data[key]:
                    return False

            return True
        
        elif data["roll"] == ROLL[1]:
            # conform Professor data
            for key in self.professor_data_keys:
                if not data[key]:
                    return False

            return True

        else: return False  # if either of them are not selected  # noqa: E701

    def data_submit_porcess(self, data: dict) -> bool:
        '''
        :method: communicate with the server, and conform the data had
        submit successfully or not.

        :return: True if submit successful else False
        '''
        try:
            dump("Test/data.txt", mode="a", value=data)
        except Exception as error:
            print(error)
            # data not able to submit to the server
            return False

        return True

    def view_term_and_policy(self, instance, value) -> None:
        print(value)

    # EVENT
    # TODO: ADD THE CODE FOR CLOSING POP-UP
    # LET SUPPOSE SOME ONE OPEN POP-UP BUT WITHOUT CLOSING IT THEY BACKED FROM
    # THE GIVE SCREEN IN THAT SITUATION WE MENUALLY HAVE TO CLOSE THE POP-UP
    def on_leave(self):
        '''
        :method: fired when the screen leave the current view.
        '''
        # closed the drop-down if it remains open
        if self.dropdown_controll_widget:
            self.dropdown_controll_widget.dismiss()

        # removing the widget from the screen manager
        self.manager.remove_widget(self)


# -------------------------- SIGNINSCREEN-CLASS ------------------------


class SignInScreen(BaseScreen):
    def __init__(self, *args, **kw):
        super().__init__(SIGNIN_SCREEN_NAME, *args, **kw)

        # loading a customizable view
        self.mobile_view = SignInScreenMobileView(master=self)
        self.tablet_view = SignInScreenTabletView(master=self)
        self.desktop_view = SignInScreenDesktopView(master=self)

        # creating data for the sign-in
        self.create_data()

    def create_data(self) -> None:
        '''
        :method: used to create a acceptable/compatible data for the
        class
        '''

        self.data = {"email": None, "password": None}

    def check_input_validation(self, instance: object, text: str) -> None:
        '''
        :method: takes care of TextField present in the sign-up form, it
        contains logic, and also take care of visual response accordingly.

        :param instance: of the TextInput object.
        :param text: available of option ("username", "email").
        In short the key value of the `self.data` variable.
        '''

        # logic for valid email
        if text == "email":
            if not instance.error:
                self.data["email"] = instance.text
            else:
                '''
                always clear the data if data not meet our condition,
                this is important because if the user type some-things
                then erase it, we need to erase the data too
                '''
                self.data["email"] = None

        # logic for the password type by the professor
        if text == "password":
            if len(instance.text):
                self.data["password"] = instance.text
            else:
                self.data["password"] = instance.text

    def submit(self) -> None:
        '''
        :method: is the last step-to-conform the form would be submit in the
        the server or not. It makes sure all the entry field are fill with
        appropriate text. If not it would inform-the user before submitting
        the form.
        '''
        '''
        making sure that all the field are enter properly, by a value and if 
        not a pop up would be shown to user to fill the value. If yes we are
        ready for the next step
        '''

        if self.conform_data(self.data):
            # move-to-the next step
            print(">>>>>>>>>Submit<<<<<<<<<")
            '''
            if the data is submit succesfully the application
            data get reset it not able to subit the same data
            again.
            '''
            self.create_data()
        else:
            # show the pop-up data submit rejected.
            btn = MDRaisedButton(text="OK")
            alertdialog = Factory.AlertDialog(title="Unable To Sign In!",
                    text="Please fill all the field in the form.",
                    buttons=[btn])

            btn.bind(on_release=lambda instance: alertdialog.dismiss())
            alertdialog.open()

    def conform_data(self, data: dict) -> None:
        '''
        :method: used to conform a data that all the value are correctly 
        extracted from the the application.

        :param dict: a dict of data where to check the value.

        :return: True if the value are collected correctly else False
        '''
        for value in data.values():
            if not value:
                return False

        return True

    def on_leave(self):
        '''
        :method: fired when the screen leave the current view.
        '''

        # removing the widget from the screen manager
        self.manager.remove_widget(self)