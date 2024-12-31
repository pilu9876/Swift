from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pickle
import tensorflow
import tensorflow.keras.models as models
from response import generate_response
from predict import prediction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder


app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dsouza82*'
app.config['MYSQL_DB'] = 'banklogin'

mysql = MySQL(app)
# Load the model
model = models.load_model("model.h5")
# Load the vectorizer
with open("vectorizer.pkl", "rb") as file:
  loaded_vectorizer = pickle.load(file)
#Save the Label Encoder
with open("labelencoder.pkl", "rb") as file:
  loaded_encoder = pickle.load(file)

@app.route('/')
def index():
    return '<h1>Home Page</h1>'

@app.route('/api')
def api():
    account_no = 0
    user_input = request.args.get('input')
    user_input = user_input.split(' ')
    if ((user_input[0].isdigit()) and (len(user_input[0])==10)):
        account_no = user_input[0]
        user_input = ''
    elif ((user_input[-1].isdigit()) and (len(user_input[-1])==10)):
        account_no = user_input[-1]
        user_input.pop()
    elif ((type(user_input[0]) == float) and (user_input[-1].isdigit()) and (len(user_input[-1]) == 10)):
        account_no = user_input[-1]
        user_input.pop()
    else:
        user_input.pop()
    user_input = ' '.join(user_input)

    tag = prediction([user_input], model, loaded_vectorizer, loaded_encoder)[0]
    response = generate_response(mysql, user_input.lower(), tag, account_no)

    json = {
        'cnt': response.response
    }

    if response.response == "Your transaction details are":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT DateTransaction, Particulars, Deposits, Withdrawals, Balance FROM (select * FROM accounts WHERE AccountNo = % s ORDER BY Recordind DESC LIMIT 3) AS r ORDER BY Recordind', (account_no,))
        accounts = cursor.fetchall()
        return render_template('transaction.html', data=accounts)
    else:
        return json



if __name__ == "__main__":
    app.run(host='192.168.99.180', port=5000, debug=True)


