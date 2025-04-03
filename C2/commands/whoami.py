from C2.func.utils.logger import log
from C2.func.utils.database import DBController

def do_whoami(self, inp):

    """Tells you informations about your session."""

    db = DBController()
    user_id = db.get_id_by_username(self.username)
    if user_id:
        user = db.get_username_by_id(user_id[0])
        if user:
            log(self, f"Username: {user[1]}\n", "generic")
            log(self, f"Rank: {user[3]}\n", "generic")
            log(self, f"User ID: {user[0]}\n", "generic")
    db.close()