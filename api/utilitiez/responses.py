wrong_password = (
    "Password Must contain a Minimum 8 characters with atleast one upper case"
    " letter, atleast on lower case letter and  atleast one number."
)

wrong_status = "Status must either be 'resolved','under investigation','"
wrong_username = (
    "Username must be string with atleast 5 characters and may"
    " contain a number"
)
wrong_phone_number = "Phone number must be a string and strictly of ten digits"
wrong_email = "Please provide a valid email format"
wrong_name = (
    "Name field is a string and cannot be blank or contain a space or a number"
)
duplicate_email = "Email address already has an account"
duplicate_user_name = "Username already registered"
duplicate_phone_number = "phoneNumber already in use"
duplicate_comment = "incident comment already reported"
duplicate_title = "incident title already reported"

invalid_token_message = "Provide a valid Token, verification failed"
expired_token_message = "Token has expired"
auth_response = (
    "Please login in again or sign up an account to access this resource"
)

wrong_status = (
    "Status must either be 'resolved','under investigation' or 'rejected'"
)
delete_not_allowed = "You are not allowed to delete this resource"

URL_SIGNUP = 'api/v1/auth/login'
URL_LOGIN = 'api/v1/auth/login'
