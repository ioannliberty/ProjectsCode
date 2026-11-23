from abc import ABC, abstractmethod


class Text(ABC):
    def __init__(self):
        self.parent = None

    @abstractmethod
    def render(self):
        pass

    def depth(self):
        d = 0
        node = self.parent
        while node is not None:
            d += 1
            node = node.parent
        return d


class Container(Text):
    def __init__(self, title):
        super().__init__()
        self._title = str(title)
        self._children = []

    @property
    def title(self):
        return self._title

    @property
    def children(self):
        return list(self._children)

    def add_child(self, child):
        if not isinstance(child, Text):
            raise TypeError("child must be a Text")
        child.parent = self
        self._children.append(child)

    def remove_child(self, idx):
        if 0 <= idx < len(self._children):
            self._children.pop(idx).parent = None

    def move_child(self, old_idx, new_idx):
        if 0 <= old_idx < len(self._children):
            el = self._children.pop(old_idx)
            new_idx = max(0, min(new_idx, len(self._children)))
            self._children.insert(new_idx, el)

    def render_children(self):
        return "\n\n".join(c.render() for c in self._children)

    def render_toc(self):
        lines = []
        for c in self._children:
            if isinstance(c, Heading):
                lines.append("  " * (c.level - 1) + "- " + c.title)
            if isinstance(c, Container):
                sub = c.render_toc()
                if sub:
                    lines.append(sub)
        return "\n".join(lines)

    @abstractmethod
    def render(self):
        pass


class Leaf(Text):
    def __init__(self, content):
        super().__init__()
        self._content = content

    @property
    def content(self):
        return self._content

    @abstractmethod
    def render(self):
        pass


class Root(Container):
    def render(self):
        return f"Title: {self._title}\n\n{self.render_children()}".strip()


class Heading(Container):
    def __init__(self, title, level=1):
        super().__init__(title)
        # markdown has only 6 levels
        self.level = max(1, min(level, 6))

    def render(self):
        head = "#" * self.level + " " + self._title
        return f"{head}\n\n{self.render_children()}".strip()


class Paragraph(Leaf):
    def render(self):
        return self._content or ""


class Link(Leaf):
    def __init__(self, content, url):
        super().__init__(content)
        self._url = url

    def render(self):
        return f"[{self._content}]({self._url})"


class Math(Leaf):
    def render(self):
        return f"$$ {self._content} $$"


class Image(Leaf):
    def __init__(self, content, src):
        super().__init__(content)
        self._src = src

    def render(self):
        return f"![{self._content}]({self._src})"


class Table(Leaf):
    # content is a list of rows, first row is the header
    def render(self):
        if not self._content:
            return ""
        head, *rows = self._content
        lines = ["| " + " | ".join(map(str, head)) + " |"]
        lines.append("|" + "---|" * len(head))
        for r in rows:
            lines.append("| " + " | ".join(map(str, r)) + " |")
        return "\n".join(lines)
