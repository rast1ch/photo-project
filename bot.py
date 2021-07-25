import psycopg2
import os
import atexit
os.environ['DJANGO_SETTINGS_MODULE'] = 'photo_project.settings'
from django.conf import settings
from telebot import TeleBot
from telebot import types


# Подключение к БД
conn = psycopg2.connect(dbname=settings.DATABASES['default']['NAME'],
                        user=settings.DATABASES['default']['USER'],
                        password=settings.DATABASES['default']['PASSWORD'],
                        host=settings.DATABASES['default']['HOST'])
cur = conn.cursor()




def atexit_func():
    cur.close()
    conn.close()
    print('\nGoodbye world!!!')


bot = TeleBot(settings.TELEBOT_TOCKEN)

@bot.message_handler(commands=["start"])
def start_command_handler(msg):
    continue_markup  = types.InlineKeyboardMarkup()
    continue_markup.add(types.InlineKeyboardButton(text="Продолжить",
                                                   callback_data='continue_start'))

    # Проверяем наличи id в БД
    bot.send_message(msg.from_user.id, 'BOT funcctions....',reply_markup=continue_markup)
    cur.execute(f"""SELECT telegram_id
                    FROM admin_page_profile
                    WHERE telegram_id='{msg.from_user.id}';""")
    if not cur.fetchall():
        # Проверям наличие реферального кода в ссылке
        if " " in msg.text:
            referrer_candidate = msg.text.split()[1]

            # Проверяем формат
            if referrer_candidate.isdigit():

                if referrer_candidate != str(msg.from_user.id):
                    cur.execute(f"""SELECT id
                                    FROM admin_page_profile
                                    WHERE telegram_id='{referrer_candidate.strip()}';""")
                    refer_id = cur.fetchone()[0]

                    if refer_id:
                        cur.execute(f"""INSERT INTO admin_page_profile (telegram_id,ref_slug,referal_id)
                                        VALUES ('{msg.from_user.id}','https://t.me/photostock123_bot?start={msg.from_user.id}', {refer_id})""")
                        return None

        cur.execute(f"""INSERT INTO admin_page_profile (telegram_id,ref_slug,referal_id)
                        VALUES ('{msg.from_user.id}','https://t.me/photostock123_bot?start={msg.from_user.id}', NULL)""")

    conn.commit()
    return None
        

@bot.message_handler(commands=["/help"])
def help_command_handler(msg):
    bot.send_message(msg.from_user.id, 'Help...')



@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data == 'continue_start'):
        msg = bot.send_message(call.from_user.id, 'You clicked continue')
        bot.register_next_step_handler(msg,)


def choose_subcategory(msg):
    cur.execute("""SELECT *
                   FROM admin_page_subcategory S
                   JOIN admin_page_category C ON S.category_id = C.id;""")
    

if __name__ == '__main__':
    bot.polling(none_stop=True)
    atexit.register(atexit_func)

