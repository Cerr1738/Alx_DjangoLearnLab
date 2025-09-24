from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# Expected Output:
# <Book: 1984 by George Orwell>


from bookshelf.models import Book
books = Book.objects.all()
books
# Expected Output:
# <QuerySet [<Book: 1984 by George Orwell>]>

for b in books:
    print(b.title, b.author, b.publication_year)
# Expected Output:
# 1984 George Orwell 1949


book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# Expected Output:
# <Book: Nineteen Eighty-Four by George Orwell>


book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Expected Output:
# (1, {'bookshelf.Book': 1})

Book.objects.all()
# Expected Output:
# <QuerySet []>
