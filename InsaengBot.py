## InsaengBot using python-telegram-bot library

# Import bot token from private directory using .gitignore
from privateFiles.insaengbotToken import token


# logs
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# call bot
import telegram
bot = telegram.Bot(token=token)
#print(bot.get_me())


# initialize updater and dispatcher
from telegram.ext import Updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


# define a function that processes a specific type of update
def start(update, context):
    """
    Answers "I'm a bot, please talk to me!"
    """
    print(type(context.bot))
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
# The goal is to have the 'start' function called every time the Bot receives a Telegram 
# message that contains the /start command. To accomplish that, you can use a CommandHandler 
# (one of the provided Handler subclasses) and register it in the dispatcher:

from telegram.ext import PrefixHandler
start_handler = PrefixHandler('!','start', start)
dispatcher.add_handler(start_handler)

########################################
##### COVID Schedule command start #####
def covid_schedule(update, context):
    """
    Returns link to picture for Covid 19 back to normal schedule in ON and QC
    """
    print(type(context.bot))
    context.bot.send_message(chat_id=update.effective_chat.id, \
                             text="https://infogram.com/ontario-and-quebec-reopening-comparison-1h7k230371jyg2x")
    
from telegram.ext import PrefixHandler
schd_handler = PrefixHandler('!','schd', covid_schedule)
dispatcher.add_handler(schd_handler)
###### COVID Schedule command end ######
########################################

import random
import re #import regex

def versus(msg):
    """
    Select random output from a string that is separated by one or more "vs".
    A unique "vs" is identified by tailing and fronting space, tab, new line or return character.
    """
    
    #print("Function: versus")
    #print("Message: ",msg)
    answer_msg = ""
    #transform msg
    if re.search("[ \t\n\r]+vs[ \t\n\r]+", msg):
        temp = re.split("[ \t\n\r]+vs[ \t\n\r]+",msg)
        #print(temp)
        answer_msg = random.choice(temp)
    return answer_msg
        

def isAble(msg):
    """
    Answers yes or no to user questions ending with "ㄱㄴ?"
    """
    #print("Function: isAble")
    #print("Message: ",msg)
    answer_msg = ""
    if re.search("^(ㄱㄴ\?+)$|([ \t\n\r]ㄱㄴ\?+)$", msg):
        yes_list = ["ㅇㅇ", "ㄱㄴ!" , "ㅇㅋ"]
        no_list  = ["ㄴㄴ", "자제점;;", "않이"]
        answer_list = random.choice([yes_list, no_list])
        answer_msg = random.choice(answer_list)
    return answer_msg


def msg_fn_group0(update, context):
    """
    Message function group for 'versus' and 'isAble' text functions.
    Executes message in the order of 'versus' then 'isAble'.
    """
    user_msg = update.message.text
    #print(user_msg)
    answer_msg_dict = {"versus": "",
                        "isAble": ""}
    answer_msg_dict["versus"] = versus(user_msg)
    answer_msg_dict["isAble"] = isAble(answer_msg_dict["versus"]) if answer_msg_dict["versus"] \
                                                                else isAble(user_msg)
    #print(answer_msg_dict)
    order = ["versus", "isAble"]
    
    answer_msg = '\n'.join([answer_msg_dict[x] for x in order if answer_msg_dict[x]])
    #print(answer_msg)
    if answer_msg:
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer_msg)

# Message handler for versus and isAble functions. 
# Uses a filter to filter out any commands. (Commands start with a '/' (slash))
from telegram.ext import MessageHandler, Filters
msg_handler0 = MessageHandler(Filters.text & (~Filters.command), msg_fn_group0)
dispatcher.add_handler(msg_handler0, group = 0)


# Run to start the bot
updater.start_polling(timeout=3, drop_pending_updates=True)


# stop the bot
#updater.stop()