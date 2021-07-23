

import keras
from keras.preprocessing import sequence
import pickle
import re
import string
import nltk
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import tensorflow as tf
load_model=keras.models.load_model("./models/hate_model.h5")
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
    stopword=set(stopwords.words('english'))
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
test=[clean_text('i love Ethiopians')]
print(test)
seq = load_tokenizer.texts_to_sequences(test)
padded = sequence.pad_sequences(seq, maxlen=300)
print(seq)
pred = load_model.predict(padded)
print("pred", pred)
if pred>0.8:
    print("no hate")
else:
    print("hate and abusive")

https://mbasic.facebook.com/ixt/trigger/nfx/msite/?trigger%5Btrigger_event_type%5D=nfx_action_executed&trigger%5Bnfx_context%5D=%7B%22session_id%22%3A%22223d7b36-dfe9-4004-85f8-780497792c08%22%2C%22type%22%3A2%2C%22initial_action_name%22%3A%22RESOLVE_PROBLEM%22%2C%22story_location%22%3A%22photo_viewer%22%2C%22entry_point%22%3A%22report_button%22%2C%22actions_taken%22%3A%22RESOLVE_PROBLEM%22%2C%22entry_point_uri%22%3A%22https%3A%5C%2F%5C%2Fmbasic.facebook.com%5C%2Fstory.php%3Fstory_fbid%3D571217590959575%26id%3D415518858611168%22%2C%22reportable_ent_token%22%3A%22571217590959575%22%7D&trigger%5Btrigger_session_id%5D=49b2057b-faa4-4c49-bcf0-babe537744ad&ref_component=mbasic_photo_permalink&_rdr