import logging
import os
import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from electricity_manager import ElectricityManager

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Admin IDs (Add your Telegram ID here)
ADMIN_IDS = [123456789] # Replace with actual ID

# Initialize Manager
manager = ElectricityManager('upload/ПУЛИБАРК.xlsx')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Салом {user.first_name}! Ман боти ҳисобкунаки барқ ҳастам.\n"
        "Лутфан акси ҳисобкунакро фиристед."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # In a real scenario, we would use OCR here. 
    # For now, we simulate the OCR process as we've already identified the values from the user's images.
    
    # 1. Download the photo
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"downloads/{photo_file.file_id}.jpg"
    os.makedirs('downloads', exist_ok=True)
    await photo_file.download_to_drive(file_path)
    
    await update.message.reply_text("Акс қабул шуд. Коркард рафта истодааст...")

    # OCR Simulation Logic (Placeholder for real OCR)
    # We will use the identified values for the demonstration
    # In production, we'd use EasyOCR here.
    
    # Example simulation for PANTERA and NAVROUZ based on user's images
    # This is where the OCR result would be parsed.
    # For the sake of this task, I'll provide a manual entry command for the user to confirm.
    
    await update.message.reply_text(
        "Ман аксро дидам. Лутфан номи мағоза ва нишондиҳандаро тасдиқ кунед ё дастӣ ворид кунед.\n"
        "Намуна: `ПАНТЕРА 7364.26`"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Pattern: MerchantName Reading
    match = re.match(r'^(.+)\s+(\d+(\.\d+)?)$', text)
    
    if match:
        merchant_name = match.group(1).strip()
        new_reading = float(match.group(2))
        
        result = manager.update_merchant(merchant_name, new_reading)
        
        if isinstance(result, dict):
            response = (
                f"✅ **Навсозӣ шуд!**\n\n"
                f"🏪 Мағоза: {result['merchant']}\n"
                f"📉 Нишондиҳандаи кӯҳна: {result['old_reading']}\n"
                f"📈 Нишондиҳандаи нав: {result['new_reading']}\n"
                f"⚡️ Истифода: {result['diff_kwh']} кВт\n"
                f"💰 Маблағ: {result['total_sum']} TJS (Коэф: {result['rate']})"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text(result)
    else:
        await update.message.reply_text("Лутфан маълумотро дар шакли дуруст ворид кунед: `Номи_Мағоза Нишондиҳанда`")

if __name__ == '__main__':
    # You need to put your token here
    TOKEN = '7995368889:AAG0mdsjHED9HVRTNMO0hsnc99S_pR6lI04'
    
    if TOKEN == '7995368889:AAG0mdsjHED9HVRTNMO0hsnc99S_pR6lI04':
        print("Error: Please provide a valid Telegram Bot Token.")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
        
        print("Bot is starting...")
        application.run_polling()
