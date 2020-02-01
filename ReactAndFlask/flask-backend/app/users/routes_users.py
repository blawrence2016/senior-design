# TODO: Make populate endpoint to populate the table upon sign in
# TODO: Test format of json token exchange - might get messed up as byte string


from app.dal.user_table import UserTable
from app.data_models.user import User
from app.decorators.auth import requires_auth, requires_role
from app.users.authentication import AuthManager
from app.users.validator import Validator
from flask import Blueprint, request

users = Blueprint(
    "users", __name__, template_folder="templates", static_folder="static"
)

AUTH_MANAGER = AuthManager()
VALIDATOR = Validator()
USER_TABLE = UserTable()


@users.route("/users/test", methods=["GET"])
@requires_auth(request)
def test():
    """ route to test user endpoints """

    json = {}

    # is_authenticated, message = AUTH_MANAGER.validate_auth_token(request.headers)
    # if not is_authenticated:
    #     return add_message_to_JSON(json, message)

    return add_message_to_JSON(json, "hello")


@users.route("/users/search", methods=["POST"])
@requires_auth(request)
@requires_role(request, "admin")
def search():

    request_data = request.get_json()
    username = request_data["username"]
    user = USER_TABLE.get_user(username)

    return user.make_json()


@users.route("/users/create", methods=["POST"])
# @requires_auth(request)
# @requires_role(request, "admin")
def create():
    """Route for creating users

    Username Criteria:
    - Between 4 and 20 characters
    - Contains only alphanumeric characters and ".", "_"
    - No "." or "_" at the beginning
    - No doubles of special characters (".." or "__")
    - Not already taken by another user

    Email Criteria:
    - Valid email address compliant with RCF 5322 standard
    - Not already associated with another account

    Password Criteria:
    - Contains at least one number.
    - Contains at least one uppercase and one lowercase character.
    - Contains at least one special symbol.
    - Between 8 to 20 characters long.


    Returns:
        string: Success or failure, if failure provide message
    """

    json = {}

    # print(request)
    request_data = request.get_json()
    # print(request_data)
    try:
        username = request_data["username"]
        password = request_data["password"]
        email = request_data["email"]
        display_name = request_data["displayName"]
        privilege = request_data["privilege"]
    except:
        return add_message_to_JSON(
            json, "Incorrectly formatted message. Application error on the frontend"
        )

    if not VALIDATOR.validate_username(username):
        return add_message_to_JSON(json, "Invalid username")

    if not VALIDATOR.validate_email(email):
        return add_message_to_JSON(json, "Invalid email address")

    if not VALIDATOR.validate_password(password):
        return add_message_to_JSON(json, "Password too weak")

    try:
        encrypted_password = AUTH_MANAGER.encrypt_pw(password)

        user = User(username, display_name, email, encrypted_password, privilege)
        USER_TABLE.add_user(user)
    except:
        return add_message_to_JSON(json, "Server error. Please try again later...")

    return add_message_to_JSON(json, "success")


@users.route("/users/delete", methods=["POST"])
@requires_auth(request)
@requires_role(request, "admin")
def delete():
    """Route for deleting users

    Returns:
        string: Success or failure, if failure provide message
    """

    json = {}

    request_data = request.get_json()
    username = request_data["username"]

    user = USER_TABLE.get_user(username)
    if user is None:
        return add_message_to_JSON(json, "User {username} does not exist")

    USER_TABLE.delete_user(user)

    return add_message_to_JSON(json, "success")


@users.route("/users/edit", methods=["POST"])
@requires_auth(request)
@requires_role(request, "admin")
def edit():

    json = {}

    request_data = request.get_json()
    username = request_data["username"]
    display_name = request_data["display_name"]
    email = request_data["email"]
    password = request_data["password"]
    privilege = request_data["privilege"]

    user = USER_TABLE.get_user(username)
    if user is None:
        return add_message_to_JSON(json, "User {username} does not exist")

    updated_user = User(
        username=username,
        display_name=display_name,
        email=email,
        password=password,
        privilege=privilege,
    )
    USER_TABLE.delete_user(user)
    USER_TABLE.add_user(updated_user)

    return add_message_to_JSON(json, "success")


@users.route("/users/authenticate", methods=["POST"])
def authenticate():
    """ Route for authenticating users """

    json = {}

    print(request)
    try:
        request_data = request.get_json()
        username = request_data["username"]
        attempted_password = request_data["password"]
    except:
        return add_message_to_JSON(json, "Connection error. Please try again later...")

    user = USER_TABLE.get_user(username)
    if user is None:
        return add_message_to_JSON(json, "Username does not exist")

    auth_success = AUTH_MANAGER.compare_pw(attempted_password, user.get_password())
    if not auth_success:
        return add_message_to_JSON(json, "Incorrect password")

    json["token"] = AUTH_MANAGER.encode_auth_token(username)
    json["privilege"] = user.privilege
    json["message"] = "success"

    return json


def add_message_to_JSON(json, message) -> dict:
    json["message"] = message

    return json
