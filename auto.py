if 1:
    api_id = 561796
    api_hash = '7699375c0a6c0889a53cc3e7e4becf56'
    sn='MD'
from telethon import TelegramClient, events, sync


client = TelegramClient(sn, api_id, api_hash)
client.start()
gud='(gud|good)'
wt='(What|wt)'
u='(u|you)'
d={
    '(ha?i+|ji+|hey|hello)$':'S',
    'oi+':'Oii Baby',
    'saptiya':'S',
    'baby':'S baby',
    'haha|nice|👍':'Cool',
    'sry|sorry':'https://philosophyonthemesa.com/2010/11/01/never-apologize-it%E2%80%99s-a-sign-of-weakness/',
    f'(Thanks|tq|thank|dhank)( {u})?':'AnyTime ☺️',
    '(oh+|hmok|o?k+$|okie+|h?m+)$':'☺️',
    '😍+$':'😍😍😍',
    f'(enna panra)|({wt} (are you )?doing\??)':'work',
    'ah$':'Ah Ahh',
    'aha+':'😍',
    f'({gud} (night|nI[8t]))|(Good night sweet dreams)':'Have a cute sleep ☺️',
f'({gud} (mor(ning)?|mrng)|Gm)$':'Have a cute day ☺️',
f'({gud} eve)$':'Have a  sweet evening☺️',
}
from collections import *
import re
from datetime import datetime,timedelta,date as dtdate,time as dttime

dc=defaultdict(int)
@client.on(events.NewMessage(incoming=True))
lst=''
async def handler(event):
    try:
        d=datetime.now().date()
        dd=d+str(event.chat_id)
        dc[dd]+=1
        
        if dc[dd]>10:return
        t=event.raw_text.lower()
        if lst==t:return
        lst=t
        for i in ('manoj','da','anna','thambi'):t=t.replace(i,'')
        t=re.sub('\s+',' ',t).strip()
        if t==' ':t='hi'
        for i,j in d.items():
            if re.match(i+r'\b',t):
                await event.respond(j)
    except Exception as e:
        print(e)


print('Auto')

