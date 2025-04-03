from C2.func.utils.database import DBController
import base64

def login(username, password):
    db = DBController()
    user = db.get_id_by_username(username)
    if user:
        user_id = user[0]
        stored_user = db.get_username_by_id(user_id)
        encoded_password = base64.b64encode(password.encode()).decode()
        if stored_user and stored_user[2] == encoded_password:
            return True
    return False