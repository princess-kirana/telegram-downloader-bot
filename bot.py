import telebot
import yt_dlp
import os

# Mengambil token dari brankas server, JANGAN tulis token aslimu di sini ya!
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Kirimkan link video (YouTube/TikTok/IG), dan aku akan mengunduhnya untukmu. 🎥")

@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text
    msg_proses = bot.reply_to(message, "⏳ Sedang memproses link... Mohon tunggu sebentar.")

    ydl_opts = {
        'format': 'best[filesize<50M][ext=mp4]/best',
        'outtmpl': 'video_unduhan.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            bot.edit_message_text("⬇️ Sedang mengunduh video...", chat_id=message.chat.id, message_id=msg_proses.message_id)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.edit_message_text("⬆️ Sedang mengirim video ke Telegram...", chat_id=message.chat.id, message_id=msg_proses.message_id)
        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, reply_to_message_id=message.message_id)

        bot.delete_message(message.chat.id, msg_proses.message_id)
        os.remove(filename)

    except Exception as e:
        bot.edit_message_text("❌ Gagal! Pastikan link benar atau ukuran video tidak lebih dari 50MB.", chat_id=message.chat.id, message_id=msg_proses.message_id)
        print(f"Error: {e}")

print("Bot siap dijalankan di server...")
bot.infinity_polling()
