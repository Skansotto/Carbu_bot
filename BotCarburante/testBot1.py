import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"{TG_VER} versione non compatibile."
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TIPO, CARBURANTE, CAPACITA, MAXKM = range(4)

tastieraTipo = [["Auto", "Moto"]]
tastieraCaburante = [["Benzina", "Diesel", "Metano"]]
tastieraCapacita = [["10", "20", "30", "40", "50"]]
tastieraMaxkm = [["5", "10", "20", "40", "50"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # avvia il bot
        user = update.message.from_user

        await update.message.reply_text(
            f"Ciao " + user.username + " sono CarbuBot, il tuo assistente personale per la scelta della migliore stazione di rifornimento per il tuo veicolo.\n\n"
            "Invia /cancel per smettere di parlare con me.\n\n"

            "Che veicolo vuoi registrare?",

            reply_markup=ReplyKeyboardMarkup(
                tastieraTipo, one_time_keyboard=True, input_field_placeholder="Seleziona il tipo di veicolo:"
            ),
        )
        # user = update.message.from_user
        # await update.message.reply_text(f"Ciao{user}")
        return CARBURANTE


async def carburante(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    print("ehi" + user)

    await update.message.reply_text(
        "Che tipo di carburante utilizza?",

        reply_markup=ReplyKeyboardMarkup(
            tastieraCaburante, one_time_keyboard=True, input_field_placeholder="Seleziona il tipo di carburante:"
        ),
    )

    return CAPACITA


async def capacita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user

    await update.message.reply_text(
        "Qual'è la capacità del serbatoio approssimata in litri?",

        reply_markup=ReplyKeyboardMarkup(
            tastieraCapacita, one_time_keyboard=True, input_field_placeholder="Seleziona la capacità del tuo serbatoio:"
        ),
    )

    return MAXKM


async def maxkm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user

    await update.message.reply_text(
        "Quanti chilometri sei disposto a fare per fare rifornimento?",

        reply_markup=ReplyKeyboardMarkup(
            tastieraMaxkm, one_time_keyboard=True, input_field_placeholder="Seleziona i km che sei disposto a fare:"
        ),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user

    logger.info("L'utente %s ha chiuso la conversazione.", user.first_name)
    await update.message.reply_text(
        "Arrivederci!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Instanzio e passo il token
    application = Application.builder().token(
        "6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CARBURANTE: [MessageHandler(filters.Regex("^(Benzina|Diesel|Metano)$"), carburante)],
            CAPACITA: [MessageHandler(filters.Regex(r"[0-9]$"), capacita)],
            MAXKM: [MessageHandler(filters.Regex(r"[0-9]$"), maxkm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Il bot è in esecuzione fino ad un Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
