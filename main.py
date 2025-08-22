# ------------------ KEEP ALIVE ------------------
from flask import Flask
from threading import Thread
import os

app = Flask("")

@app.route("/")
def home():
    return "Bot attivo!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ------------------ BOT TELEGRAM ------------------
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)

# --- CIFRATURA SPECIALE ---
alfabeto = "abcdefghijklmnopqrstuvwxyz"

def cifra(testo: str) -> str:
    testo = testo.lower()
    risultato = []
    for parola in testo.split(" "):
        cifrata_parola = ""
        for char in parola:
            if char == "!":
                cifrata_parola += "!!!"
            elif char in alfabeto:
                pos = alfabeto.index(char) + 1
                num = pos / 2
                num_str = str(int(num)) if num.is_integer() else str(num)
                if pos >= 10:
                    cifrata_parola += f"{num_str}•"
                else:
                    cifrata_parola += num_str
            else:
                cifrata_parola += char
        risultato.append(cifrata_parola)
    return "!".join(risultato)

def decifra(testo: str) -> str:
    parole = testo.split("!")
    risultato = []
    for parola in parole:
        i = 0
        parola_decifrata = ""
        while i < len(parola):
            if parola[i:i+3] == "!!!":
                parola_decifrata += "!"
                i += 3
                continue
            num_str = ""
            while i < len(parola) and (parola[i].isdigit() or parola[i] == "." or parola[i] == "•"):
                num_str += parola[i]
                i += 1
            if num_str:
                if num_str[-1] == "•":
                    num = float(num_str[:-1])
                    pos = int(num * 2)
                else:
                    num = float(num_str)
                    pos = int(num * 2)
                parola_decifrata += alfabeto[pos - 1]
            else:
                parola_decifrata += parola[i]
                i += 1
        risultato.append(parola_decifrata)
    return " ".join(risultato)

# --- HANDLER TELEGRAM ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Sono il tuo bot cifrario 🔐\n"
        "Usa /cifra <testo> per cifrare\n"
        "Usa /decifra <testo> per decifrare"
    )

async def handle_cifra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        testo = " ".join(context.args)
        await update.message.reply_text(cifra(testo))
    else:
        await update.message.reply_text("Devi scrivere un messaggio dopo /cifra")

async def handle_decifra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        testo = " ".join(context.args)
        await update.message.reply_text(decifra(testo))
    else:
        await update.message.reply_text("Devi scrivere un messaggio dopo /decifra")

# --- MAIN ---
if __name__ == "__main__":
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("cifra", handle_cifra))
    app_bot.add_handler(CommandHandler("decifra", handle_decifra))

    app_bot.run_polling()



