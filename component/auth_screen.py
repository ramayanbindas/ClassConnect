'''
# version: 1.0.0
:about: This module build the authentication system layout and functionality,

:class:
    [CreateAuth, SignUpScreen, SignInScreen]
'''

from kivymd.uix.menu import MDDropdownMenu
from kivymd.color_definitions import colors

# import in-built module
from .utils import Base
from .auth_screen_views import (AuthScreenMobileView, AuthScreenTabletView,
                                AuthScreenDesktopView)
from .auth_screen_views import (SignUpScreenMobileView, SignUpScreenTabletView,
                                SignUpScreenDesktopView)

from .settings import SPECIAL_CHAR, NUMBER, UPPER_CASE, LOWER_CASE

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
            self.manager.current = SIGNUP_SCREEN


# -------------------------- SIGNUPSCREEN-CLASS ------------------------


class SignUpScreen(Base):
    """:about: class handles the sign in process for the application."""
    USERNAME_MIN_LIMIT = 6

    def __init__(self, screenmanager: object = None, *args, **kwargs):
        super().__init__(SIGNUP_SCREEN, screenmanager, *args, **kwargs)

        self.data = {"username": "", "email": "", "password": "", "profession": "",
                     "course": "", "admission-data": "", "code": ""}

        # loading a customizable view
        self.mobile_view = SignUpScreenMobileView(master=self)
        self.tablet_view = SignUpScreenTabletView(master=self)
        self.desktop_view = SignUpScreenDesktopView(master=self)

    # creating drop-down for the form
    def drop_down(self, instance: object, text: str) -> None:
        ''':method: is used in creating the drop-down menu items used for
            selecting profession, courses, year-of-admission.
           
           :param instance: object of the caller of the drop down menu.
           :param text: text should be amoung the data key, which value
           could be loaded in the drop-down items list.
        '''
        data = {"profession": ["STUDENT", "TEACHER", "ADMIN"]}

        self.menu = MDDropdownMenu(caller=instance, position="center")

        # creating a menu items list and set items to the instace after release
        # event called in the instance widget.
        # TODO: ITMES NOT SHOWN IN THE DROPDOWN MENU
        menu_items = [
            {
              "text": x,
              "md_bg_color": "#bdc6bo",
              "on_release": lambda x: self.set_item_and_close_dropdown(instance, x)
            } for x in data[text]]

        self.menu.items = menu_items

        self.menu.open()  # opening the dropdown menu here.

    def set_item_and_close_dropdown(self, instance: object, text: str) -> None:
        '''
        :method: use to set text to the caller or the dropdown, and also used
        for closing the drop-down menu. This function is only used by the 
        instance whom are used for creating drop-down menu.

        :param instance: caller instance of the drop-down menu
        :param text: text which should be display over the caller instance.
        '''
        instance.text = text
        # closing the drop-down instance when the value in selected for the
        # drop-down list.
        self.menu.dismiss()
        print(self.menu)

    def check_input_validation(self, instance: object, text: str) -> None:
        '''
        :method: takes care of TextField present in the sign-up form, it
        contains logic, and also take care of visual responce accordingly.

        :param instance: of the TextInput object.
        :param text: aviable of option ("username", "email", "password",
        "profession", "course", "admission-year", "code"). In short the
        key value of the `self.data` varaibel.
        '''
        
        # TODO: FOCUS LEFT AND FOCUS NORMAL NOT WORKING PORPERLY.
        # logic for accepting username
        if text == "username":
            if len(instance.text) < self.USERNAME_MIN_LIMIT:
                instance.helper_text_color_focus = colors["Red"]["800"]
                instance.helper_text_color_normal = colors["Red"]["800"]
            else:
                instance.helper_text_color_focus = colors['Green']['800']
                instance.helper_text_color_normal = colors["Green"]["800"]
                self.data[text] = instance.text

        # logic for valid email
        if text == "email":
            if "@gmail.com" in instance.text and len(instance.text) > len("@gmail.com"):
                self.data[text] = instance.text
                print(instance.text)

        # TODO: MAKE IS MORE RESPONSIZE AND EFFECTIVE
        # logic for valid password
        if text == "password":
            progressbar_id = self.current_view.ids.progressbar
            if len(instance.text) > self.USERNAME_MIN_LIMIT:
                # logic for filtering strong password.
                progressbar_id.value = 10

                S = check_match_for_password("S", instance.text)
                N = check_match_for_password("N", instance.text)
                U = check_match_for_password("U", instance.text)
                L = check_match_for_password("L", instance.text)

                if S or N or U or L:
                    progressbar_id.value = 20
                    
                    # combination of twos
                    if (S and N) or (S and U) or (S and L) or (N and U) or \
                       (N and L) or (U and L):
                        progressbar_id.value = 60
                    
                    # combination of threes
                    if (S and U and N) or (S and N and L) or (N and U and L)\
                       or (S and U and L):
                        progressbar_id.value = 80

                if S and N and U and L:  # cobination of four.
                    progressbar_id.value = 100

                instance.helper_text_color_focus = (0, 0, 0, 1)
                instance.helper_text_color_normal = (0, 0, 0, 1)

            else:
                progressbar_id.value = 0
                instance.helper_text_color_focus = colors["Red"]["800"]
                instance.helper_text_color_normal = colors["Red"]["800"]


# TODO: MAKE THIS MATCHING FUNCTION ALGORITH MORE EFFICIENT
# BASED OVER MEMORY AND PROCESSING TIME.
def check_match_for_password(check: str, text: str) -> bool:
    '''
    :function: use for checking the strangth of the password.

    :param check: options ("S", "N", "U", "L")
            "S" for checking if special character persent it the text.
            "N" for checking if nuber present in the text.
            "U" for upper-case letter.
            "L" for lower-case letter.
    :param text: within which it perfore checks.

    :return: True if those symbol are persent if not than False.
    '''
    if check == 'S':
        for i in SPECIAL_CHAR:
            if i in text:
                return True
    elif check == "N":
        for i in NUMBER:
            if i in text:
                return True

    elif check == "U":
        for i in UPPER_CASE:
            if i in text:
                return True

    elif check == "L":
        for i in LOWER_CASE:
            if i in text:
                return True

    return False
