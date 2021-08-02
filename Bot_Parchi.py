from telegram import *
from telegram.ext import *
import math as m
import psycopg2
import json

def dist(lat1,lon1, lat2, lon2):
    return 6371 * 2 * m.asin(m.sqrt(m.pow(m.sin((m.radians(lat2) - m.radians(lat1)) / 2), 2) + m.cos(lat1) * m.cos(lat2) * m.pow(m.sin((m.radians(lon2) - m.radians(lon1)) / 2), 2)))

def start(update: Update, context: CallbackContext) -> None:
    testo = "Benvenuto!!! \nQuesto bot ti permette di trovare il parco più vicino a te. \nInvia la tua posizione."
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo)

def distanza(update: Update, context: CallbackContext) -> None:
    lat1 = update.message.location.latitude
    lon1 = update.message.location.longitude
    d = []
    for i in range(0,len(coord_x)):
        d.append(dist(lat1,lon1,coord_x[i],coord_y[i]))
    e = d[:]        #uso "e" come copia
    d.sort()
    ind = 0
    for i in range(0,len(d)):
        if d[0]==e[i]:
            ind = i
            break
    testo = "Il parco più vicino è: " + nome[ind]
    testo_dist = "\nDistanza: " + str(round(d[0],2)) + " km"
    testo_via = "\nIndirizzo: " + indirizzo[ind]
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo+testo_dist+testo_via)
    update.message.reply_location(coord_x[ind], coord_y[ind])

def echo(update: Update, context: CallbackContext) -> None:
    testo = "Non è un comando valido"
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo) #update.message.text per leggere il messaggio ricevuto

def main():
    updater = Updater("1915954757:AAGzinL25-jV6A_5olz6KEVxCUxOCGLBsXk")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.location, distanza))    #update.message.reply_location(10,10) metti coordinate del posto e invia

    updater.start_polling()

    updater.idle()

con = psycopg2.connect(
    host="127.0.0.1",       #192.168.20.20 IP locale
    database="geoapp",
    user="postgres",
    password="postgres"
)

cur = con.cursor()
v = []
coord_x = []
coord_y = []
nome = []
indirizzo = []

cur.execute("select ST_AsGeoJSON(geom) from parchipunti")    #ricava coordinate in GeoJSON
a = cur.fetchall()
cur.execute("select denominazi from parchipunti")    #ricava coordinate in GeoJSON
b = cur.fetchall()
cur.execute("select nome_via from parchipunti")    #ricava coordinate in GeoJSON
c = cur.fetchall()
for i in range(0,len(a)):
    v.append(json.loads(a[i][0]))
    coord_x.append(v[i]['coordinates'][1])
    coord_y.append(v[i]['coordinates'][0])
    nome.append(b[i][0])
    indirizzo.append(c[i][0])
cur.close()
con.close()
main()
