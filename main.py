import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# --- INLINE BUTTON LAYOUT ---
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📡 Get Signals", callback_data="get_signals")],
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton("⭐ Upgrade", callback_data="upgrade")],
        [InlineKeyboardButton("ℹ Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_menu():
    keyboard = [
        [InlineKeyboardButton("🚀 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🛠 Engine Settings", callback_data="admin_engine")],
        [InlineKeyboardButton("📡 Auto Scanner", callback_data="admin_scanner")],
        [InlineKeyboardButton("👤 Manage Users", callback_data="admin_users")],
    ]
    return InlineKeyboardMarkup(keyboard)


# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    # Normal welcome
    await update.message.reply_text(
        "Hey! 👋\nWelcome to QuantumEdge.\nChoose an option below:",
        reply_markup=main_menu()
    )

    # Admin panel displayed automatically
    if uid in ADMIN_IDS:
        await update.message.reply_text(
            "🛡 Admin Panel:",
            reply_markup=admin_menu()
        )


# --- CALLBACK HANDLER ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    uid = query.from_user.id
    await query.answer()

    # USER BUTTONS
    if data == "get_signals":
        await query.edit_message_text("Fetching signals… 🔄 (feature coming)")
    elif data == "dashboard":
        await query.edit_message_text("Opening dashboard… 🌐 (we’ll link it later)")
    elif data == "upgrade":
        await query.edit_message_text("Premium details coming soon ⭐")
    elif data == "help":
        await query.edit_message_text("Need help? Just ask!")

    # ADMIN BUTTONS
    elif uid in ADMIN_IDS:
        if data == "admin_broadcast":
            await query.edit_message_text("Broadcast panel (coming)")
        elif data == "admin_engine":
            await query.edit_message_text("Engine settings panel (coming)")
        elif data == "admin_scanner":
            await query.edit_message_text("Scanner controls (coming)")
        elif data == "admin_users":
            await query.edit_message_text("User management (coming)")

    else:
        await query.edit_message_text("Access restricted ⚠")


# --- APP LAUNCH ---
def run():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running…")
    app.run_polling()

if __name__ == "__main__":
    run()
