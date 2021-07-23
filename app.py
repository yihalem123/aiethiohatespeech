from flask import Flask,render_template,request,flash, redirect,url_for,session
from flask_session import Session
import requests
import bs4 
import re
from googletrans import Translator, constants
import googletrans
import sqlite3
import keras
from keras.preprocessing import sequence
import pickle
import bcrypt
import string
import nltk
import os
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import tensorflow as tf

#from datetime import date
app = Flask(__name__)   
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = os.urandom(24)
@app.route('/', methods=['GET'])
def asm():
    """ Displays the index page accessible at '/' """

    return render_template('index.html')

# A decorator used to tell the application
# which URL is associated function
def get_db_connection():
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn
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
@app.route('/index', methods =["POST"])
def index():
    from datetime import date
    if request.method == "POST":
       # getting input with name = fname in HTML form
       url = request.form.get("url")
       # getting input with name = lname in HTML form 
       today = date.today()
       name = request.form.get("name") 
       date1 = request.form.get('date')
       
       date = 'this'
       email = request.form.get('email') 
       res = [int(i) for i in url.split('/') if i.isdigit()]
       r = requests.get(f"https://mbasic.facebook.com/{res[0]}/posts/{res[1]}")
       html = bs4.BeautifulSoup(r.text,features="lxml")
       title1=html.title
       print(title1)
       #title=title[:len(title) // 2]
       title=str(title1)
       
       title=title[7:len(title) // 2] + '......'
       

       translator = Translator()  # initalize the Translator object
       translations = translator.translate(title, dest='en')  # translate two phrases to Hindi
 # print every translation
       translated=translations.text
       image_src = ''
       for image_src in html.find_all(attrs={'href': re.compile("http")},class_='sec'):
               image_src = image_src.get('href')
       print(image_src)       
       conn= get_db_connection()
       conn.execute('INSERT INTO users (name, email,content) VALUES (?, ?,?)',
                         (name, email,title))
       conn.commit()
       conn.close()
       load_model=keras.models.load_model("./models/hate_model.h5")
       with open('./models/tokenizer.pickle', 'rb') as handle:
            load_tokenizer = pickle.load(handle)
       test=[clean_text(title)]
       seq = load_tokenizer.texts_to_sequences(test)
       padded = sequence.pad_sequences(seq, maxlen=300)
       print(seq)
       pred = load_model.predict(padded)
       print("pred", pred)
       result = ''
       if pred>0.7:
            result = "no hate"
       else:
            result = "hate and abusive"

       
       return render_template("index.html", data=title,index=True,img=image_src,result=result)
    return render_template("index.html", data=title,index=True)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        name=request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
    name=request.form.get('email')
    password = request.form.get('password')
    conn= get_db_connection()
    user = conn.execute("SELECT * FROM admins WHERE email =?", (name,))
    if user is not None:
        data =user.fetchone()
        try:
            passworddb = data['password']
        except Exception:
            error = 'Invalid Username or Password'
            return render_template('./admin/auth/login.html', error=error)


        #if bcrypt.checkpw(bcrypt.hashpw(password.encode('utf-8')),bcrypt.hashpw(passworddb.encode('utf-8'))):
        if password == passworddb:
            app.logger.info('Password Matched')
            session['isloged'] = True
            
            flash('You are now logged in','success')
            conn.close()
            return redirect(url_for('dashboard'))
        else:
                error = 'Invlaid Username or Password'
                return render_template('./admin/auth/login.html',error=error)
    else:
        error = 'Username not found'
        return render_template('./admin/auth/login.html', error=error)
    return render_template('./admin/auth/login.html',error = error)
@app.route('/dashboard')
def dashboard():
    conn= get_db_connection()
    user=conn.execute("SELECT COUNT(*) FROM users;")
    data = user.fetchall()[0][0]
    value = 0
    requests = data
    user2 = conn.execute('SELECT COUNT(*) FROM users WHERE created = CURRENT_TIMESTAMP')
    user1 = user2.fetchall()[0][0]
    if session.get('isloged'):

        return render_template('./admin/index.html',data=data,value=value,resuests=data,user1=user1)
    else:
        return render_template('./admin/auth/login.html')
@app.route('/logout')
def logout():
    session.pop('isloged',False)
    return redirect(url_for('admin'))
  
if __name__=='__main__':
   app.run(debug=True)