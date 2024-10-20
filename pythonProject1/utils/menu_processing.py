import aiogram
from keyboards.inline import get_profile_button, get_region_buttons
from assets.menu_data import desciption_for_pages as dfp

def find_text(menu_name):
    for name, text in dfp.items():
        if name == menu_name:
            return text
def main(level, menu_name):
    kb = get_profile_button(level=level, sizes=(1,))
    text = find_text(menu_name)
    return kb, text
def region(level, menu_name):
    kb = get_region_buttons(level=level, sizes=(1,))
    text = find_text(menu_name)
    return kb, text



def get_menu_content(level: int, menu_name: str):
    if level == 0:
        return main(level=level, menu_name=menu_name)
    elif level == 1:
        return region(level=level, menu_name=menu_name)

def role(level, menu_name):
    pass
def nick(level, menu_name):
    pass
def fio(level, menu_name):
    pass
def pas(level, menu_name):
    pass
def confirm(level, menu_name):
    pass
def correction(level, menu_name):
    pass


def get_setting_content(level: int, menu_name: str):
    if level == 0:
        return role(level=level, menu_name=menu_name)
    elif level == 1:
        return nick(level=level, menu_name=menu_name)
    elif level == 2:
        return fio(level=level, menu_name=menu_name)
    elif level == 3:
        return pas(level=level, menu_name=menu_name)
    elif level == 4:
        return confirm(level=level, menu_name=menu_name)
    elif level == 5:
        return correction(level=level, menu_name=menu_name)


