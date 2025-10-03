import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------------------
# Game Data
# ---------------------------
quests = {
    1: {
        "story": "🌱 **Level 1: Village of Variables**\n"
                 "The elder says: 'We need magical containers to store our resources!'",
        "challenge": "Declare variables: int gold = 100; float health = 75.5; char potion = 'H';",
        "answers": ["int gold = 100;", "float health = 75.5;", "char potion = 'H';"],
        "reward": "🎒 You gained an **Inventory Bag** (Variables Unlocked)"
    },
    2: {
        "story": "🌲 **Level 2: Forest of Decisions**\n"
                 "A guard blocks your way. Choose wisely, adventurer!",
        "challenge": "Write an if-statement where if gold > 50, you print 'You bribe the guard.'",
        "answers": ['if (gold > 50) { printf("You bribe the guard.\\n"); }'],
        "reward": "⚖️ You unlocked **Decision-Making Power**"
    },
    3: {
        "story": "⛏ **Level 3: Looping Mines**\n"
                 "You must mine 5 crystals by repeating actions.",
        "challenge": "Write a for-loop that prints 'Crystal mined!' 5 times.",
        "answers": ['for (int i = 0; i < 5; i++) { printf("Crystal mined!\\n"); }'],
        "reward": "🔄 You unlocked **Grinding Power** (Loops)"
    },
    4: {
        "story": "🏰 **Level 4: Dungeon of Functions**\n"
                 "You face endless monsters. Only reusable spells (functions) can save you.",
        "challenge": "Write a function called attack() that prints 'You strike the monster!'",
        "answers": ['void attack() { printf("You strike the monster!\\n"); }'],
        "reward": "✨ You unlocked **Spellcasting** (Functions)"
    },
    5: {
        "story": "⛰ **Level 5: Memory Mountains**\n"
                 "Memory leaks plague the land. Master Pointers to survive.\n"
                 "⚠️ Beware the Segfault Dragon!",
        "challenge": "Declare an int pointer p, assign it memory with malloc, and free it.",
        "answers": ["int *p = malloc(sizeof(int)); free(p);"],
        "reward": "🧙 You became a **Pointer Wizard**"
    },
    6: {
        "story": "👑 **Final Boss: The Dark Overlord (Bugs)**\n"
                 "Build your hero army with structs and save them in a file!",
        "challenge": "Create a struct Hero with name[20], int health, int attack. "
                     "Then save one hero to a file 'heroes.txt'.",
        "answers": ["struct Hero { char name[20]; int health; int attack; };"],
        "reward": "🏆 You defeated the Dark Overlord and became **Master of C**!"
    }
}

# Track player stats
players = {}

# ---------------------------
# Handlers
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    players[user_id] = {"level": 1, "xp": 0}
    await update.message.reply_text(
        "⚔️ Welcome, brave adventurer, to the Kingdom of C!\n"
        "Type /quest to begin your journey."
    )

async def quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)

    if not player:
        await update.message.reply_text("Type /start to begin your adventure.")
        return

    level = player["level"]
    quest_data = quests.get(level)

    if not quest_data:
        await update.message.reply_text("🎉 You’ve completed all quests! More will come soon...")
        return

    reply = f"{quest_data['story']}\n\n📝 Challenge:\n{quest_data['challenge']}"
    await update.message.reply_text(reply)

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)

    if not player:
        await update.message.reply_text("Type /start to begin your adventure.")
        return

    level = player["level"]
    quest_data = quests.get(level)

    if not quest_data:
        await update.message.reply_text("🎉 You are already a Master of C!")
        return

    user_answer = update.message.text.strip()

    if any(ans in user_answer for ans in quest_data['answers']):
        player["level"] += 1
        player["xp"] += 50
        await update.message.reply_text(
            f"✅ Correct! You gain 50 XP.\n{quest_data['reward']}\n"
            f"⭐ Current XP: {player['xp']}\n"
            f"Type /quest for the next challenge."
        )
    else:
        await update.message.reply_text("❌ Wrong incantation. Try again, hero!")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = players.get(user_id)

    if not player:
        await update.message.reply_text("Type /start to begin your adventure.")
        return

    await update.message.reply_text(
        f"📜 Your Stats:\n"
        f"Level: {player['level']}\n"
        f"XP: {player['xp']}"
    )

# ---------------------------
# Main
# ---------------------------
def main():
    TOKEN = os.getenv("BOT_TOKEN")  # Set in Render environment variables
    PORT = int(os.getenv("PORT", 8080))  # Render gives a PORT dynamically
    APP_URL = os.getenv("RENDER_EXTERNAL_URL")  # Auto-detected Render URL

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quest", quest))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    print("🤖 Bot running with webhook...")

    # Run webhook instead of polling
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{APP_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
