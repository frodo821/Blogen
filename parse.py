#pylint: disable=C0326, R0903, C0111, W0603

from os import makedirs
from os.path import basename, dirname, exists, splitext

from collections import deque
from re import search, sub, match, MULTILINE, DOTALL

from markdown import Markdown as md
from markdown.blockparser import BlockParser
import markdown.blockprocessors as procs

from .article import Article, addArticle
from .modules import preprocess

TITLE       = r"<!--title:((?:[^-]|-(?!->))*)-->"
DESCRIPTION = r"<!--description:((?:[^-]|-(?!->))*)-->"
TAGS        = r"<!--tags:((?:[^-]|-(?!->))*)-->"
WRITTEN     = r"<!--date:((?:[^-]|-(?!->))*)-->"

INITIALIZED = False

def chunkSplit(src):
    HTML_BLOCK_START = r"<[^/>][^>]*>$"
    HTML_BLOCK_END   = r"^.+</[^>]*>$"
    CODE_BLOCK_SEPT  = r"^.*```\Z"

    ret  = []
    temp = ""
    state = deque([""])
    skips = 0

    for i, c in enumerate(src):
        if skips > 0:
            skips -= 1
            continue

        if c == "\n" and state[-1] == "":
            v = 1
            while True:
                if i + v >= len(src):
                    v = 2
                    break
                if src[i+v] != "\n":
                    break
                v += 1
            if v > 1:
                ret.append(temp)
                temp = ""
                continue

        temp += c

        if match(HTML_BLOCK_END, temp, MULTILINE | DOTALL) and state[-1] != "CODE":
            state.pop()
            if state[-1] != "HTML":
                ret.append(temp)
                temp = ""
                continue

        if match(HTML_BLOCK_START, temp, MULTILINE | DOTALL) and state[-1] != "CODE":
            state.append("HTML")
            continue

        if match(CODE_BLOCK_SEPT, temp, MULTILINE | DOTALL):
            if state[-1] == "CODE":
                state.pop()
                if state[-1] == "":
                    ret.append(temp)
                    temp = ""
                    continue
            else:
                state.append("CODE")

    if temp:
        ret.append(temp)
    return ret

class FixedBlockParser(BlockParser):
    def parseChunk(self, parent, text):
        self.parseBlocks(parent, chunkSplit(text))

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
    global INITIALIZED

    if not INITIALIZED:
        procs.BlockParser = FixedBlockParser
        INITIALIZED = True

    with open(path, encoding="utf-8") as f:
        src = f.read()

    title = (search(TITLE, src) or DummyMatch("タイトルなし")).group(1)
    description = (search(DESCRIPTION, src) or DummyMatch("")).group(1)
    tags = (search(TAGS, src) or DummyMatch("")).group(1).split(',')
    date = (search(WRITTEN, src) or DummyMatch("")).group(1)
    src = sub(r"<!--(?:[^-]|-(?!->))*-->", "", src)
    addArticle(
        articlesJsonPath,
        Article(title, description, tags, date),
        outpath or splitext(basename(path))[0])
    if not exists(dirname(outPath)):
        makedirs(dirname(outPath))

    proc = md(output_format="html5")
    if code_highlight:
        src, tree = preprocess(src, language_prefix)
        proc.treeprocessors['syntax_highlighter'] = tree

    with open(outPath, 'w', encoding="utf-8") as f:
        f.write(template.format(
            title=title,
            article=proc.convert(src)))
