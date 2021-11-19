from flask import Flask
import json, re, sys, demoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from flaskext.mysql import MySQL
from strsimpy.levenshtein import Levenshtein

# app = Flask(__name__)
mysql = MySQL()
app = Flask(__name__)

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
# check similarity
levenshtein = Levenshtein()
# init count
count = 0

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

# looping from json for text processing
for i in jsonData['messages']:
    if i['type'] == 'message':
        # init variabel text
        text = str(i['text'])
        # text to lowercase
        lowerCase = text.lower()
        # # remove /n
        # replaceEnter = lowerCase.replace('/n', '') 
        # # text to remove emoji
        # removeEmoji = demoji.replace(remove_emoji(replaceEnter))
        # # text to remove special character
        # removeSpecialCharacter = re.sub(r"[^a-zA-Z0-9]"," ",removeEmoji)
        # stemming
        stemming = stemmer.stem(lowerCase)
        # stopword removal
        stopWord = stopword.remove(stemming)
        print(stopWord)
        # sys.exit()
        # check similarity
        # try:
        #     textFinal = stopWord.split()[0]
        #     cari = "%" + textFinal +"%"
        #     cursor = conn.cursor() 
        #     #execute select statement 
        #     cursor.execute("SELECT text FROM messages WHERE text LIKE %s LIMIT 1", cari) 
        #     #fetch all rows 
        #     result = cursor.fetchall()
        #     if levenshtein.distance(result, stopWord) < 2.1:
        #         count = count + 1
        #         messagesId = i['id']
        #         groupId = jsonData['id']
        #         type = 'messages'
        #         date = i['date']
        #         chatFrom = i['from']
        #         fromId = i['id']
        #         # insert to database
        #         sql = "INSERT INTO messages (messages_id, group_id, type, date, chat_from, from_id, text) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        #         val = (messagesId, groupId, type, date, chatFrom, fromId, stopWord)
        #         print(val)
        #         print(stemming)
        #         cursor.execute(sql, val)

        #         conn.commit()
        #         print("Scam Detected")
        # except IndexError:
        #     print("IndexError")
print(count)

if __name__ == '__main__':
    app.run()
