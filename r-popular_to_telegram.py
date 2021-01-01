# -*- coding: utf-8 -*-

import telebot
import praw
from telebot import types

TELEGRAM_TOKEN = ''
CLIENT_ID = ''
CLIENT_SECRET = ''

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def top_popular_reddit():
     content_reddit = []
     reddit = praw.Reddit(client_id=CLIENT_ID,
                          client_secret= CLIENT_SECRET,
                          user_agent='testscript')
     
     subreddit = reddit.subreddit('popular')
     top_python = subreddit.hot(limit=10)
      
     for submission in top_python:
         content_reddit.append(submission)
             
     return content_reddit
 

    
top_1 = "The Hottest post"
top_5 = "Top - 5"
top_10 = "Top - 10"

    
def generate_markup(top_1, top_5, top_10):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(top_1)
    markup.add(top_5)
    markup.add(top_10)
    return markup

def get_url_reddit_keyboard(permalink):
    full_url = 'www.reddit.com' + permalink
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Read it on reddit", url=full_url)
    keyboard.add(url_button)
    return keyboard

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "The bot is running. Enter command /help to provide more information.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Enter command /news to start.")

@bot.message_handler(commands=["news"])
def interesting(message):
    markup = generate_markup(top_1, top_5, top_10)
    bot.send_message(message.chat.id, "The bot displays the top interesting posts from Reddit. Choose Top 1, Top 5 or Top 10.", reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def top_popular(message):
    content_reddit = top_popular_reddit()     
    answer = message.chat.id
    if not answer or message.text not in [top_1,top_5,top_10]:
        bot.send_message(message.chat.id, "Enter command /news to start.")
    else:
        if message.text == top_1:
            keyboard = get_url_reddit_keyboard(content_reddit[0].permalink)
            bot.send_photo(message.chat.id, content_reddit[0].url, caption=content_reddit[0].title, reply_markup=keyboard)
               
        elif message.text == top_5:
            for submission in content_reddit[:5]:
                keyboard = get_url_reddit_keyboard(submission.permalink)
                bot.send_photo(message.chat.id, submission.url, caption=submission.title, reply_markup=keyboard)
        elif message.text == top_10:
            for submission in content_reddit:
                keyboard = get_url_reddit_keyboard(submission.permalink)
                bot.send_photo(message.chat.id, submission.url, caption=submission.title, reply_markup=keyboard)
    
if __name__ == '__main__':
    bot.polling(none_stop=True)

