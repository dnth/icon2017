#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

from pygame.locals import *
import pygame.camera

import time

empty_bay = 0

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO, NUM_PLATE = range(5)


def start_reg(bot, update):
    # reply_keyboard = [['Boy', 'Girl', 'Other']]
    #
    # update.message.reply_text(
    #     'Hi! My name is Professor Bot. I will hold a conversation with you. '
    #     'Send /cancel to stop talking to me.\n\n'
    #     'Are you a boy or a girl?',
    #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    #
    # return NUM_PLATE

    update.message.reply_text("Please enter your vehicle plate number")
    return NUM_PLATE

def start_park(bot, update):
    bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADRgADVSx4C5-O4uhXcrjOAg")

    reply_keyboard = [['Peekaboo', 'Bays Left'],
                       ['Park Now', 'Request Shuttle']]
    update.message.reply_text("Hi! I am your TNB Valet. Allow me to ease your parking experience in TNB Bangsar HQ. "
                              "What would you like me to do?\n\n"
                              "Please select from the options below.\n\n"
                              "*PEEKABOO*: Take an image of the parking zone\n"
                              "*BAYS LEFT*: Show the number of empty parking bays\n"
                              "*PARK NOW*: Book a parking bay now by registering your vehicle plate\n"
                              "*REQUEST SHUTTLE*: Call for a shuttle to pick you from the waiting room",
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def peekaboo(bot, update):
    bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADXAADVSx4C01PSHLmRFaqAg")

    try:
        update.message.reply_text("Wait a sec.. lemme take a peek.....", one_time_keyboard=True)
        num_of_burst_shots = 1
        pygame.init()
        pygame.camera.init()
        # cam = pygame.camera.Camera("/dev/video0", (480,360))
        # cam = pygame.camera.Camera("/dev/video0", (640,480))
        cam = pygame.camera.Camera("/dev/video0", (1280, 720))
        cam.start()

        for i in range(num_of_burst_shots):
            image = cam.get_image()
            # image = pygame.transform.rotate(image, 90)
            pygame.image.save(image, 'visitor_' + '{}'.format(i) + '.jpg')
            # bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            bot.sendPhoto(update.message.chat_id, photo=open('visitor_' + '{}'.format(i) + '.jpg', 'rb'))
            time.sleep(0.2)

    except Exception as e:
        print e
    finally:
        cam.stop()

def bays_left(bot, update):
    # update.message.reply_text("Estimating remaining bays left.. There are {} empty bay(s) at the moment.".format(empty_bay))
    update.message.reply_text("Estimating remaining bays left...", one_time_keyboard=True)

    if empty_bay == 0:
        bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADTAADVSx4C1Euf8V7S5s0Ag")
        update.message.reply_text("Yikes! There are no empty bays the moment. Try again later.", one_time_keyboard=True)

    else:
        bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADUAADVSx4C4RAPsaJNQ4GAg")
        update.message.reply_text("There is(are) {} empty bay(s) at the moment.".format(empty_bay))
        reply_keyboard = [['Peekaboo', 'Bays Left'],
                       ['Park Now', 'Request Shuttle']]
        update.message.reply_text("Choose the PARK NOW from the option below to book your parking bay.",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def plate_reg (bot, update):
    text = update.message.text
    print text
    update.message.reply_text('I see! You have entered {}. Looking around the parking bay for empty slots'.format(text))

    if empty_bay == 0:
        bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADTAADVSx4C1Euf8V7S5s0Ag")
        update.message.reply_text("I'm sorry, there is no empty bay at the moment")

    else:
        bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADUgADVSx4C_ct_Y9DLB4zAg")
        update.message.reply_text("Good news there is an empty bay at Zone Kelab Kilat")


    update.message.reply_text("Thank you, have a nice day!", one_time_keyboard=True)

    return ConversationHandler.END


def req_shuttle(bot, update):
    bot.sendSticker(chat_id=update.message.chat_id, sticker="CAADAgADOgADVSx4C7RBZBTJ4211Ag")
    update.message.reply_text("A shuttle is on its way now.. See you soon!")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("332897518:AAFHfHR1Zyh5FkLhY8z8N1kKk869SbaS7jU")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[RegexHandler('^(Park Now)$', start_reg)],

        states={
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],

            NUM_PLATE: [MessageHandler(Filters.text, plate_reg)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]


        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("start", start_park))
    dp.add_handler(RegexHandler('^(Peekaboo)$', peekaboo))
    dp.add_handler(RegexHandler('^(Bays Left)$', bays_left))
    dp.add_handler(RegexHandler('^(Request Shuttle)$', req_shuttle))
    # dp.add_handler(RegexHandler('^(Park Now)$', start_reg))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()