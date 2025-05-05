import pytest
from main import BooksCollector
from data import test_books, test_books_genre
from helpers import get_key_from_dict, get_value_from_dict

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # Проверка получения списка книг в т.ч. пустого. Возвращает книги из списка
    def test_get_books_genre_all_book(self, collector_w_books):
        assert len(collector_w_books.get_books_genre()) > 0

    # Проверка добавления книг в новую коллекцию
    @pytest.mark.parametrize(
            'book_names, result',
            [
                ([], 0),
                (get_key_from_dict(test_books), len(test_books)),
                ([get_key_from_dict(test_books, 0),get_key_from_dict(test_books, 0)],1)
            ],
            ids=[
                'Collector w/o books => (0)',
                f'Add a few books => ({len(test_books)})',
                'Add the same book in collection is impossible'
            ]
    )
    def test_add_new_book_add_two_books(self, book_names, result):
        book_collector = BooksCollector()
        i = 0
        while i < result:
            book_collector.add_new_book(get_key_from_dict(test_books,i))
            i +=1
        assert len(book_collector.get_books_genre()) == result

    # Проверка получения жанра по имени книги из коллекции
    def test_get_book_genre_for_book_in_collection (self, collector_w_books):
        book_genre_in_collector = collector_w_books.get_book_genre(get_key_from_dict(test_books)[0])
        book_genre_orig = get_value_from_dict(test_books, 0)
        assert book_genre_in_collector == book_genre_orig

    # После добавления в коллекцию жанр не установлен
    def test_add_new_book_without_genre (self):
        book_collector = BooksCollector()
        book_name = get_key_from_dict(test_books, 0)
        book_collector.add_new_book(book_name)
        genre_name = book_collector.get_book_genre(book_name)
        assert genre_name == ''

    # Смена жанра для книги
    @pytest.mark.parametrize(
            'book_name, new_book_genre, result',
            [
                (
                    get_key_from_dict(test_books, 0), 
                    'test_book_invalid_genre',
                    get_value_from_dict(test_books, 0)
                ),
                (
                    get_key_from_dict(test_books, 0),
                    test_books_genre[0], 
                    test_books_genre[0]
                ),
                (
                    get_key_from_dict(test_books, 0),
                    get_value_from_dict(test_books, 0),
                    get_value_from_dict(test_books, 0)
                )
            ],
            ids= [
                'Change to incorrect genre is impossible',
                'Change current genre to another',
                'Change current genre to current'

            ]
    )
    def test_set_book_genre_for_book (self, book_name, new_book_genre, result, collector_w_books):
        collector_w_books.set_book_genre(book_name, new_book_genre)
        new_genre = collector_w_books.get_book_genre(book_name)
        assert new_genre == result

    # выводим список книг с определённым жанром
    @pytest.mark.parametrize(
            'genre, result',
            [
                (get_value_from_dict(test_books, 2), 2),
                ('test_book_invalid_genre', 0)
            ],
            ids= [
                f'Books with correct genre',
                'Books with unknown genre'
            ]
    )
    def test_get_books_with_specific_genre(self, genre, result, collector_w_books):
        lst = collector_w_books.get_books_with_specific_genre(genre)
        assert len(lst) == result

    # возвращаем книги, подходящие детям
    def test_get_books_for_children_return_books_only_for_children(self, collector_w_books):
        children_books = collector_w_books.get_books_for_children()
        full_book_list = get_key_from_dict(collector_w_books.get_books_genre())
        assert set(children_books) < set(full_book_list)

    # получаем список Избранных книг
    def test_get_list_of_favorites_books(self, collector_w_books):
        cnt_fvr_books = len(collector_w_books.get_list_of_favorites_books())
        assert 1 == cnt_fvr_books

    # добавляем книгу в Избранное
    @pytest.mark.parametrize(
            'book_name, result',
            [
                (get_key_from_dict(test_books, 1), 2),
                ('test_incorrect_name_book', 1),
                (get_key_from_dict(test_books, 0), 1)
            ],
            ids= [
                'Add not favorite book to favorites',
                'Add unknown book to favorites is impossible',
                'Add the same book to favorite twice is impossible'
            ]
    )
    def test_add_book_in_favorites (self, book_name, result, collector_w_books):
        collector_w_books.add_book_in_favorites(book_name)
        cnt_fvr_books = len(collector_w_books.get_list_of_favorites_books())
        assert result == cnt_fvr_books

    # удаляем книгу из Избранного
    @pytest.mark.parametrize(
            'book_name, result',
            [
                (get_key_from_dict(test_books, 0), 0),
                ('test_incorrect_name_book', 1),
                (get_key_from_dict(test_books, 1), 1)
            ],
            ids= [
                'Del book from favorites',
                'Del unknown book from favorites is impossible',
                'Del book in collection but not in favorites from favorite is impossible'
            ]
    )
    def test_delete_book_from_favorites(self, book_name, result, collector_w_books):
        collector_w_books.delete_book_from_favorites(book_name)
        cnt_fvr_books = len(collector_w_books.get_list_of_favorites_books())
        assert result == cnt_fvr_books
