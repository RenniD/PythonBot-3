
# 7823429661:AAEaErk_RdI_Aj7FJvgmuRYxzI1k2-nHmus

from telegram import Update, InlineKeyboardButton, InputMediaPhoto, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, \
    MessageHandler, filters

# Стадії конверсії
NUMBER, DELIVERY_TIME, FORM_OF_DELIVERY, DELIVERY, PAY, ORDER = range(6)

app = ApplicationBuilder().token('7823429661:AAEaErk_RdI_Aj7FJvgmuRYxzI1k2-nHmus').build()

# ---------------------------------------------------

async def contacts_command(update, context):
    contacts_text = (
        "Контактний номер: +380675994939, +380935994939, +380665994939\n"
        "Адрес:Вознюка 1в,Днепр"
    )
    await update.message.reply_text(contacts_text)


async def delivery_command(update, context):
    delivery_text = (
        "Приднепровск - доставка 50 грн.\n"
        "Цапли, Рыбальское - 100-150 грн (стоимость уточняется при заказе)\n."
        "Любимовка - 200 грн.\n"
        "Победа 6 - 150 грн.\n"
        "При заказе от 500 грн предоставляется скидка 50 грн на доставку.\n"
    )
    await update.message.reply_text(delivery_text)

async def work_schedule_command(update, context):
        work_schedule_text = (
            "Прием заказов осуществляется с 10:00 до 20:00.Выдача заказов - с 11:15 до 21:00.\n"
        )
        await update.message.reply_text(work_schedule_text)
#--------------------------------------------------------------------------------------------------------------
async def start_command(update,context):
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
        elif query.data == "delivery":
            await query.message.reply_text("Приднепровск - доставка 50 грн.\n"
        "Цапли, Рыбальское - 100-150 грн (стоимость уточняется при заказе)\n."
        "Любимовка - 200 грн.\n"
        "Победа 6 - 150 грн.\n"
        "При заказе от 500 грн предоставляется скидка 50 грн на доставку.\n"
             )
        elif query.data == "contacts":
            await query.message.reply_text("Контактний номер: +380675994939, +380935994939, +380665994939\n"
        "Адрес:Вознюка 1в,Днепр"
             )
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
    context.user_data['order'] = update.message.text
    booking_details = (
    f"Ваши данные для заказа:\n"
    f"- номер телефона: {context.user_data['number']}\n"
    f"- время доставки: {context.user_data['delivery_time']}\n"
    f"- форма доставки: {context.user_data['form_of_delivery']}\n"
    f"- адрес доставки: {context.user_data['delivery']}\n"
    f"- форму оплаты: {context.user_data['pay']}\n"
    f"- заказ: {context.user_data['order']}\n"
    "Если все верно, наш администратор свяжется с вами для подстверждения."
    )

    await update.message.reply_text(booking_details, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
async def cancel(update,context):
    await update.message.reply_text("Заказ отменен.Возращайтесь, когда будете готовы!",reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
# ---------------------------------------------------

#Добавление ConversationHandler для заказа
booking_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern="^ordering_food$")],
    states={
    NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number)],
    DELIVERY_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, delivery_time)],
    FORM_OF_DELIVERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_of_delivery)],
    DELIVERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, delivery)],
    PAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, pay)],
    ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_message=True
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


app.add_handler(booking_handler)

def main():
    app.add_handler(CommandHandler("start", start_command))
    app.run_polling()


if __name__ == '__main__':
    main()
