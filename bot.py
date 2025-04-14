from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, InlineQueryHandler, CallbackQueryHandler, ContextTypes
from uuid import uuid4
from config import BOT_TOKEN
from inline_search import search_youtube
from downloader import download_video
import os

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    for video in search_youtube(query):
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=video["title"],
                input_message_content=InputTextMessageContent(f"{video['title']}\n{video['url']}"),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("144p", callback_data=f"dl|{video['url']}|144"),
                        InlineKeyboardButton("360p", callback_data=f"dl|{video['url']}|360"),
                        InlineKeyboardButton("480p", callback_data=f"dl|{video['url']}|480"),
                    ],
                    [
                        InlineKeyboardButton("MP3 128kbps", callback_data=f"dl|{video['url']}|mp3128"),
                        InlineKeyboardButton("MP3 320kbps", callback_data=f"dl|{video['url']}|mp3320"),
                    ]
                ])
            )
        )

    await update.inline_query.answer(results)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, url, quality = query.data.split("|")
    await query.edit_message_text(f"⏬ Downloading `{quality}` from YouTube...", parse_mode="Markdown")

    file_path = download_video(url, quality)

    if quality.startswith("mp3"):
        await query.message.reply_audio(audio=open(file_path, "rb"), title=os.path.basename(file_path))
    else:
        await query.message.reply_video(video=open(file_path, "rb"), caption=os.path.basename(file_path))

    os.remove(file_path)  # Clean up

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
