
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from config import Config
from config import IS_ADMIN_TEST
#  load Variables

# Define the paths to the files
PDF_FILE_PATH = r"resources/documents/Ammar General Panner.pdf"  # 
PDF_FILE_PATH2 = r"resources/documents/Ammar Solar Panner.pdf"  # 
IMAGE_FILE_PATH = r"resources/images/Ammar General Panner.jpg"
IMAGE_FILE_PATH2 = r"resources/images/Ammar Solar Panner.jpg"
CONTACTS_FILE_PATH = r"resources/contacts."  # 
testPath = r"D:\TelegramShopBot\app\resources\numbers\Contacts.vcf"

ADMIN_USER_ID = Config.ADMIN_USER_ID
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id == int(ADMIN_USER_ID) and IS_ADMIN_TEST:
        await update.message.reply_text("Welcome, Admin!")
    else:
        # Define the inline keyboard layout
        keyboard = [
        # First row with "موقعنا" and "حمل كرتنا" buttons
       [
            InlineKeyboardButton("📍 موقعنا",    callback_data="our_location"),
            InlineKeyboardButton("📄 حمل كرتنا", callback_data="download_pdf")
            ],
        # Second row with "تصفح الأن" button linking to a web app
            [
            InlineKeyboardButton("⚙️ تصفح الأن", web_app={"url": "https://Modroid.pythonanywhere.com"})
            ]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
         # Send a welcome message with the inline keyboard attached
        await update.message.reply_text("مرحبا بك في عمار الهندسية .\nاختر وتصفح حلولنا الهندسية.", reply_markup=reply_markup)

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the callback data from the button click
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    # Check which button was pressed
    if query.data == "our_location":
        # Send a predefined location (coordinates for Ammar's shop)
        latitude, longitude = 15.458248965687313, 36.39670325301276
        #await query.message.reply_text()
        await context.bot.send_location(chat_id=query.message.chat_id, latitude=latitude, longitude=longitude)
        await query.message.reply_text("هذا هو موقعنا على الخريطة.")

    elif query.data == "download_pdf":
        # Send the PDF file
        if os.path.exists(testPath):
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(testPath, 'rb'))
            await query.message.reply_text("تم تحميل الكرت بنجاح!")
        else:
            await query.message.reply_text("عذرًا، لم يتم العثور على الملف.")

def main() -> None:
    # Initialize the bot application
    application = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()

    # Add handlers for the /start command and button clicks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button_click))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()

