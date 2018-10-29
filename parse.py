#pylint: disable=C0326, R0903, C0111, W0603

from os import makedirs
from os.path import basename, dirname, exists, splitext

from re import search, sub MULTILINE, DOTALL
from markdown import Markdown as md

from .article import Article, addArticle
from .modules import preprocess

TITLE       = r"<!--title:((?:[^-]|-(?!->))*)-->"
DESCRIPTION = r"<!--description:((?:[^-]|-(?!->))*)-->"
TAGS        = r"<!--tags:((?:[^-]|-(?!->))*)-->"
WRITTEN     = r"<!--date:((?:[^-]|-(?!->))*)-->"

class DummyMatch:
    """dummy matching class"""
    def __init__(self, dummy):
        self.dummy = dummy

    def group(self, *_):
        """dummy search group"""
        return self.dummy

def parseMarkdown(
        path,
        outPath,
        articlesJsonPath,
        template,
        outpath=None,
        code_highlight=True,
        language_prefix="language-"):
    """parse markdown into html"""
    with open(path, encoding="utf-8") as f:
        src = f.read()

    title = (search(TITLE, src) or DummyMatch("タイトルなし")).group(1)
    description = (search(DESCRIPTION, src, MULTILINE | DOTALL) or DummyMatch("")).group(1)
    tags = (search(TAGS, src) or DummyMatch("")).group(1).split(',')
    date = (search(WRITTEN, src) or DummyMatch("")).group(1)
    src = sub(r"<!--(?:[^-]|-(?!->))*-->", "", src)
    addArticle(
        articlesJsonPath,
        Article(title, description, tags, date),
        outpath or splitext(basename(path))[0])
    if not exists(dirname(outPath)):
        makedirs(dirname(outPath))

    proc = md(output_format="html5", extensions=["fenced_code"])
    if code_highlight:
        src, tree = preprocess(src, language_prefix)
        proc.treeprocessors['syntax_highlighter'] = tree

    with open(outPath, 'w', encoding="utf-8") as f:
        f.write(template.format(
            title=title,
            article=proc.convert(src)))
