class Book:
    def __init__(self, title, author, publisher, date):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.date = date
        self.stock = 0

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nPublisher: {self.publisher}\nDate: {self.date}"
