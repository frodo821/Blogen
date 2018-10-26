#pylint: disable=C0326, R0903, C0111, W0201
from re import search, MULTILINE

from markdown.treeprocessors import Treeprocessor

code_block = r"```(?:[^`]|`(?!``))*```"

def preprocess(src, prefix):
    codes = []
    m = search(code_block, src, MULTILINE)
    ss = 0
    while m:
        mstr = m.group(0)
        if "\n" not in mstr:
            continue
        lang = mstr.split('\n', 1)[0][3:]
        codes.append(lang.lower())
        code = mstr.replace(lang, "", 1).replace('_', '&#x5f;')
        pre = src[:m.start(0) + ss] + code
        src = pre + src[m.end(0) + ss:]
        ss = len(pre)
        m = search(code_block, src[ss:], MULTILINE)
    return src, CodeTreeprocessor(prefix).setPreprocessor(codes)

class CodeTreeprocessor(Treeprocessor):
    """Syntax Highlight Processor"""
    def __init__(self, prefix: str):
        super().__init__()
        self.prefix = prefix

    def setPreprocessor(self, preprop):
        self.codes = preprop
        return self

    def run(self, root):
        i = 0
        for e in root.getiterator(tag='code'):
            if "\n" not in e.text:
                continue
            e.set("class", self.prefix + self.codes[i])
            i += 1
