from flask import Flask, g, redirect, url_for, render_template, request, jsonify, flash
from werkzeug.utils import secure_filename
from operasiFile import hitungTotalFile

import pandas as pd
import numpy as np
import os
import uuid
import base64

import cekDataset as cd
import systemTesting as uji

import sqlite3
import datetime

BASE_DIR = os.getenv("BASE_DIR")

UPLOAD_FOLDER = "data_upload"
BASE_URL = os.getenv("SERVER_URL")

batik_class = ["Batik_Betawi", "Batik_Geblekrenteng", "Batik_Kawung", "Batik_Lasem", "Batik_Megamendung", 
               "Batik_Pala", "Batik_Parang", "Batik_Sekarjagad", "Batik_Tambal"]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle

from keras.models import load_model
model = load_model('model/chatbot_model.h5')
import json
import random
intents = json.loads(open('model/chatbot_intents.json').read())
words = pickle.load(open('model/words.pkl','rb'))
classes = pickle.load(open('model/classes.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

#script chatbot
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

#script chatbot
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

#script chatbot
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

#script chatbot
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

# route index
@app.route("/")
def index():
    return render_template("home.html", dr=BASE_URL)

# route dataset 
@app.route("/dataset")
def dataset():
    dataset = cd.getInformasiDataset()
    return render_template("dataset.html", mData=BASE_URL, fileBetawi=dataset['dataBatik'])


# route cara tambahkan dataset 
@app.route('/cara-tambahkan-dataset')
def caraTambahkanDataset():
    return render_template('cara-tambah-dataset.html', mData=BASE_URL)

# route training data 
@app.route('/training-data')
def trainingData():
    return render_template('training-data.html', mData=BASE_URL)

@app.route('/proses-cek-dataset', methods=('GET','POST'))
def prosesCekDataset():
    dataset = cd.getInformasiDataset()
    dr = {'status' : 'success', 'dataset':dataset['dataKuantitas']}
    return jsonify(dr)



@app.route('/upload', methods=["POST"])
def upload():
    if(request.method == "POST"):
        imagefile = request.file['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("/uplodedimages" + filename)
        return jsonify({
            "message": "Image Upload Successfully"
        })




@app.route('/klasifikasi')
def klasifikasi():
    return render_template('klasifikasi.html', mData=BASE_URL)

@app.route('/proses-klasifikasi', methods=('GET','POST'))
def prosesKlasifikasi():
    kdPengujian = uuid.uuid4()
    dataGambar = request.form.get("gambar")
    format, imgstr = dataGambar.split(";base64,")
    decoded_img = base64.b64decode((imgstr))
    img_file = open(str(BASE_DIR)+'/static/upload_data_uji/'+str(kdPengujian)+'.png', 'wb')
    img_file.write(decoded_img)
    img_file.close()

    hasilKlasifikaasi = uji.testingDataUji(batik_class, kdPengujian)

    dr = {'status' : 'success', 'hasil' : hasilKlasifikaasi}
    
    return jsonify(dr)

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")
# route chatbot
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

# Set a secret key for the app to use
app.secret_key = 'abcdef12345!@#$%'

# Set the database file name
DATABASE = 'Store.db'

# Define a function to get the database connection
def get_db():
    # Get the database connection from the app context
    db = getattr(g, '_database', None)
    if db is None:
        # Create a new database connection if one does not exist
        db = g._database = sqlite3.connect(DATABASE)
        # Set the row factory to sqlite3.Row to return rows as dictionaries
        db.row_factory = sqlite3.Row
    return db

# Define a function to close the database connection when the app context is torn down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Define an error handler for database errors
@app.errorhandler(sqlite3.Error)
def handle_database_error(error):
    return 'A database error occurred: ' + str(error), 500

@app.route('/login')
def login():
    try:
        
        # Get the database connection
        db = get_db()
        # Create a cursor to execute SQL statements
        cursor = db.cursor()
        # Create a users table if it does not exist
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, password TEXT, created_at DATETIME)')
        # Commit the changes to the database
        db.commit()
        # Close the cursor
        cursor.close()
        # Return the index.html template
        return render_template('login.html')
    except sqlite3.Error as e:
        # Return an error message if a database error occurs
        return 'A database error occurred: ' + str(e), 500

# Define a route to create a new user
@app.route('/create_account', methods=['POST'])
def create_user():
    # Get the database connection
    db = get_db()
    # Get the form data from the request
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Check if the passwords match
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return render_template('login.html')

    # Create a cursor to execute SQL statements
    cursor = db.cursor()
    # Check if the email already exists in the database
    cursor.execute('SELECT email FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    if user:
        # Return an error message if the email already exists
        cursor.close()
        flash('User already exists', 'error')
        return render_template('login.html')

    # Insert the new user into the users table
    cursor.execute('INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (?, ?, ?, ?, ?)',
                (first_name, last_name, email, password, datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
    # Commit the changes to the database
    db.commit()
    # Close the cursor
    cursor.close()

    # Return a success message
    flash('User created successfully', 'success')   
    return render_template('login.html')

# jalankan server 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6005)