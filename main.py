from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from text_to_speech import convert
from chatGPT import talk_to_chatGPT
from credentials import telegramTOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args)
    await convert(text)
    await update.message.reply_audio(audio='msg.mp3')


async def hanger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        rf"Привет,сейчас ты сыграешь в игру виселица",
        rf"Введите одну букву:"
    )

async def chatGPT(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = ' '.join(context.args)
    answer = await talk_to_chatGPT(text)
    await update.message.reply_text(answer) 


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:

    application = Application.builder().token(telegramTOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("to_speech", to_speech))
    application.add_handler(CommandHandler("hangman", hanger))
    application.add_handler(CommandHandler("chatGPT", chatGPT))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()
