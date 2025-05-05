import helpers
import pytest
from main import BooksCollector
from data import test_books

@pytest.fixture(scope='function')
def collector_w_books():
    book_collector = BooksCollector()
    book_collector.books_genre = test_books
    book_collector.favorites = [helpers.get_key_from_dict(test_books, 0)]
    return book_collector