"""FSM holatlari."""
from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    tabel = State()      # tabel raqamini kiritish (parol vazifasini bajaradi)


class ReportForm(StatesGroup):
    choosing_date = State()
    custom_date = State()
    choosing_mode = State()   # mavjud hisobotga qo'shishmi yoki almashtirishmi
    done = State()
    problems = State()
    plans = State()
    confirm = State()


class ExportForm(StatesGroup):
    custom_period = State()
