from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to FB Auto Like & Comment Bot!\n\nSend your Facebook Cookie:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_data:
        user_data[user_id] = {"cookie": None, "post_link": None, "comment": None}

    if not user_data[user_id]["cookie"]:
        user_data[user_id]["cookie"] = text
        await update.message.reply_text("Now send the Facebook Post Link:")
    elif not user_data[user_id]["post_link"]:
        user_data[user_id]["post_link"] = text
        await update.message.reply_text("Now send your comment text:")
    elif not user_data[user_id]["comment"]:
        user_data[user_id]["comment"] = text

        cookie = user_data[user_id]["cookie"]
        post_link = user_data[user_id]["post_link"]
        comment_text = user_data[user_id]["comment"]

        try:
            post_id = post_link.split("posts/")[1].split("/")[0]
        except:
            await update.message.reply_text("❌ Invalid Post Link. Try again.")
            user_data.pop(user_id)
            return

        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0"
        }

        like_url = f"https://mbasic.facebook.com/ufi/reaction/?ft_ent_identifier={post_id}"
        comment_url = f"https://mbasic.facebook.com/a/comment.php?ft_ent_identifier={post_id}"

        like_res = requests.get(like_url, headers=headers)
        comment_res = requests.post(comment_url, data={"comment_text": comment_text}, headers=headers)

        if like_res.status_code == 200 and comment_res.status_code == 200:
            await update.message.reply_text("✅ Liked and Commented Successfully!")
        else:
            await update.message.reply_text("❌ Failed! Make sure your cookie and link are valid.")

        user_data.pop(user_id)

app = ApplicationBuilder().token("8024793958:AAFGQ6RqC_3t3pOvgj3e2-fATurTh2Empns").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
