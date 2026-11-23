from text_factory import TextFactory
from text_system import Text, Container, Leaf, Paragraph, Heading

doc = TextFactory("Стаття")

doc.add_paragraph("Анотація")

doc.add_heading("Вступ")
doc.add_paragraph("Перший абзац")
doc.add_paragraph("Другий абзац")
doc.add_link("Подібні статті", "https://example.com/similar")
doc.up()

doc.add_heading("Основний матеріал")
doc.add_heading("Опис методу")
doc.add_math("E = mc^2")
doc.up()
doc.add_heading("Хід експерименту")
doc.add_paragraph("Крок за кроком")
doc.up()
doc.add_heading("Аналіз результатів")
doc.add_image("Графік тренду", "trend.png")
doc.add_table([["Метрика", "Значення"], ["accuracy", 0.93], ["loss", 0.12]])
doc.up()
doc.up()

doc.add_heading("Висновки")
doc.add_paragraph("Метод працює")
doc.up()

doc.add_heading("Використані джерела")
doc.add_link("Джерело 1", "https://example.com/1")
doc.add_link("Джерело 2", "https://example.com/2")

print(doc)
print("\n--- toc ---")
print(doc.toc())

print("\n--- polymorphism ---")
h = Heading("x")
h.add_child(Paragraph("y"))
for node in (h, h.children[0]):
    print(type(node).__name__, isinstance(node, Text), isinstance(node, Container), isinstance(node, Leaf))

try:
    Text()
except TypeError as e:
    print("abstract:", e)
