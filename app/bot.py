import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models.schedule import Schedule
from app.db.models.user import User
from sqlalchemy.orm import Session

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Хранилище chat_id пользователей
user_chats = {}


# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Команда /start для регистрации chat_id
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user_chats[message.from_user.id] = message.chat.id
    await message.answer("✅ Вы успешно зарегистрированы для получения уведомлений!")


# Команда для получения расписания
@dp.message_handler(commands=["schedule"])
async def get_schedule(message: types.Message):
    db = next(get_db())
    schedules = db.query(Schedule).all()

    if not schedules:
        await message.answer("❗ Расписание пока не добавлено.")
        return

    schedule_list = ""
    for schedule in schedules:
        schedule_list += (
            f"🚍 Маршрут: {schedule.route_id}\n"
            f"👨‍✈️ Водитель: {schedule.driver_id}\n"
            f"⏰ Время: {schedule.departure_time} - {schedule.return_time}\n"
            f"📅 Дата: {schedule.date}\n\n"
        )

    await message.answer(schedule_list)


# Уведомление водителя о новом рейсе
async def notify_driver(driver_id: int, message: str):
    if driver_id in user_chats:
        chat_id = user_chats[driver_id]
        await bot.send_message(chat_id, message)


# Команда для получения информации о рейсе
@dp.message_handler(commands=["my_route"])
async def get_driver_route(message: types.Message):
    user_id = message.from_user.id
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        await message.answer("❗ Вы не зарегистрированы в системе.")
        return

    schedules = db.query(Schedule).filter(Schedule.driver_id == user.id).all()

    if not schedules:
        await message.answer("❗ У вас пока нет назначенных маршрутов.")
        return

    schedule_info = ""
    for schedule in schedules:
        schedule_info += (
            f"🚍 Маршрут: {schedule.route_id}\n"
            f"⏰ Время: {schedule.departure_time} - {schedule.return_time}\n"
            f"📅 Дата: {schedule.date}\n\n"
        )

    await message.answer(schedule_info)


# Обработчик ошибок
@dp.errors_handler()
async def error_handler(update, exception):
    print(f"Ошибка: {exception}")
    return True

async def main():
    await dp.start_polling(bot)

# Запуск бота
async def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(main())
