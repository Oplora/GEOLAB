

class Book:
    page = 0
    authors = ['']

if __name__ == '__main__':
    books = [Book(), Book(), Book()]
    books[0].page = 100
    books[0].authors = ['A1', 'A2']
    books[1].page = 120
    books[1].authors = ['A3', 'A1']
    books[2].page = 10
    books[2].authors = ['A2', 'A3']

    books = sorted(books, key=lambda x: x.authors[1] )

    for i in books:
        print(i.authors)