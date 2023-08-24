"""Этот скрипт содержит функции для очистки экрана и рендеринга шаблонов с использованием Jinja2.

Функция `screen_cleaner` принимает флаг `flag`, который определяет, нужно ли очистить экран.
В зависимости от операционной системы, функция использует команду 'cls' для Windows и 'clear' для других систем.

Функция `render_template` принимает контекст (словарь с данными для шаблона), имя шаблона и флаг `cls` для очистки экрана.
Если контекст не указан, то используется пустой словарь.
Функция загружает указанный шаблон с помощью `env.get_template` из пакета шаблонов и рендерит его,
передавая контекст как параметры. Затем рендеренный шаблон выводится на экран с помощью `print`. Если флаг `cls` равен True,
то экран очищается перед выводом шаблона.

В целом, данный скрипт предназначен для удобного и красивого вывода шаблонов на экран с помощью Jinja2."""

import os
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader(__name__, 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def screen_cleaner(flag):
    if flag:
        os.system('cls' if os.name == 'nt' else 'clear')


def render_template(context=None, template="default.jinja2", cls=True):
    """Prints rendered template with context data

    Args:
        context (dict, optional): [data for rendering template]. Defaults to None.
        template (str, optional): [template filename]. Defaults to "default.jinja2".
        cls (bool, optional): [Clear screen flas. Shows if screan should be 
        cleaned before showing this view]. Defaults to True.
    """
    if not context:
        context = {}
    screen_cleaner(cls)
    template = env.get_template(template)
    print(template.render(**context))
