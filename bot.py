from keep_alive import keep_alive
keep_alive()

import os
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, InlineQueryHandler, CommandHandler
from youtube_search_python import VideosSearch
from uuid import uuid4
from downloader import download_video_or_audio

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("I'm alive! Use me inline by typing @YourBotName + video name.")

async def inline_query(update, context):
    query = update.inline_query.query
    if not query:
        return

    videosSearch = VideosSearch(query, limit=5)
    results = videosSearch.result()["result"]

    articles = []
    for video in results:
        title = video["title"]
        url = video["link"]

        articles.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=title,
                input_message_content=InputTextMessageContent(f"Downloading: {title}\n{url}"),
                description="Click to choose format...",
            )
        )

    await update.inline_query.answer(articles)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(InlineQueryHandler(inline_query))

app.run_polling()
