import logging

from .Mongo.mongo_manager import MongoManager

log = logging.getLogger(__name__)


class UserManager:

    def __init__(self):
        self.users_collection = MongoManager().users_collection

    def check_if_user_exist_in_db(self, user_email: str, user_password: str) -> dict | None:
        """
        Check if user exist in User collection in database.

        :param user_email: User email to check
        :param user_password: User password to check

        :return: User data if user exist in database
        """
        user = self.users_collection.find_one({'email': user_email, 'password': user_password})

        if user:
            log.info("User exist in Users Collection.")
            return user

        log.warning("Can't find registered user in database.")
        return None

    def register_user(self, new_login: str, new_email: str, new_password: str, new_pesel: int) -> bool:
        """
        Adding user to database if given record does not exist.

        :param new_login: New login
        :param new_email: New email
        :param new_password: New password
        :param new_pesel: New pesel
        :return: If the user did not exist, it adds him and returns True, if he already exists, skip and returns False.
        """
        existing_user_login = self.users_collection.find_one({'login': new_login})
        existing_user_email = self.users_collection.find_one({'email': new_email})
        existing_user_pesel = self.users_collection.find_one({'pesel': new_pesel})

        if not existing_user_login and not existing_user_email or not existing_user_pesel:
            found_results = [doc for doc in self.users_collection.find().sort('_id', -1)]
            if len(found_results) > 0:
                user_id = found_results[0]['_id'] + 1
            else:
                user_id = 1
            new_user = {
                '_id': user_id,
                'login': new_login,
                'email': new_email,
                'password': new_password,
                'pesel': new_pesel,
            }
            self.users_collection.insert_one(new_user)
            log.warning("Registered new user and added to database!")
            return True

        log.warning("User exist. Can't register new user and add to database.")
        return False
