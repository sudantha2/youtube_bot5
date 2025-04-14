import logging
import yt_dlp
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext, CallbackQueryHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your bot token
TOKEN = 'YOUR_BOT_TOKEN'  # Replace with your bot token

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Use inline mode to search for YouTube videos.')

def search_youtube(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please provide a search query.')
        return

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)
            results = info_dict['entries']
            results_list = []

            for entry in results[:5]:  # Limit to 5 results
                video_url = entry['url']
                title = entry['title']
                video_id = entry['id']

                # Create inline query results with download options
                results_list.append(InlineQueryResultArticle(
                    id=video_id,
                    title=title,
                    input_message_content=InputTextMessageContent(f"Download options for: {title}"),
                    description="Click to download in various qualities.",
                    thumb_url=entry['thumbnail'],
                    reply_markup={
                        "inline_keyboard": [
                            [
                                {"text": "144p", "callback_data": f"download:{video_url}:144p"},
                                {"text": "360p", "callback_data": f"download:{video_url}:360p"},
                                {"text": "480p", "callback_data": f"download:{video_url}:480p"},
                                {"text": "MP3", "callback_data": f"download:{video_url}:mp3"},
                            ]
                        ]
                    }
                ))

            update.inline_query.answer(results_list)
        except Exception as e:
            update.message.reply_text(f"An error occurred: {str(e)}")

def download_video(update: Update, context: CallbackContext) -> None:
    query = update.callback_query.data
    _, url, quality = query.split(':')

    ydl_opts = {
        'format': quality if quality != 'mp3' else 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if quality == 'mp3' else [],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            update.callback_query.answer('Download completed!')
        except Exception as e:
            update.callback_query.answer(f"An error occurred: {str(e)}")

def main() -> None:
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and inline query handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(InlineQueryHandler(search_youtube))
    dispatcher.add_handler(CallbackQueryHandler(download_video))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
