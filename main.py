import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота (ЗАМЕНИТЕ НА СВОЙ!)
TOKEN = "8533696494:AAFUjQM1ynZPDn87Wvb_93H3tmKQO06UHTM"

# Путь к изображению на PythonAnywhere
# Измените 'ваш_username' на ваш реальный username
IMAGE_PATH = "/home/Uncedia/Uncedia/Uncedia.png"

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} запустил бота")
    
    # Создаем клавиатуру с кнопкой
    keyboard = [
        [InlineKeyboardButton("Перейти в бота", url="http://t.me/Uncedia_bot/startbot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Пробуем отправить изображение
    try:
        # Проверяем существование файла
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption="Добро Пожаловать! Вы попали в официального бота Uncedia.\n\nUncedia - это независимая энциклопедия в Telegram",
                    reply_markup=reply_markup
                )
                logger.info("Изображение успешно отправлено")
        else:
            logger.warning(f"Изображение не найдено по пути: {IMAGE_PATH}")
            # Отправляем текстовое сообщение, если изображение не найдено
            await send_text_message(update, reply_markup)
            
    except Exception as e:
        logger.error(f"Ошибка при отправке изображения: {e}")
        # Отправляем текстовое сообщение в случае ошибки
        await send_text_message(update, reply_markup)

# Функция для отправки текстового сообщения (резервный вариант)
async def send_text_message(update: Update, reply_markup):
    await update.message.reply_text(
        "🎉 *Добро Пожаловать!*\n\n"
        "Вы попали в официального бота *Uncedia*.\n\n"
        "*Uncedia* - это независимая энциклопедия в Telegram\n\n"
        "Наша миссия - предоставлять свободный доступ к знаниям!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Основная функция
def main() -> None:
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    
    # Запускаем бота
    print("🤖 Бот Uncedia запущен...")
    print(f"📂 Ожидается изображение по пути: {IMAGE_PATH}")
    print("✅ Используйте /start для тестирования")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()