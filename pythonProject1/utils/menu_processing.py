import aiogram
from pythonProject1.keyboards.inline import get_profile_button
def main(level):
    return get_profile_button(level=level, sizes=(1,))

def get_menu_content(level: int):
    if level == 0:
        return main(level=level)