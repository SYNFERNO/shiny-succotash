import demoji
from flask import Flask
import json, re
import demoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

app = Flask(__name__)

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
# open json from telegram
f = open('telegram.json',)
jsonData =  json.load(f)
# stop word
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

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
        # remove /n
        replaceEnter = lowerCase.replace('/n', '') 
        # text to remove emoji
        removeEmoji = demoji.replace(remove_emoji(replaceEnter))
        # text to remove special character
        removeSpecialCharacter = re.sub(r"[^a-zA-Z0-9]"," ",removeEmoji)
        # stemming
        stemming = stemmer.stem(removeSpecialCharacter)
        # stopword removal
        stopWord = stopword.remove(stemming)

        # print
        print(stopWord)

if __name__ == '__main__':
    app.run()