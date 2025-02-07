from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont

# Bot setup
bot_token = "7675190882:AAEa_jt4CW0cppTcMb24SpGricwZ8wU2AMY"  # Replace with your bot token
font_path = "C:/Users/User/Downloads/NotoSansEgyptianHieroglyphs-Regular (4).ttf"  # Correct font path
font_size = 70  # Font size

# English to Hieroglyphic mapping (using real hieroglyphic Unicode characters)
english_to_hieroglyphs = {
    "a": "𓀀", "b": "𓃀", "c": "𓍿", "d": "𓂧", "e": "𓇋",
    "f": "𓆑", "g": "𓎼", "h": "𓉔", "i": "𓇋", "j": "𓊃",
    "k": "𓎡", "l": "𓃭", "m": "𓅓", "n": "𓈖", "o": "𓅱",
    "p": "𓊪", "q": "𓏘", "r": "𓂋", "s": "𓋴", "t": "𓏏",
    "u": "𓅱", "v": "𓆑", "w": "𓅱", "x": "𓐍", "y": "𓇋", "z": "𓊃",
    " ": " "  # Preserve spaces
}

# Function to convert English text to Hieroglyphs
def convert_to_hieroglyphs(text):
    hieroglyphs = "".join(english_to_hieroglyphs.get(char.lower(), "") for char in text)
    return hieroglyphs

# Function to create the image
def create_image(text):
    image_width = 800
    image_height = 150
    background_color = "black"
    text_color = "white"

    # Create a blank image
    image = Image.new("RGB", (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # Load the font
    try:
        font = ImageFont.truetype(font_path, size=font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return None

    # Calculate text position using textbbox
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)  # Get text bounding box
        text_width = text_bbox[2] - text_bbox[0]  # Calculate text width
        text_height = text_bbox[3] - text_bbox[1]  # Calculate text height
        text_x = (image_width - text_width) // 2  # Center text horizontally
        text_y = (image_height - text_height) // 2  # Center text vertically
    except Exception as e:
        print(f"Error calculating text dimensions: {e}")
        return None

    # Draw the text on the image
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Save the image
    image_path = "hieroglyphs.png"
    image.save(image_path)
    print(f"Image created and saved at: {image_path}")
    return image_path

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send any English text, and I will convert it to hieroglyphs.")

# Message handler for text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text  # Get the user's message
    hieroglyphs_text = convert_to_hieroglyphs(user_text)  # Convert to hieroglyphs
    image_path = create_image(hieroglyphs_text)  # Create the image

    if image_path:
        # Send the image
        chat_id = update.message.chat_id
        await context.bot.send_photo(chat_id=chat_id, photo=open(image_path, "rb"))
        await update.message.reply_text("Here is your text in hieroglyphs!")
    else:
        await update.message.reply_text("Failed to create the image.")

# Main function to run the bot
def main():
    # Create the application
    application = Application.builder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()