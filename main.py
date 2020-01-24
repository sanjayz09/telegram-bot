#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging

import telegram
from flask import Flask
from flask import request

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

API_TOKEN = config['TELEGRAM']['ACCESS_TOKEN']
WEB_HOOK_PATH = config['TELEGRAM']['WEB_HOOK_PATH']

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = telegram.Bot(token=API_TOKEN)
bot_name = "@Robot"


@app.route('/')
def root():
    if request.method == "GET":
        return r'{"Robot":"hi"}'


@app.route(WEB_HOOK_PATH, methods=['POST'])
def launcher():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        logging.info("Calling {}".format(update.message))
        try:
            handle_message(update.message)
        except:
            logging.info('handle_message ERROR')
    return 'ok'


def handle_message(message):
    text = message.text
    if text is None:
        logging.info('Warning: message.text == None')
        return
    if "/start" in text:
        send_message_text(message, "Hi, I'm Robot!")
    elif "/echo" in text:
        echo(message)
    elif "/help" in text:
        send_message_text(message, text_help_tip)
    else:
        send_message_text(message, "Can't find cmd!\n")
        send_message_text(message, text_help_tip)

    logging.info(text)


text_help_tip = ('/echo - Repeat the same message back\n'
                 '/help - Help Info')


def echo(message):
    """
    repeat the same message back (echo)
    """
    cmd, text = parse_cmd_text(message.text)
    if text is None or len(text) == 0:
        send_message_text(message, "Usage error: Example -> /echo xxx")
    else:
        send_message_text(message, text)


def parse_cmd_text(text):
    # Telegram understands UTF-8
    cmd = None
    if '/' in text:
        try:
            index = text.index(' ')
        except ValueError as e:
            return text, None
        cmd = text[:index]
        text = text[index + 1:]
    if cmd is not None and '@' in cmd:
        cmd = cmd.replace(bot_name, '')
    return cmd, text


def send_message_text(message, text):
    bot.sendMessage(chat_id=message.chat.id, text=text)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=18443)
