import configparser
from datetime import datetime
import pymongo
import logging

from ..book import Book

log = logging.getLogger(__name__)


class MongoManager:
    """
    Class to connect with mongo database and handle all operations related to.
    """
    def __init__(self, config_path='./config.ini'):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_path)
        self.client = pymongo.MongoClient(self.cfg.get('mongo', 'host'),
                                          self.cfg.getint('mongo', 'port'),
                                          username=self.cfg.get('mongo', 'username'),
                                          password=self.cfg.get('mongo', 'password'))
        self.db = self.client['eLibrary']

    def get_all_books(self) -> list:
        """
        Get all book records from Books collection in MongoDB and for each create Book object with proper data.

        :return: Book objects
        """
        book_objects = []

        books_data = self.book_collection.find({})

        for book in books_data:
            book = Book(book['_id'], book['name'], book['img_name'])
            book_objects.append(book)

        return book_objects

    def add_book(self, book_name: str, book_img_name: str) -> bool:
        """
        Add book to Book collection if given book does not exist in MongoDB.

        :param book_name: New book name
        :param book_img_name: New book img name

        :return: True if book does not exist in database, and False if exist
        """
        try:
            highest_book_id = [book for book in self.book_collection.find().sort('_id', -1)]

            new_book = {
                '_id': highest_book_id[0]['_id'] + 1,
                'name': book_name,
                'img_name': book_img_name
            }
        except IndexError:
            new_book = {
                '_id': 1,
                'name': book_name,
                'img_name': book_img_name
            }

        found_book_by_img_name = self.book_collection.find_one({'img_name': book_img_name, 'name': book_name}) is None

        if found_book_by_img_name:
            self.book_collection.insert_one(new_book)
            log.info(f"Book added successfully!")
            return True

        log.error(f"Book exist in database! Skipping.")
        return False

    def remove_book(self, _id: int) -> bool:
        """
        Delete book from Book collection in MongoDB.
        :param _id: Unique book ID

        :return: True if book was removed successfully, False if not.
        """
        result = self.book_collection.delete_one({'_id': _id})

        if result.deleted_count == 1:
            log.info(f"Book with _id: {_id} deleted successfully.")
            return True

        log.error(f"Can't delete book with _id: {_id}. Book not found!")
        return False

    def edit_book(self, _id: int, new_data: dict) -> bool:
        """
        Edit data for selected book in Book collection.

        :param _id: Unique book ID
        :param new_data: New data set to change in selected book
        :return:
        """
        result = self.book_collection.update_one(
            {'_id': _id},
            {'$set': new_data}
        )

        if result.modified_count == 1:
            log.info(f"Book with ID {_id} updated successfully")
            return True

        log.error(f"Book with ID {_id} not found")
        return False

    def add_user_operation(self, user: str, operation: str, timestamp: datetime.timestamp) -> None:
        """
        Add new user operation to UsersOperations collection from MongoDB.

        :param user: The user who performed the operation
        :param operation: New operation
        :param timestamp: Timestamp of this operation
        """
        new_operation = {
            'user': user,
            'operation': operation,
            'timestamp': datetime.fromtimestamp(timestamp)
        }
        self.db['UsersOperations'].insert_one(new_operation)

    def get_all_users_operations(self) -> list:
        """
        Get all operations from UsersOperations collection from MongoDB.

        :return: Users dicts operations
        """
        all_operations = []
        db_operations = self.users_operations.find({})

        for operation in db_operations:
            operation_dict = {
                'user': operation['user'],
                'operation': operation['operation'],
                'timestamp': operation['timestamp']
            }
            all_operations.append(operation_dict)

        return all_operations

    @property
    def users_collection(self):
        return self.db['Users']

    @property
    def book_collection(self):
        return self.db['Books']

    @property
    def users_operations(self):
        return self.db['UsersOperations']
