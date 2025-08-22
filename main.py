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
from telegram.ext import Updater, CommandHandler
import logging

# --- CIFRATURA SPECIALE ---
alfabeto = "abcdefghijklmnopqrstuvwxyz"

def cifra(testo):
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

def decifra(testo):
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

# --- TELEGRAM BOT ---
logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("8251352657:AAH5XXTjxvD3tR7_9sentuCE4nJj86tL-KI")  # Legge il token dalle variabili d'ambiente

def start(update, context):
    update.message.reply_text(
        "Ciao! Sono il tuo bot cifrario 🔐\n"
        "Usa /cifra <testo> per cifrare\n"
        "Usa /decifra <testo> per decifrare"
    )

def handle_cifra(update, context):
    if context.args:
        testo = " ".join(context.args)
        update.message.reply_text(cifra(testo))
    else:
        update.message.reply_text("Devi scrivere un messaggio dopo /cifra")

def handle_decifra(update, context):
    if context.args:
        testo = " ".join(context.args)
        update.message.reply_text(decifra(testo))
    else:
        update.message.reply_text("Devi scrivere un messaggio dopo /decifra")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cifra", handle_cifra))
    dp.add_handler(CommandHandler("decifra", handle_decifra))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
