import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from coinbase_commerce import Client

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Coinbase Commerce API configuration
COINBASE_COMMERCE_API_KEY = 'YOUR API KEY'
coinbase_client = Client(api_key=COINBASE_COMMERCE_API_KEY)

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = 'YOUR BOT TOKEN'


def start(update: Update, context: CallbackContext):
    """Handler for the /start command."""
    chat_id = update.effective_chat.id
    text = "Welcome to the Coinbase Commerce payment bot!\n\nUse the /checkout command to initiate a payment."
    context.bot.send_message(chat_id=chat_id, text=text)


def list_checkouts(update: Update, context: CallbackContext):
    """Handler for the /list_checkouts command."""
    chat_id = update.effective_chat.id

    try:
        checkouts = coinbase_client.checkout.list(limit=5)

        if not checkouts:
            context.bot.send_message(chat_id=chat_id, text="No checkouts found.")
            return

        for checkout in checkouts.data:
            text = f"Checkout ID: {checkout.id}\n\nDescription: {checkout.description}"
            context.bot.send_photo(chat_id=chat_id, photo=checkout.logo_url, caption=text)

    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f'Error: {str(e)}')


def checkout(update: Update, context: CallbackContext):
    """Handler for the /checkout command."""
    chat_id = update.effective_chat.id

    try:
        # Create a new charge
        charge_data = {
            'name': 'Test Product',
            'description': 'Sample product description',
            'local_price': {
                'amount': '10.0',
                'currency': 'USD'
            },
            'pricing_type': 'fixed_price'
        }

        charge = coinbase_client.charge.create(**charge_data)
        payment_url = charge['hosted_url']

        # Create the payment button
        button_text = f'Pay {charge["pricing"]["local"]["amount"]} {charge["pricing"]["local"]["currency"]}'
        button = InlineKeyboardButton(text=button_text, url=payment_url)
        keyboard = InlineKeyboardMarkup([[button]])

        context.bot.send_message(chat_id=chat_id, text='Click the button below to make a payment:', reply_markup=keyboard)

    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f'Error: {str(e)}')


def main():
    # Create the Telegram bot updater and dispatcher
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add the command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list_checkouts", list_checkouts))
    dispatcher.add_handler(CommandHandler("checkout", checkout))

    # Start the bot
    updater.start_polling()
    logging.info("Bot started.")


if name == '__main__':
    main()
