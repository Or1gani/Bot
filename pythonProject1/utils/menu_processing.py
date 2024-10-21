import aiogram
from keyboards.inline import (get_profile_button, get_region_buttons, get_role_btns, get_nick_confirm_btns,
                              get_name1_confirm_btns, get_name2_confirm_btns, get_name3_confirm_btns, get_pass_btns,
                              get_correction_btns, get_correction_btns2)
from assets.menu_data import desciption_for_pages as dfp
from assets.menu_data import desciption_for_pages_settings as dfps
from typing import Optional

def find_text(menu_name, data: dict[str, str]):
    for name, text in data.items():
        if name == menu_name:
            return text

def main(level, menu_name):
    kb = get_profile_button(level=level, sizes=(1,))
    text = find_text(menu_name, dfp)
    return kb, text
def region(level, menu_name):
    kb = get_region_buttons(level=level, sizes=(1,))
    text = find_text(menu_name, dfp)
    return kb, text

def get_menu_content(level: int, menu_name: str):
    if level == 0:
        return main(level=level, menu_name=menu_name)
    elif level == 1:
        return region(level=level, menu_name=menu_name)

###

def role(level, menu_name):
    kb = get_role_btns(level=level)
    text = find_text(menu_name, dfps)
    return kb, text
def nick(level, menu_name, data_for_db):
    kb = get_nick_confirm_btns(level=level, data_for_db=data_for_db, sizes=(1,))
    text = find_text(menu_name, dfps)
    return kb, text
def name1(level, menu_name, data_for_db):
    kb = get_name1_confirm_btns(level=level, data_for_db=data_for_db, sizes=(1,))
    text = find_text(menu_name, dfps)
    return kb, text
def name2(level, menu_name, data_for_db):
    kb = get_name2_confirm_btns(level=level, data_for_db=data_for_db, sizes=(1,))
    text = find_text(menu_name, dfps)
    return kb, text
def name3(level, menu_name, data_for_db):
    kb = get_name3_confirm_btns(level=level, data_for_db=data_for_db, sizes=(1,))
    text = find_text(menu_name, dfps)
    return kb, text
def pas(level, menu_name, data_for_db):
    kb = get_pass_btns(level=level, data_for_db=data_for_db, sizes=(1,))
    text = find_text(menu_name, dfps)
    return kb, text
def correction(level, menu_name, data_for_db):
    kb = get_correction_btns2(level=level, data_for_db=data_for_db, sizes=(1,))
    text = find_text(menu_name, dfps)
    return kb, text


def get_setting_content(level: int, menu_name: str, data_for_db: Optional[str]):
    if level == 0:
        return role(level=level, menu_name=menu_name)
    elif level == 1:
        return nick(level=level, menu_name=menu_name, data_for_db=data_for_db)
    elif level == 2:
        return name1(level=level, menu_name=menu_name, data_for_db=data_for_db)
    elif level == 3:
        return name2(level=level, menu_name=menu_name, data_for_db=data_for_db)
    elif level == 4:
        return name3(level=level, menu_name=menu_name, data_for_db=data_for_db)
    elif level == 5:
        return pas(level=level, menu_name=menu_name, data_for_db=data_for_db)
    elif level == 6:
        return correction(level=level, menu_name=menu_name, data_for_db=data_for_db)