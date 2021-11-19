from flask import Flask
import json, nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from flaskext.mysql import MySQL
from nltk.tokenize import word_tokenize 

# app = Flask(__name__)
mysql = MySQL()
app = Flask(__name__, template_folder='templates')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'telegram_scam_v1_db'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 8889

mysql.init_app(app)
conn = mysql.connect()

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
# open json from telegram
f = open('telegram.json',)
jsonData =  json.load(f)
# stop word
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

count = 1

for i in jsonData['messages']:
    if i['type'] == 'message':
        # init variabel text
        text = str(i['text'])
        # text to lowercase
        lowerCase = text.lower()
        stemming = stemmer.stem(lowerCase)
        # stopword removal
        stopWord = stopword.remove(stemming)
        count = count + 1
        textStemming =  str(count) + '. ' + stemming
        textStopWord =  str(count) + '. ' + stopWord
        textTokenizing = str(count) + '. ' + str(word_tokenize(stopWord))
        
        print(textStemming)
        print(textStopWord)
        print(textTokenizing)
            
if __name__ == '__main__':
    app.run()
    
# pseudocode
# if text != null:
#     if text tidak berisi kata yang hanya satu huruf , ex: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
#         if text tidak berisi kata singkatan ketika chat, ex: sy, sya, km, kmu
#         else:
#         convert kata ke bentuk asli, ex: sya -> saya, km-> kamu
#    else:
#    hapus kata yang berisi satu character   

