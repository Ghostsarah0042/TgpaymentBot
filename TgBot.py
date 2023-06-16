import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, ContextTypes
from replit import db

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(_name_)

# Conversation states
CREATE_ACCOUNT_EMAIL, CREATE_ACCOUNT_PASSWORD, LOGIN_EMAIL, LOGIN_PASSWORD = range(4)

# Flag to track login status
logged_in = False

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    if logged_in:
        msg = (
            "Use /select_plan to list the available checkouts.\n"
            "Use /withdrawal to initiate a withdrawal.\n"
            "Use /open_ticket to open a support ticket."
        )
    else:
        msg = (
            "Use /create_account to create a new account.\n"
            "Use /login to log in to your account."
        )
    await update.message.reply_text(msg)

async def create_account_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the create account process and asks for the user's email."""
    await update.message.reply_text("Please provide your email.")
    return CREATE_ACCOUNT_EMAIL

async def create_account_email_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's email and asks for the password."""
    email = update.message.text
    context.user_data["email"] = email
    await update.message.reply_text("Please provide your password.")
    return CREATE_ACCOUNT_PASSWORD

async def create_account_password_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's password and asks for the verification code."""
    password = update.message.text
    context.user_data["password"] = password
    await update.message.reply_text("Please provide the verification code.")

    # Store the email and password in the database
    db["email"] = email
    db["password"] = password

    return ConversationHandler.END

async def login_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the login process and asks for the user's email."""
    await update.message.reply_text("Please enter your email to login.")
    return LOGIN_EMAIL

async def login_email_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's email and asks for the password."""
    email = update.message.text
    context.user_data["login_email"] = email
    await update.message.reply_text("Please enter your password.")
    return LOGIN_PASSWORD

async def login_password_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validates the login credentials and prints the login status."""
    email = context.user_data.get("login_email")
    password = update.message.text

    # Check if the email and password match the stored account details
    stored_email = db.get("email")
    stored_password = db.get("password")

    if email == stored_email and password == stored_password:
        await update.message.reply_text("Login successful!")
    else:
        await update.message.reply_text("Invalid login credentials.")

    return ConversationHandler.END

async def select_plan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists the available checkouts for selecting a plan and provides the description and URL."""
    # Fetch the available checkouts from your system or API
    checkouts = [
        {
            "name": "Hudson Rivers Starter Trading Bot",
            "description": "The Hudson Rivers trading bot provides integrated solutions for making trades smooth for you. This bot makes it possible to get returns of up to 1.475% interest daily",
            "url": "https://cutt.ly/4ww4KvAj"
        },
        {
            "name": "Hudson Rivers Advanced Trading Bot",
            "description": "The Hudson Rivers advanced trading bot provides integrated solutions for making trades smooth for you. This bot makes it possible to get returns of up to 2.55% interest daily from potential market",
            "url": "https://cutt.ly/qww4Vqna"
        },
        {
            "name": "Hudson Rivers Professional Trading Bot",
            "description": "The Hudson Rivers professional trading bot provides integrated solutions for making trades smooth for you. This bot makes it possible to get returns of up to 6.575% interest weekly from the market",
            "url": "https://cutt.ly/Bww47YgQ"
        }
    ]

    # Generate a formatted list of checkouts with their descriptions and URLs
    checkout_list = "\n\n".join([f"{i + 1}. {c['name']}:\n{c['description']}\nURL: {c['url']}\n" for i, c in enumerate(checkouts)])

    # Send the checkout list to the user
    await update.message.reply_text(f"Available checkouts:\n\n{checkout_list}")

async def withdrawal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initiates a withdrawal by asking for wallet and verification pin."""
    await update.message.reply_text("Please provide your wallet and verification pin.")

async def open_ticket_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Opens a support ticket by sending a message to the admin."""
    admin_chat_id = "6008082458"  # Replace with the actual admin chat ID
    await context.bot.send_message(admin_chat_id, "Please open a support ticket @Dougborden01.")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5977373456:AAH8gz-xbuWGRwJ8C2I3zvkp0IQ48Gzy6fM").build()

    # Add command handler for start
    application.add_handler(CommandHandler("start", start_callback))

    # Add command handler for create_account
    application.add_handler(CommandHandler("create_account", create_account_start_callback))

    # Add command handler for login
    application.add_handler(CommandHandler("login", login_start_callback))

    # Add command handler for select_plan
    application.add_handler(CommandHandler("select_plan", select_plan_callback))

    # Add command handler for withdrawal
    application.add_handler(CommandHandler("withdrawal", withdrawal_callback))

    # Add command handler for open_ticket
    application.add_handler(CommandHandler("open_ticket", open_ticket_callback))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if _name_ == "_main_":
    main()
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
