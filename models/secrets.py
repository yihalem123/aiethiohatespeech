import tensorflow as tf

import keras
# Making a GET request
#r = requests.get('https://mbasic.facebook.com/story.php?story_fbid=571217590959575&id=415518858611168')
  
# check status code for response received
# success code - 200

  
# print content of request
#html = bs4.BeautifulSoup(r.text, "lxml")
#print(html.title)
#title = str(html.title)
#print("this")

#text1="የዓመቱ ምርጥ ቪዲዮ ፡ ይህንን የሰማ ይፀናል "
#translator = Translator()  # initalize the Translator object
#translations = translator.translate(title, dest='en')  # translate two phrases to Hindi
 # print every translation
#text=translations.text
load_model=tf.keras.models.load_model("models/hate.h5")
with open('./models/tokenizer.pickle', 'rb') as handle:
    load_tokenizer = pickle.load(handle)

def clean_text(text):
    print(text)
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    print(text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
test=[clean_text('this is hate from me')]
print(test)
seq = load_tokenizer.texts_to_sequences(test)
padded = sequence.pad_sequences(seq, maxlen=300)
print(seq)
pred = load_model.predict(padded)
print("pred", pred)
if pred<0.8:
    print("no hate")
else:
    print("hate and abusive")


