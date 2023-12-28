# messages
import email


USER_EXISTS = "Account with the same email is already exists."
USER_CREATED = "Account created successfully. We have sent account verification link on this email: {email}"
SUBSCRIPTION_ADDED = "Subscription is added Successfully with Id : {id} "
USER_UPDATED = "Account : {username}'s information updated successfully."
INVALID_DETAILS_FORMAT = "Please enter details with proper format"
INVALID_USERNAME_FORMAT = "Invalid Username."
INVALID_PASSWORD_FORMAT = "Invalid Password."
INVALID_EMAIL_FORMAT = "Invalid Email."
INVALID_FIRST_NAME = "Invalid First Name."
INVALID_LAST_NAME = "Invalid Last Name."
INVALID_MOBILE_NUMBER = "Invalid Mobile Number."
FIELDS_MISSING = "Fields Missing."
SOMETHING_WENT_WRONG = "Something Went Wrong."
ACCOUNT_DISABLED = "Your account is disabled. Please contact to Administrator."
INVALID_CREDENTIALS = "Invalid Email or Password. Please Try Again."
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
EMAIL_VERIFICATION_LINK_SHARED='Account verification is pending, We have sent account verification link on this email: {email}'
RESET_PASSWORD_EMAIL_SENT = 'Password reset link sent on your registered email address.'
EMAIL_IS_NOT_VERIFIED = "Email is not verified or doesn't exist."
ACCOUNT_DOESNT_EXIST="Account does not exist."
PASSWORD_AND_OLD_PASSWORD_ARE_SAME="Password and old passwords are same.Please choose another one."
PASSWORD_CHANGED_SUCCESSFULLY = "Password changed successfully."
YOU_DONT_HAVE_PERMISSION_TO_PERFORM_THIS_ACTION="You don't have permissions to perform this action."
OTP_SHARED_SUCCESSFULLY="OTP is shared succssfully on {mobile}."
OTP_IS_EXPIRED = "OTP is already expired."
INVALID_OTP="Entered OTP is invalid."
MOBILE_NUMBER_VERIFIED="Mobile number is verified successfully"

# Regex
PASSWORD_PATTERN = "^(?!.*\s)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{10,}$"
USERNAME_PATTERN = "^(?!.*\s)(?=.*[a-z])[a-z0-9]{7,30}$"
EMAIL_PATTERN = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$"
MOBILE_NUMBER_PATTERN = "[0-9]{10,16}"
FIRST_NAME_PATTERN = "^[A-Za-z]{3,100}$"
LAST_NAME_PATTERN = "^[A-Za-z]{3,50}$"

# SMS Sending API
NETTYFISH_MESSAGE_SEND_URL="https://sms.nettyfish.com/api/v2/SendSMS"
MESSAGE_TEMPLATE="Your OTP for Registering your number on WACTO is {generated_otp}, The one time password is valid for {minutes} minutes from the time it is generated NETTYFISH"