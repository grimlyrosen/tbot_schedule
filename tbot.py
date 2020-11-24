TOKEN = "1408399142:AAE5JxpiyAaXNJ_VI8X7-IPXHOjitl82CF8"

from telegram import Update
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from datetime import datetime
from tbot_schedule.ring import get_rings, get_next_lesson, get_schedule

KEYBOARD_BUTTONS = [
    "Следующий урок",
    "Расписание на неделю"
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
SCHEDULE = get_schedule()
RINGS = get_rings()
DAYS = {1: "понедельник",
        2: "вторник",
        3: "среду",
        4: "четверг",
        5: "пятницу"}

def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == KEYBOARD_BUTTONS[0]:
        return now_handler(update=update, context=context)
    if text == KEYBOARD_BUTTONS[1]:
        return week_handler(update=update, context=context)


def start_handler(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=KEYBOARD_BUTTONS[0]),
                KeyboardButton(text=KEYBOARD_BUTTONS[1]),
            ]
        ]
    )
    return update.message.reply_text("Привет, нажми меня", reply_markup=reply_markup)


def inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="Понедельник", callback_data="day1"),
            InlineKeyboardButton(text="Вторник", callback_data="day2"),
            InlineKeyboardButton(text="Среда", callback_data="day3"),
            InlineKeyboardButton(text="Четверг", callback_data="day4"),
            InlineKeyboardButton(text="Пятница", callback_data="day5"),

        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def week_handler(update: Update, context: CallbackContext):
    return update.message.reply_text("Выберите день недели", reply_markup=inline_keyboard())


def week_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    day = int(query.data[3])
    today_schedule = SCHEDULE[day]
    text = f"Расписание на {DAYS[day]}\n"
    for lesson in today_schedule:
        if today_schedule[lesson]:
            text += f'{RINGS[day][lesson].strftime("%H %M")}: {today_schedule[lesson]}\n'

    query.edit_message_text(text=text, reply_markup=inline_keyboard())


def now_handler(update: Update, context: CallbackContext):
    weekday = datetime.today().isoweekday()
    curtime = datetime.now().time()
    next_lesson = get_next_lesson(RINGS, weekday, curtime)
    text = "Сегодня уроков  нет"
    if next_lesson:
        today_schedule = SCHEDULE[weekday]
        for i in range(next_lesson, len(today_schedule)):
            if today_schedule[i]:
                text = f"Следующий урок '{today_schedule[i]}' в {RINGS[weekday][i]}"
                break

    return update.message.reply_text(text)


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )
    print(updater.bot.get_me())

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=week_button_handler, pass_chat_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
