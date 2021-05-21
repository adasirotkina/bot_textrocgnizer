import telebot
import cv2
import pytesseract
import numpy as np
from telebot import types

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Photo:

    def __init__(self, image):
        self.image = image

    def text(self, lang, size = 2):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # creating Binary image by selecting proper threshold
        binary_image = cv2.threshold(gray_image, 130, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Inverting the image
        inverted_bin = cv2.bitwise_not(binary_image)

        inverted_bin_0 = cv2.resize(inverted_bin, (int(inverted_bin.shape[1] * size), int(inverted_bin.shape[0] * size)))
        # Some noise reduction
        kernel = np.ones((2, 2), np.uint8)
        processed_img = cv2.erode(inverted_bin_0, kernel, iterations=1)
        processed_img = cv2.dilate(processed_img, kernel, iterations=1)

        # Applying image_to_string method
        if lang == 'rus':
            text = pytesseract.image_to_string(processed_img, lang='rus')
            return text

        if lang == 'eng':
            text = pytesseract.image_to_string(processed_img, lang='eng')
            return text
        if lang == 'rus+eng':
            text = pytesseract.image_to_string(processed_img, lang='rus+eng')
            return text

bot = telebot.TeleBot('1810169094:AAFPeAWc_-O-AtnMJLbdWXO9-07bqxpPAzM')

bot.remove_webhook()


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Данный бот предназначен для обработки текста с фотографий.'
                                           'Просто отправьте мне снимок и я скажу, что на нем написано.')

@bot.message_handler(content_types=['text', 'audio', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def error(message):
    bot.send_message(message.from_user.id, 'Что-то не то... Я принимаю только фотографии.')

@bot.message_handler(content_types=['document'])
def doc(message):
    bot.send_message(message.from_user.id, 'Это что-то очень похожее на фото, но не оно. Если вы отправляли фото, попробуйте отправить еще раз \t'
                                           'и проверьте, что стоит галочка напротив "Compress image"')



@bot.message_handler(content_types=['photo'])
def get_photo(message):
    global image


    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    image = bot.download_file(file_info.file_path)
    with open("kotikisobachki.jpg", 'wb') as new_file:
        new_file.write(image)

    image = cv2.imread('kotikisobachki.jpg')
    image = Photo(image)

    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_rus = types.InlineKeyboardButton(text='Русский', callback_data='rus');
    keyboard.add(key_rus); #добавляем кнопку в клавиатуру
    key_eng= types.InlineKeyboardButton(text='Английский', callback_data='eng');
    keyboard.add(key_eng);
    key_ruseng = types.InlineKeyboardButton(text='Оба', callback_data='rus+eng');
    keyboard.add(key_ruseng)
    question = 'На каком языке написан текст?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global image
    try:
        if call.data == "rus":
            bot.send_message(call.message.chat.id, image.text('rus'))
        if call.data == "eng": #call.data это callback_data, которую мы указали при объявлении кнопки
            bot.send_message(call.message.chat.id, image.text('eng'))
        if call.data == "rus+eng": #call.data это callback_data, которую мы указали при объявлении кнопки
            bot.send_message(call.message.chat.id, image.text('rus+eng'))
    except:
        try:
            if call.data == "rus":
                bot.send_message(call.message.chat.id, image.text('rus', size = 1.5))
            if call.data == "eng":  # call.data это callback_data, которую мы указали при объявлении кнопки
                bot.send_message(call.message.chat.id, image.text('eng', size = 1.5))
            if call.data == "rus+eng":  # call.data это callback_data, которую мы указали при объявлении кнопки
                bot.send_message(call.message.chat.id, image.text('rus+eng', size = 1.5))
        except:
            try:
                if call.data == "rus":
                    bot.send_message(call.message.chat.id, image.text('rus', size=1))
                if call.data == "eng":  # call.data это callback_data, которую мы указали при объявлении кнопки
                    bot.send_message(call.message.chat.id, image.text('eng', size=1))
                if call.data == "rus+eng":  # call.data это callback_data, которую мы указали при объявлении кнопки
                    bot.send_message(call.message.chat.id, image.text('rus+eng', size=1))
            except:
                try:
                    if call.data == "rus":
                        bot.send_message(call.message.chat.id, image.text('rus', size=0.5))
                    if call.data == "eng":  # call.data это callback_data, которую мы указали при объявлении кнопки
                        bot.send_message(call.message.chat.id, image.text('eng', size=0.5))
                    if call.data == "rus+eng":  # call.data это callback_data, которую мы указали при объявлении кнопки
                        bot.send_message(call.message.chat.id, image.text('rus+eng', size=0.5))
                except:
                    bot.send_message(call.message.chat.id, 'Не могу найти текст :(')





bot.polling(none_stop=True)
