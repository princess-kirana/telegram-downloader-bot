from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "ISI_TOKEN_BOT_KAMU"

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    await update.message.reply_text("Sedang download video...")

    ydl_opts = {'outtmpl': 'video.%(ext)s'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await update.message.reply_video(video=open("video.mp4","rb"))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, download))

app.run_polling()
