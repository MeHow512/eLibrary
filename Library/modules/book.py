class Book:
    """
    Class for Book objects to easily manage store Book fields for each book.
    """
    def __init__(self, book_id: int, book_name: str, book_img_name: str):
        self.book_id = book_id
        self.book_name = book_name
        self.book_img_name = book_img_name
