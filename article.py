#pylint: disable=E0202, C0111, R0903

from os.path import exists
from json import dump, load
from json import JSONEncoder as encoder

class Article:
    def __init__(self, title, description, tags, date):
        self.title = title
        self.description = description
        self.tags = tags
        self.date = date
    def __str__(self):
        return f"Article <{self.title}>"
    def __repr__(self):
        return str(self)
    def __iter__(self):
        yield "title", self.title
        yield "description", self.description
        yield "tags", self.tags
        yield "date", self.date

class ArticlesEncoder(encoder):
    def default(self, o):
        if isinstance(o, Article):
            return dict(o)
        return super().default(o)

def addArticle(path, article, article_file):
    data = {}
    if exists(path):
        with open(path) as f:
            data = load(f)
    data[article_file] = article
    with open(path, 'w') as f:
        dump(data, f, cls=ArticlesEncoder)
