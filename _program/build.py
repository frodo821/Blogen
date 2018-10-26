"""Project command"""
#pylint: disable=W0122

from os import getcwd
from os.path import exists, join, dirname, basename, splitext
from glob import iglob
from .command import Command, UnsatisfiableArgumentError, CommandError
from ..parse import parseMarkdown

DEFAULT_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        {article}
    </body>
</html>
"""

class BuildCommand(Command):
    """This command is to build a project."""
    def __init__(self):
        super().__init__("build")

    @property
    def summaries(self):
        yield "This command is used for building a project."
        yield "This command has no additional arguments."

    def main(self, args):
        if args:
            raise UnsatisfiableArgumentError(self.__name__, len(args), 0)
        if not exists(join(getcwd(), "config.py")):
            raise CommandError(self.__name__, "current directory is not a project directory.")
        with open(join(getcwd(), "config.py"), encoding="utf-8") as f:
            cond = {}
            try:
                exec(f.read(), globals(), cond)
            except Exception as e:
                raise CommandError(
                    self.__name__,
                    (f"Config parse failed at line {e.__traceback__.tb_lineno}."
                     f"(Reason: {e})")) from e
        out_dir = join(getcwd(), cond.get("OUTPUT_DIR", "output"))
        out_type = cond.get("OUTPUT_TYPE", "directory")
        article_indices = join(getcwd(), cond.get("ARTICLES_JSON", "articles.json"))
        template_path = join(getcwd(), cond.get("TEMPLATE_HTML", "template.html"))
        code_highlight = cond.get("ENABLE_SYNTAX_HIGHLIGHT", True)
        language_prefix = cond.get("CSS_CLASS_LANGUAGE_PREFIX", "language-")

        if not exists(template_path):
            print("template not found, using default template.")
            template = DEFAULT_TEMPLATE
        else:
            with open(template_path, encoding="utf-8") as f:
                template = f.read()

        for source in iglob(join(getcwd(), "src", "**", "*.md"), recursive=True):
            if out_type == "directory":
                out = join(
                    dirname(source.replace(join(getcwd(), "src"), out_dir)),
                    splitext(basename(source))[0],
                    "index.html")
            elif out_type == "html":
                out = join(
                    dirname(source.replace(join(getcwd(), "src"), out_dir)),
                    splitext(basename(source))[0] + ".html")
            try:
                parseMarkdown(
                    source, out,
                    article_indices,
                    template,
                    code_highlight,
                    language_prefix)
            except Exception as e:
                raise CommandError(self.__name__, f"parsing failed: {e} in {source}")
