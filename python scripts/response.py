import MySQLdb.cursors
from datetime import date
from collections import namedtuple
import random
import json
import random
from preprocess import textPreprocess
from commonword import findcommonword

#Load file to get response
with open('intents.json') as file:
    intents = json.load(file)


Response = namedtuple('Response', 'response accuracy')

def generate_response(mysql, lc_input: str, tag: str, account_no: int) -> Response:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for intent in intents["intents"]:
        if tag == intent["tag"]:
           if len(intent["responses"])>2:
               response = findcommonword(lc_input, intent["responses"])
           else:
               response = random.choice(intent["responses"])
    if lc_input.find("withdrawtrue") != -1:
        dep = None
        withdraw = float(lc_input.split(' ')[0])
        cursor.execute('SELECT * FROM accounts WHERE AccountNo = % s', (account_no,))
        account = cursor.fetchall()
        n_records = len(account)
        cursor.execute('SELECT * FROM accounts')
        account_tot = cursor.fetchall()
        total_records = len(account_tot)
        particulars = "POS ATM PU" + " " + str(random.randint(1000, 9999)) + " " + lc_input.split(' ')[-2].upper()
        datetransaction = date.today()
        sql = "INSERT INTO accounts (Recordind, UserName, AccountNo, DateTransaction, Particulars, Deposits, Withdrawals, Balance, Address, BranchAddress, MICR, IFSC, TelNo, CardNo, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
        total_records+1, account[n_records - 1]["UserName"], account[n_records - 1]["AccountNo"], datetransaction, particulars,
        dep, withdraw, account[n_records - 1]["Balance"] - withdraw,
        account[n_records - 1]["Address"], account[n_records - 1]["BranchAddress"], account[n_records - 1]["MICR"],
        account[n_records - 1]["IFSC"], account[n_records - 1]["TelNo"], account[n_records - 1]["CardNo"], account[n_records - 1]["Password"])
        cursor.execute(sql, val)
        mysql.connection.commit()
        return Response("Payment done", 1)
    elif lc_input.find("blocktrue") != -1:
        blocknumber = int(lc_input.split(' ')[0])
        cursor.execute('select AccountNo FROM accounts WHERE CardNo = % s and AccountNo = % s', (blocknumber, account_no,))
        accounts = cursor.fetchall()
        if len(accounts) != 0:
            cursor.execute('UPDATE accounts SET CardNo=null WHERE AccountNo = % s', (account_no,))
            mysql.connection.commit()
            return Response("Your card has been blocked. For issueing a new card, please contact our customer support at +912261717806", 1)
        else:
            return Response("Please enter valid Card Number", 1)
    elif tag == "accountbalance":
        cursor.execute('SELECT Balance FROM accounts WHERE AccountNo = % s ORDER BY DateTransaction DESC LIMIT 1', (account_no,))
        accounts = cursor.fetchall()
        return Response("Your account balance is" + " " + str(accounts[0]['Balance']), 1)
    elif ((lc_input.split(" ")[0].isdigit()) and (len(lc_input.split(" ")[0])==4)):
        cursor.execute('SELECT CardNo FROM accounts WHERE Password = % s and AccountNo = % s', (lc_input.split(" ")[0], account_no,))
        accounts = cursor.fetchall()
        if len(accounts) == 0:
            return Response("Please enter the valid four digit", 0)
        else:
            return Response("valid number To whom should the payment be made?", 1)
    elif (account_no==0):
        if (tag != "Greetings"):
            return Response("Please enter account number.", 1)
        else:
            return Response(response, 1)
    elif account_no!=0:
        cursor.execute('SELECT AccountNo FROM accounts WHERE AccountNo = % s', (account_no,))
        accounts = cursor.fetchall()
        if len(accounts)==0:
           return Response("This account number is not found in our records. Please enter the valid account no.", 0)
        else:
            if len(lc_input)>0:
                return Response(response, 1)
            else:
                cursor.execute('SELECT UserName FROM accounts WHERE AccountNo = % s LIMIT 1', (account_no,))
                accounts = cursor.fetchall()
                return Response("Hi"+" "+ accounts[0]['UserName'] + " " + "What can I do for you?", 1)
