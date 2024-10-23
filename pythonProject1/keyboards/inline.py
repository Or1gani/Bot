from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

from utils.db_data import get_region_list, get_tickets, get_name_by_tg_id
from aiogram.filters.callback_data import CallbackData
from assets.menu_data import desciption_for_pages_settings as dfps

class region_callback(CallbackData, prefix="region"):
    level: int
    menu_name: str # | None = None
    yes: str | None = None

class name_callback(CallbackData, prefix="name"):
    name: str


class add_employee_callback(CallbackData, prefix="employee"):
    level: int
    menu_name: str
    data_for_db: str | None = None
    yes: int | None = None


class edit_employee_callback(CallbackData, prefix="edit"):
    menu_name: str | None = None
    value: str | None = None
    decide: str | None = None
    take: str |None = None
def get_callback_buttons(
        *,
        buttons: dict[str, str],
        sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

def get_profile_button(*, level: int, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text="Смена района",
         callback_data=region_callback(level=level+1, menu_name="region", yes="False").pack()
    ))
    return keyboard.adjust(*sizes).as_markup()

def get_region_buttons(*, level: int, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    regions = get_region_list()
    keyboard.add(InlineKeyboardButton(
        text='Назад',
         callback_data=region_callback(level=0, menu_name="main", yes="False").pack()
    ))
    for region_id, region_name in regions.items():
        keyboard.add(InlineKeyboardButton(
            text=region_name,
            callback_data=region_callback(level=level+1, menu_name=str(region_id), yes="True").pack()
        ))
    return keyboard.adjust(*sizes).as_markup()
def get_back_to_panel(sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back-to-admin-panel"
        )
    )

    return keyboard.adjust(*sizes).as_markup()
def get_name_emplyees_buttons(names: List[str], sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for name in names:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{name}",
                callback_data=name_callback(name=f"{name}").pack()
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text="Добавить Сотрудника",
            callback_data="add_employee"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back-to-admin-panel"
        )
    )
    return keyboard.adjust(*sizes).as_markup()

###

def get_role_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Курьер",
            callback_data=add_employee_callback(level=level + 1, menu_name="nick", data_for_db="courier").pack()
        ),
        InlineKeyboardButton(
            text="Админ",
            callback_data=add_employee_callback(level=level + 1, menu_name="nick", data_for_db="admin").pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back-to-admin-panel"
        )
    )
    return keyboard.adjust(*sizes).as_markup()

#Нужно как-то придумать как запихнуть в data_for_db ник пользователя...
def get_nick_confirm_btns(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=add_employee_callback(level=level + 1, menu_name="name1", data_for_db=data_for_db, yes=1).pack() #тут
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=add_employee_callback(level=level, menu_name="nick", data_for_db=data_for_db, yes=0).pack() #тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()

def get_name1_confirm_btns(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=add_employee_callback(level=level + 1, menu_name="name2", data_for_db=data_for_db, yes=1).pack() #тут
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=add_employee_callback(level=level, menu_name="name1", data_for_db=data_for_db, yes=0).pack() #тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()
def get_name2_confirm_btns(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=add_employee_callback(level=level + 1, menu_name="name3", data_for_db=data_for_db, yes=1).pack() #тут
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=add_employee_callback(level=level, menu_name="name2", data_for_db=data_for_db, yes=0).pack() #тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()
def get_name3_confirm_btns(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=add_employee_callback(level=level + 1, menu_name="pass", data_for_db=data_for_db, yes=1).pack() #тут
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=add_employee_callback(level=level, menu_name="name3", data_for_db=data_for_db, yes=0).pack() #тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()

def get_pass_btns(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=add_employee_callback(level=level + 1, menu_name="region", data_for_db=data_for_db, yes=1).pack()# тут
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=add_employee_callback(level=level, menu_name="pass", data_for_db=data_for_db, yes=0).pack()  # тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()

def get_correction_btns(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Роль",
            callback_data=add_employee_callback(level=0, menu_name="role", data_for_db=data_for_db).pack()  # тут
        ),
        InlineKeyboardButton(
            text="Ник телеграм",
            callback_data=add_employee_callback(level=1, menu_name="nick", data_for_db=data_for_db).pack()  # тут
        ),
        InlineKeyboardButton(
            text="Имя",
            callback_data=add_employee_callback(level=2, menu_name="name1", data_for_db=data_for_db).pack()  # тут
        ),
        InlineKeyboardButton(
            text="Фамилия",
            callback_data=add_employee_callback(level=3, menu_name="name2", data_for_db=data_for_db).pack()  # тут
        ),
        InlineKeyboardButton(
            text="Отчество",
            callback_data=add_employee_callback(level=4, menu_name="name3", data_for_db=data_for_db).pack()  # тут
        ),
        InlineKeyboardButton(
            text="Пасспорт",
            callback_data=add_employee_callback(level=5, menu_name="pass", data_for_db=data_for_db).pack()  # тут
        ),
        InlineKeyboardButton(
            text="Подтвердить",
            callback_data=add_employee_callback(level=level+1, menu_name="confirm_data", data_for_db=data_for_db).pack()  # тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()

def get_correction_btns2(level: int, data_for_db: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Роль",
            callback_data= edit_employee_callback(menu_name="role", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Ник телеграм",
            callback_data= edit_employee_callback(menu_name="nick", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Имя",
            callback_data= edit_employee_callback(menu_name="name1", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Фамилия",
            callback_data= edit_employee_callback(menu_name="name2", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Отчество",
            callback_data= edit_employee_callback(menu_name="name3", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Паспорт",
            callback_data= edit_employee_callback(menu_name="pass", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Регион",
            callback_data=edit_employee_callback(menu_name="region", take='1').pack()
        ),
        InlineKeyboardButton(
            text="Подтвердить",
            callback_data=add_employee_callback(level=level+1, menu_name="confirm_data", data_for_db=data_for_db).pack()  # тут
        )
    )
    return keyboard.adjust(*sizes).as_markup()

def get_decide(menu_name: str, value: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=edit_employee_callback(menu_name=menu_name, value=value, decide="True").pack()  # Здесь
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=edit_employee_callback(menu_name=menu_name, value=value, decide="False").pack()  # Здесь
        )
    )
    return keyboard.adjust(*sizes).as_markup()

def get_region_setting_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    reg_list = get_region_list()
    print(reg_list)
    for reg_id, reg_name in reg_list.items():
        keyboard.add(
            InlineKeyboardButton(
                text=reg_name,
                callback_data=add_employee_callback(level=level + 1, menu_name="correction", data_for_db=str(reg_id)).pack()
            )
        )
    return keyboard.adjust(*sizes).as_markup()

class ticket_callback(CallbackData, prefix="ticket"):
    level: int
    name: str | None = None
    fr: str | None = None
    to: str | None = None
    tg_id: str | None = None
    decide: str | None = None

def get_ticket_btns(level: int, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    ticket_list = get_tickets()
    for ticket in ticket_list:
        tg_id = ticket[0]
        name = get_name_by_tg_id(ticket[0])
        print(name, ticket[1], ticket[2])
        keyboard.add(
            InlineKeyboardButton(
                text=name,
                callback_data=ticket_callback(level=level+1, tg_id=tg_id, fr=str(ticket[1]), to=str(ticket[2])).pack()
            )
        )
    return keyboard.adjust(*sizes).as_markup()

def get_ticket_approve_btns(level: int, tg_id: str, fr: str, to: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text= "Да",
            callback_data=ticket_callback(level=level+1, tg_id=tg_id, fr=fr, to=to, decide="Yes").pack()
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=ticket_callback(level=level+1, tg_id=tg_id, fr=fr, to=to, decide="No").pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="change_reg"
        )
    )
    return keyboard.adjust(*sizes).as_markup()

