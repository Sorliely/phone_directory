from views import render_template

from models import *


def default_controller(data=None, cls=True):
    """Функция ожидает ввод пользователя и возвращает введенные данные вместе с None в кортеже."""
    render_template(context={}, template="default.jinja2", cls=cls)
    return (input(), None)


def exit_controller(data=None, cls=True):
    """Выполняет выход"""
    render_template(context={}, template="exit.jinja2", cls=cls)
    exit()


def all_users_controller(data=None, cls=True):
    """Функция `all_users_controller` является контроллером (компонентом управления) для отображения всех пользователей.
    Его основная цель - получить список пользователей из базы данных (в данном случае с использованием метода `User.all()`),
    передать этот список в шаблон `all_users.jinja2` и вызвать функцию отображения шаблона."""
    users = User.all()
    render_template(context={'users': users}, template="all_users.jinja2", cls=cls)
    input("Продолжить?")
    return 'main', None  # (next state, data)


def add_user_controller(data=None, cls=True):
    """Добовляет новое имя пользователя"""
    render_template(context={}, template="add_user.jinja2", cls=cls)
    username = input()
    user = User.add(username)
    return 2, user  # (next state, data)


def add_surname_controller(user, cls=True):
    """Добовляет фамилию"""
    render_template(context={}, template="surname.jinja2", cls=cls)
    surname = input()
    add_surname = Surname.add(surname, user)
    return 3, user  # (next state, data)


def add_fathers_name(user, cls=True):
    """Добовляет отчество"""
    render_template(context={}, template="fathers_name.jinja2", cls=cls)
    fname = input()
    add_fathers_name = NameOrganization.add(fname, user)
    return 21, user


def add_name_organization(user, cls=True):
    """Добаляет название организации"""
    render_template(context={}, template="add_organization.jinja2", cls=cls)
    name = input()
    add_name = NameOrganization.add(name, user)
    return 51, user


def add_phone_controller(user, cls=True):
    """Добовляет номер телефона пользователя"""
    render_template(context={}, template="add_phone.jinja2", cls=cls)
    phone_number = input()
    phone = Phone.add(phone_number, user)
    return 212, user  # (next state, data)


def add_more_controller(user, cls=True):
    """Проверяет нужно ли добавить еще один номер телефона (если есть)
    если нужно добавить возвращает функцию add_phone_controller, если нет функция прекращает работу"""
    render_template(context={}, template="add_more.jinja2", cls=cls)
    answer = input()
    if answer == 'Y':
        return 21, user
    return 222, user  # (next state, data)


def search_controller(user, cls=True):
    """Ищет пользователя по номеру"""
    render_template(context={}, template="search.jinja2", cls=cls)
    query = input()
    phone = session.query(Phone).join(User).filter(Phone.phone == query).first()
    if phone:
        print("Телефон:", phone.phone)
        print("Имя:", phone.user.name)
        print("Фамилия:", phone.user.surname[0])
        print("Отчество:", phone.user.fathername)
        print("Организация:", phone.user.organizations[0])

    else:
        print("Телефон не найден.")



def delete_controller():
    """удаляет пользователя из бд"""
    print("удалил")


def get_controller(state):
    """Функция get_controller(state) возвращает контроллер, ассоциированный с заданным состоянием state.
    Если в словаре controllers_dict найден контроллер для данного состояния, то он возвращается.
    Если в словаре нет контроллера для данного состояния, то возвращается контроллер default_controller."""
    return controllers_dict.get(state, default_controller)


controllers_dict = {  # use dict type instead of if else chain
    '0': exit_controller,
    '1': all_users_controller,
    '2': add_user_controller,
    '3': delete_controller,
    '4': search_controller,
    2: add_surname_controller,
    3: add_fathers_name,
    21: add_phone_controller,  # user can't enter 21 of int type
    212: add_more_controller,
    222: add_name_organization,

}
