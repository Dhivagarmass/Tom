from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='v.json'
# initialize Pusher
pusher_client = pusher.Pusher(
   app_id = "714271",
key = "a214a89c7b40cf22c896",
secret = "94e0c6705a1ffd64e2a2",
cluster = "ap2",
    ssl=True)

import requests
import urllib
import os,re
from flask import Flask,redirect, url_for,request,render_template
from threading import Thread
from datetime import datetime,timedelta
from time import sleep
from bs4 import *


domain='dhivagar'
TOKEN = '775020963:AAETGxRdZJZsD4YIdZkmeyIqnfcCcRvSV7A'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
headers={"User-Agent":"Mozilla/5.0 (Linux; Android 5.1; HTC Desire 728 dual sim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36"}

print('Started')
def dipres(rn):
  try:
    f=requests.get(f"http://112.133.214.75/result_oct2018/display.php?regno={rn}&scheme=k", headers=headers)
    r=(BeautifulSoup(f.text,"lxml"))
    j=0
    tab1=r.select('table')[0].select('tr')
    x=("Name   : "+tab1[0].select('td')[1].text.strip()+"\nReg No : "+tab1[1].select('td')[1].text+"\nDept   : "+tab1[2].select('td')[1].text)
    for i in range(1,9):
      j+=int(r.select('table')[1].select('tr')[i].select('td')[3].text)
    x+=(f"\nResult : {r.select('table')[1].select('tr')[10].select('td')[1].text}\nTotal  : {j} \nAverage : {j/8}%\n{alink(f'http://mechsteed.pythonanywhere.com/dip/{rn}','More')}\n@MassDhiva ")
    return x
  except Exception as e:
    return str(e)
def alink(s,k=None):
    if not k:k=s
    return '<a href="{}">{}</a>'.format(s,k)
def slink(s,k=None,v=1):
    ss=s
    for i,j in (('__','\n'),('--',' '),('-','.'),('_','@'),):
            s=s.replace(j,i)
    if k:ss=k
    s=f'https://t.me/smartmanojbot?start={s}'
    return '<a href="{}">{}</a>'.format(s,ss) if v else s
def tclink(s,d=None):
    if d:return f"+91{s[-10:]} | {slink(f'w.{s}',d)} |"
    return slink(f'w.{s}',f"+91{s[-10:]}")
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    return  requests.get(url).json()

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url=URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, chat_id)
    try:
        r=requests.get(url,timeout=30)
        if r.reason!='OK':print(r.text)
    except Exception as e:
        print(e)
        print(url)

def main():
    last_update_id = None
    while True:
        try:
            updates = get_updates(last_update_id)           
            z=updates.get("result")
            if z and len(z) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)
            sleep(0.5)
        except Exception as e:
            print(e)        


def echo_all(updates):
    for update in updates["result"]:
        try:
            bv='message'
            if update.get('edited_message'):
                bv='edited_'+bv
            fname =update[bv]['chat']['first_name']
            chat = update[bv]["chat"]["id"]
            text = update[bv].get("text")
            msg(text,fname,chat)
        except Exception as e:
            print(e)
def msg(text,fname='',chat=0):
    if text:
        print(chat,text)
    text=text.lower()
    text=text.replace('-','')
    text=text.strip('/')
    if text.startswith('start'):
        v=text.split()
        if len(v)==1:
            text='Welcome {}'.format(fname)
            send_message(text,chat)
            text='/help'
        else:
            v=detect_intent_texts(project_id, "unique", v[1], 'en')
            msgf(v,chat,name=name);return
    elif text.startswith('help'):
        h='''
/help
'''
        text=(h)
    elif text.isdigit() and len(text)==8:text=dipres(text)
    elif text.startswith('hi'):text=f'Hi {fname}'
            #customize here
    if text: print(chat,text)
    send_message(text,chat)

def snt(f,a,b=None):
  try:
    Thread(None,f,None,a,b).start()
  except Exception as e:        
    return str(e)


def restart():
 while True:
  try:
   v=(datetime.utcnow()+timedelta(hours=5,minutes=30))
   if(5*60<v.hour*60+v.minute<21*60+30):
    requests.head(f"http://{domain}.herokuapp.com",timeout=5)
   sleep(25*60)
  except Exception as e:
   sleep(60)
   continue

snt(main,())
snt(restart,())



if __name__ == '__main__':
    # app.run()
    z=dipres('19303689')
    print(z)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movie_detail', methods=['POST'])
def get_movie_detail():
    data = request.get_json(silent=True)
    
    try:
        movie = data['queryResult']['parameters']['movie']
        api_key = os.getenv('OMDB_API_KEY')
        
        movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
        movie_detail = json.loads(movie_detail)

        response =  """
            Title : {0}
            Released: {1}
            Actors: {2}
            Plot: {3}
        """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])
    except:
        response = "Could not get movie detail at the moment, please try again"
    
    reply = {
        "fulfillmentText": response,
    }
    
    return jsonify(reply)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    # socketId = request.form['socketId']
    message = request.form['message']
    project_id = 'tombot-138d8'
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    

    pusher_client.trigger('movie_bot', 'new_message',
                        {'human_message': message, 'bot_message': fulfillment_text})
                        
    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
    app.run(debug=1)