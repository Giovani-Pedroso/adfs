import cv2
import os
import numpy as np
from PIL import Image
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from pyzbar.pyzbar import decode, ZBarSymbol
from pdf2image import convert_from_path, convert_from_bytes
import tempfile
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('TOKEN_TELEGRAM')

# Commands
async def start_command(update, context):
    await update.message.reply_text("Voce iniciou o bot")

async def help_command(update, context):
    await update.message.reply_text("E assim que o robo funciona")

async def test_command(update, context):
    await update.message.reply_text("comando de tesxt")

# responses
def handle_respnse(text):
    processed = text.lower()

    if 'hello' in processed:
        return "hey ther"

    if 'how are you' in processed:
        return "I am good"

    return 'I do not understand'


# async def handle_message(update,context ):
async def handle_message(update, context):
    message_type = update.message.chat.type

    print("info of the message")
    print(update.message)

    text = update.message.text

    print(f'n\ User ({update.message.chat.id}) in {message_type}: {text}\n')

    response = handle_message(text)
    print(f'Ther response is {response}')

    await update.message.reply_text(response)

async def error(update, context):
    print(f'\n\n--------------------------------------------------------\n\n')
    print(f'Update {update}')
    print(f' caused error {context.error}')

async def photo_handler(update, context):
    print("aphoto was sent")
    await update.message.reply_text("image recievied")

    print (update.message.photo[-1].file_id)

    #Pega o id da imagem com a maior resolucao
    file_id = update.message.photo[-1].file_id

    #Se remover a linha abaixo o codigo para de funcionar
    print (type(update.message.photo))

    file = await context.bot.getFile(file_id)
    await file.download_to_drive('./tmp/boleto.jpg')


async def document_handler(update, context):
    file_id = update.message.document.file_id
    print("a PDF was sent")
    await update.message.reply_text("PDF recievied")
    file = await context.bot.getFile(file_id)
    await file.download_to_drive('./tmp/boleto.pdf')

if __name__ == '__main__':
    print("The bot is running")
    app = Application.builder().token(BOT_TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('test', test_command))
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Images
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    #Documents
    app.add_handler(MessageHandler(filters.Document.PDF, document_handler))
    
    #Erros
    app.add_error_handler(error)
    print('Polling...')
    app.run_polling(poll_interval=1)




# img = Image.open('./imgs/bank.png')
# img = Image.open('./imgs/barTest.png')
# decoded_list = decode(img)
# print(decoded_list)

# img = cv2.imread('./imgs/bank.png')
# img2 = cv2.imread('./imgs/barTest.png')

# bd = cv2.barcode.BarcodeDetector()

# print(bd.detectAndDecode(img))
# print(bd.detectAndDecode(img2))

# images = convert_from_path('/home/belval/example.pdf')
# img = cv2.imread('./imgs/boleto_qr_3.jpg')
# img = cv2.imread('./imgs/boleto_qr_4.jpg')
# img = cv2.imread('./imgs/bar1.jpg')
# img = cv2.imread('./imgs/bar2.png')

# img = cv2.imread('./imgs/boleto_qr_1.jpg')
# bd = cv2.barcode.BarcodeDetector()

# qcd = cv2.QRCodeDetector()

# retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
# retval_bar, decoded_info_bar,  points_bar = bd.detectAndDecode(img)
# # retval, decoded_info, decoded_type  = bd.detectAndDecode(img)
# print(bd.detectAndDecode(img))

# print("There is some qr codes: ")
# print(retval)
# print("There is some barcodes: ")
# print(retval_bar)
# print(decoded_info)
