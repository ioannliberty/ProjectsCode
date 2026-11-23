from text_system import Root, Heading, Paragraph, Link, Math, Image, Table


class TextFactory:
    def __init__(self, title):
        self._root = Root(title)
        self._current = self._root

    def add_heading(self, title, level=None):
        # by default level follows how deep we are
        if level is None:
            level = self._current.depth() + 1
        heading = Heading(title, level)
        self._current.add_child(heading)
        self._current = heading
        return self

    def add_paragraph(self, content):
        self._current.add_child(Paragraph(content))
        return self

    def add_link(self, content, url):
        self._current.add_child(Link(content, url))
        return self

    def add_math(self, formula):
        self._current.add_child(Math(formula))
        return self

    def add_image(self, alt, src):
        self._current.add_child(Image(alt, src))
        return self

    def add_table(self, rows):
        self._current.add_child(Table(rows))
        return self

    def up(self):
        if self._current.parent is None:
            print("you are already in root")
        else:
            self._current = self._current.parent
        return self

    def toc(self):
        return self._root.render_toc()

    def __str__(self):
        return self._root.render()
