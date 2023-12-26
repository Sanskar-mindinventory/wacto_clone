# messages
import email


USER_EXISTS = "User with {username} is already exists."
USER_CREATED = "User: {username} created Successfully. Id : {id}"
SUBSCRIPTION_ADDED = "Subscription is added Successfully with Id : {id} "
USER_UPDATED = "User : {username}'s data is updated successfully."
INVALID_DETAILS_FORMAT = "Please enter details with proper format"
INVALID_USERNAME_FORMAT = "Invalid Username format."
INVALID_PASSWORD_FORMAT = "Invalid Password format."
INVALID_EMAIL_FORMAT = "Invalid Email format."
INVALID_FIRST_NAME = "Invalid First Name format."
INVALID_LAST_NAME = "Invalid Last Name format."
INVALID_MOBILE_NUMBER = "Invalid Mobile Number format."
FIELDS_MISSING = "Fields Missing."
SOMETHING_WENT_WRONG = "Something Went Wrong."
ACCOUNT_DISABLED = "Your account is disabled. Please contact to Administrator."
INVALID_CREDENTIALS = "Invalid Username or Password. Please Try Again."
USER_DOES_NOT_EXIST = "User doesn't exist with id: {id}"
SUBSCRIPTION_DOES_NOT_EXIST = "Subscription doesn't exist with id: {id}"
YOU_CAN_NOT_UPDATE = ". So,You can't update."
SOURCE_ERROR = "source missing or empty."
COUNTRY_CODE_MISSING = "Country code missing or empty."
INVALID_COUNTRY_CODE = "Please enter valid country code"
MOBILE_NUMBER_ALREADY_EXIST = "Mobile number already exist."
PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH = "Password and conﬁrm password doesn’t match."
SUBSCRIPTION_UPDATED = "Subscription : {id}'s data is updated successfully."
EMAIL_SENT_SUCCESSFULLY = "Email is sent successfully on {email}"
EMAIL_VERIFICATION_LINK_SHARED='Please verify your email, link is shared on {email}'

# Regex
PASSWORD_PATTERN = "^(?!.*\s)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{10,}$"
USERNAME_PATTERN = "^(?!.*\s)(?=.*[a-z])[a-z0-9]{7,30}$"
EMAIL_PATTERN = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$"
MOBILE_NUMBER_PATTERN = "[0-9]{10,16}"
FIRST_NAME_PATTERN = "^[A-Za-z]{3,100}$"
LAST_NAME_PATTERN = "^[A-Za-z]{3,50}$"