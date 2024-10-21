from aiogram.fsm.state import State, StatesGroup

class add_employee_states(StatesGroup):
    waiting_for_nick = State()
    waiting_for_name1 = State()
    waiting_for_name2 = State()
    waiting_for_name3 = State()
    waiting_for_pass = State()
    waiting_for_confirmation = State()