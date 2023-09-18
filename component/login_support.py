""""""
from hashlib import sha256
from secrets import token_hex

class SecurePasswordGenerator:
	def __init__(self, password: str):
		self.set_password()

	def create_hash(self, salt: str) -> str:
		""":about: internal method takes a string as param and return a
			hash password
		"""

		self.password = self.password + salt
		p = sha256() # create a hash object
		p.update(self.password.encode("utf-8"))
		return p.hexdigest()

	def generate_salt(self) -> str:
	    """:about: method randomly generate salt"""
	    salt = token_hex() # generae the salt with help of secrets module
	    return salt

	def create_password(self) -> tuple[str, str]:
	    """:about: method return hashpassword and the salt"""
	    salt = self.generate_salt()
	    hashpassword = self.create_hash(salt) # secure password is created
	    return (hashpassword, salt)

	def match_password(self, salt: str, correct_password: str) -> bool:
	    """:about: method helps in matching the password from database and return a True if matched
	        else False
	    """
	    hashpassword = self.create_hash(salt)
	    if hashpassword == correct_password:
	        return True # password matched

	    return False

	def set_password(self, password: str) -> None:
		""":about: setter method for password"""
		if type(password) != str: password = str(password)

		self.password = password

def captha():
    """:about: function handles the captha functionality"""
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
           "y", "z"]

    captha_string = randomletter_generator(choice([4, 5, 6]))
    captha_input = str(input(f"Type the captha text: {captha_string}: "))
    if captha_input != captha_string:
        exit()

    return True