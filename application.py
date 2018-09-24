"""Template simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="d66709ec90fb4683700c8bd701406b8e0fdf54c5",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher


def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    print(user_data)


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("سلام \n به سامانه *کميته بهداشت و *\
                          *درمان هيات آل يس* خوش آمديد")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    ask_question(bot,update)
   # dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), ask_question))


def ask_question(bot, update):
    user_peer = update.get_effective_user()
    my_message = TextMessage("ted!")
   # bot.send_message(my_message, user_peer, success_callback=success, failure_callback=failure)
    # Set client message as general message of a template message
    general_message = update.get_effective_message()
    # Create how many buttons you like with TemplateMessageButton class
    btn_list = [TemplateMessageButton(text="بروز رساني فايل موجود", value="berooz", action=0),
                TemplateMessageButton(text="اضافه کردن فايل جديد", value="jadid", action=0)]
    # Create a Template Message
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TemplateResponseFilter(keywords=["berooz"]),
                                                                       berooz),
                                                        MessageHandler(TemplateResponseFilter(keywords=["jadid"]),
                                                                       jadid)])


# Use when answer is 'berooz'
def berooz(bot, update):
  
    user_peer = update.get_effective_user()
    
    # Use CommandHandler to handle a command which is sent by client
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("/end", finish_conversion))


# Use when answer is 'jadid'
def jadid(bot, update):
    message = TextMessage("نام مددجو را وارد نماييد")         
    user_peer = update.get_effective_user()
    kwargs = {"message": message, "user_peer": user_peer}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       # Set Regex pattern for TextFilter
                                                       [MessageHandler(TextFilter(), ask_bimari),
                                                        MessageHandler(DefaultFilter(), finish_conversion)])

def ask_bimari(bot, update):
        message = TextMessage("نوع بيماري مددجو را وارد کنيد")  
        user_peer = update.get_effective_user()
        kwargs = {"message": message, "user_peer": user_peer}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
        dispatcher.register_conversation_next_step_handler(update,
                                                           MessageHandler(TextFilter(),
                                                                          ask_mahal_sokonat))

def ask_mahal_sokonat(bot, update):
    message = TextMessage("محل سکونت")  
    user_peer = update.get_effective_user()
    kwargs = {"message": message, "user_peer": user_peer}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       MessageHandler(TextFilter(),ask_sen ))



def ask_sen(bot, update):
    message = TextMessage("سن")  
    user_peer = update.get_effective_user()
    kwargs = {"message": message, "user_peer": user_peer}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       MessageHandler(TextFilter(), sabt_madadjo_jadid))


def sabt_madadjo_jadid(bot, update):
      message = TextMessage("اطلاعات مددجو ثبت شد")
      user_peer = update.get_effective_user()
      name_obj = update.get_effective_message()
      bimari = name_obj.text
      kwargs = {"message": message, "user_peer": user_peer}
      bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
     # dispatcher.register_conversation_next_step_handler(update, MessageHandler(DefaultFilter(), finish_conversion))
      finish_conversion(bot, update)  

def finish_conversion(bot, update):
    message = TextMessage("*Thanks* \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    # Finish conversation
    dispatcher.finish_conversation(update)


updater.run()
