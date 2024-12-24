
from telegram import Update, InlineKeyboardButton, InputMediaPhoto, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, \
    MessageHandler, filters
import sqlite3
import asyncio

# Стадії конверсії
NUMBER, DELIVERY_TIME, FORM_OF_DELIVERY, DELIVERY, PAY, ORDER = range(6)



app = ApplicationBuilder().token('7407148766:AAFLNMOcY13rEBo_xtbQ0jgM7QLUPKkKtVU').build()

#______________________________________________
def setup_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Создание таблицы пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    chat_id INTEGER NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    )
    """)

    # Создание таблицы заказа
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id INTEGER NOT NULL,
     number TEXT NOT NULL,
     delivery_time TEXT NOT NULL,
     form_of_delivery TEXT NOT NULL,
     delivery TEXT NOT NULL,
     pay TEXT NOT NULL,
     order_ TEXT NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (user_id) REFERENCES user (id)
    )
    """)
    connection.commit()
    connection.close()
    print("База данних успешно настроена")

def add_user(username, chat_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO user (username, chat_id)
        VALUES (?, ?)
        """, (username, chat_id))
        connection.commit()
        print(f"Пользователь {username} успешно добавлен.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        connection.close()

def add_booking(chat_id, number, delivery_time, form_of_delivery, delivery, pay, order_):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        #Получение user_id за chat_id
        cursor.execute("SELECT id FROM user WHERE chat_id =?", (chat_id))
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            cursor.execute("""
            INSERT INTO bookings (chat_id, number, delivery_time, form_of_delivery, delivery, pay, order_)
            VALUES(?, ?, ?, ?, ?, ?, ?) 
            """, (chat_id, number, delivery_time, form_of_delivery, delivery, pay, order_))
            connection.commit()
            print("Бронирование успешно добавлено.")
        else:
            print("Пользователя не найдено в базе.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        connection.close()

def get_all_users():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = cursor.fetchall()
    connection.close()
    return [user[0] for user in users]
async def broadcast_message(update, context):
    users = get_all_users()
    messages = "Рассылка для всех пользователей!"
    successful = 0
    failed = 0

    for chat_id in users:
        try:
            await context.bot.send_massage(chat_id=chat_id, text=messages)
            successful += 1
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {chat_id}: {e}")
            failed += 1
        await asyncio.sleep(0.1)  # Добавить задержку для избежания лимиту Telegram

    await update.message.reply_text(f"Рассылка закончена.Успешно:{successful}, Неудачно:{failed}")


# ---------------------------------------------------

async def contacts_command(update, context):

    contacts_text = (
        "Контактний номер: +380675994939, +380935994939, +380665994939\n"
        "Адрес:Вознюка 1в,Днепр"
    )
    await update.message.reply_text(contacts_text)

async def work_schedule_command(update, context):
        work_schedule_text = (
            "Прием заказов осуществляется с 10:00 до 20:00.Выдача заказов - с 11:15 до 21:00.\n"
        )
        await update.message.reply_text(work_schedule_text)
#--------------------------------------------------------------------------------------------------------------
# Команда/start c cохранением пользователя
async def start_command(update,context):
        username = update.effective_user.username or "NoUsername"
        chat_id = update.effective_user.id

        # Добавление пользователя в базу данних
        add_user(username, chat_id)

        inline_keyboard = [
            [InlineKeyboardButton("Меню", url="https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MTQwODUxMjg1MzQ2Mzg4?story_media_id=3469935359620179540&igsh=MTZqdm1mN3Z1dnp1dQ==")],
            [InlineKeyboardButton("Акции",callback_data="stocks")],
            [InlineKeyboardButton("График работы", callback_data="work_schedule")],
            [InlineKeyboardButton("Оформить заказ", callback_data="ordering_food")],
            [InlineKeyboardButton("Доставка", callback_data="delivery")],
            [InlineKeyboardButton("Контакты", callback_data="contacts")],
            [InlineKeyboardButton("Наш Instagram", url="https://www.instagram.com/firepizza.dp?igsh=MWp2aHI4cGxhODM0ag==")]
       ]

        markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(
        "Добро пожаловать Вас приветствует служба доставки еды 'FirePizza'!\n"
        "Здесь вы можете ознакомится с нашим меню, акциями, оформить заказ, узнать график работы,контакты, ознакомится с услугами доставки.\n",
        reply_markup=markup)

async def button_handler(update, context):
        query = update.callback_query
        await query.answer()

        if query.data == "work_schedule":
            await query.message.reply_text(
            "Прием заказов осуществляется с 10:00 до 20:00.Выдача заказов - с 11:15 до 21:00.\n"
             )
            return ConversationHandler.END

        elif query.data == "delivery":
            await query.message.reply_text("Приднепровск - доставка 50 грн.\n"
        "Цапли, Рыбальское - 100-150 грн (стоимость уточняется при заказе)\n."
        "Любимовка - 200 грн.\n"
        "Победа 6 - 150 грн.\n"
        "При заказе от 500 грн предоставляется скидка 50 грн на доставку.\n"
             )
            return ConversationHandler.END

        elif query.data == "contacts":
            await query.message.reply_text("Контактний номер: +380675994939, +380935994939, +380665994939\n"
        "Адрес:Вознюка 1в,Днепр"
             )
            return ConversationHandler.END

        elif query.data == "ordering_food":
                    await query.message.reply_text("Для оформления заказа укажите пожалуйста: адрес доставки,\n"
                "ваш номер телефона для связи с курьером,\n"
                "форму оплатить заказ: наличными или картой,\n"
                "на какое время вам удобно получить заказ \n"
                        )
                    print("Потрапив у стан NUMBER")  # Відладкове повідомлення
                    return NUMBER


        elif query.data == "stocks":
            room_image_url = "img/234.png"
            caption = ("При заказе от 500 грн предоставляется скидка 50 грн на доставку.\n"
                "При заказе от 500 грн доставка по г. Приднепровск - бесплатная.\n")
            room_image_url2 ="img/Birthday 1.png"
            caption2 = ("Празднуй день рождения с выгодой - именинникам дарим скидку 10% на все меню. Скидка действует за два дня до и два дня после вашего Дня рождения. Для получения скидки нужно иметь при себе оригинал документа, подтверждающего дату рождения.\n"
                "*Скидка не суммируется с другими предложениями.\n")
            try:
                await query.message.reply_photo(photo=room_image_url, caption=caption)
            except FileNotFoundError as e:
                await query.message.reply_text(f"Ошибка: файл {e.filename} не найдено.")
            except Exception as e:
                await query.message.reply_text(f"Возникла ошибка: {str(e)} ")
        return ConversationHandler.END

# ---------------------------------------------------
async def number(update,context):
    context.user_data['number'] = update.message.text
    await update.message.reply_text("Введите ваш номер телефона для связи (например, +380951111111):")
    return DELIVERY_TIME

async def delivery_time (update,context):
    context.user_data['delivery_time'] = update.message.text
    await update.message.reply_text("Укажите время доставки")
    return FORM_OF_DELIVERY

async def form_of_delivery (update,context):
    context.user_data['form_of_delivery'] = update.message.text
    reply_keyboard = [["Самовывоз", "Доставка"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите форму доставки:",reply_markup=markup)
    return DELIVERY

async def delivery (update,context):
    context.user_data['delivery'] = update.message.text
    await update.message.reply_text("Укажите адрес доставки")
    return PAY

async def pay (update,context):
    context.user_data['pay'] = update.message.text
    reply_keyboard = [["Наличные", "Карта"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите форму оплаты:",reply_markup=markup)
    return ORDER

async def order (update,context):
    chat_id = update.effective_user.id
    context.user_data['order'] = update.message.text

    # Сохранение в базе данных
    add_booking(
        chat_id,
        context.user_data['number'],
        context.user_data['delivery_time'],
        context.user_data['form_of_delivery'],
        context.user_data['delivery'],
        context.user_data['pay'],
        context.user_data['order'],
    )
    booking_details = (
    f"Ваши данные для заказа:\n"
    f"- номер телефона: {context.user_data['number']}\n"
    f"- время доставки: {context.user_data['delivery_time']}\n"
    f"- форма доставки: {context.user_data['form_of_delivery']}\n"
    f"- адрес доставки: {context.user_data['delivery']}\n"
    f"- форму оплаты: {context.user_data['pay']}\n"
    f"- заказ: {context.user_data['order']}\n"
    "Если все верно, наш администратор свяжется с вами для подтверждения."
    )

    await update.message.reply_text(booking_details, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
async def cancel(update,context):
    await update.message.reply_text("Заказ отменен.Возращайтесь, когда будете готовы!",reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Инициализация базы данных ----------
setup_database()

#Добавление ConversationHandler для заказа
booking_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern="^(ordering_food|work_schedule|delivery|contacts|stocks)$")],
    states={
    NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number)],
    DELIVERY_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, delivery_time)],
    FORM_OF_DELIVERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_of_delivery)],
    DELIVERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, delivery)],
    PAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, pay)],
    ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_user=True
)

#-------------------------------------------------------------
async def send_photos(update,context):
# Пути к локальным файлам
    room_image_url = "img/234.png"
    caption = ("При заказе от 500 грн предоставляется скидка 50 грн на доставку.\n"
               "При заказе от 500 грн доставка по г. Приднепровск - бесплатная.\n")
    room_image_url2 = "img/Birthday 1.png"
    caption2 = ("Празднуй день рождения с выгодой - именинникам дарим скидку 10% на все меню. Скидка действует за два дня до и два дня после вашего Дня рождения. Для получения скидки нужно иметь при себе оригинал документа, подтверждающего дату рождения.\n"
    "*Скидка не суммируется с другими предложениями.\n")
    try:
        await update.message.reply_photo(photo=room_image_url, caption=caption)
    except FileNotFoundError as e:
        await update.message.reply_text(f"Ошибка: файл {e.filename} не найдено.")
    except Exception as e:
        await update.message.reply_text(f"Возникла ошибка: {str(e)} ")

# добавление обработчика команд
app.add_handler(CommandHandler("sendphotos", send_photos))
app.add_handler(CommandHandler("contacts", contacts_command))
app.add_handler(CommandHandler("work_schedule", work_schedule_command))


app.add_handler(booking_handler)

def main():
    app.add_handler(CommandHandler("start", start_command))
    app.run_polling()


if __name__ == '__main__':
    main()
