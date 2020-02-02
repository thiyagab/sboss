import os
from uuid import uuid4

import firebase_admin
import telegram
from telegram import InlineKeyboardButton, InlineQueryResultArticle, InlineKeyboardMarkup, InputTextMessageContent, \
    ParseMode
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler, Dispatcher

from firebase_admin import credentials
from firebase_admin import firestore

score=-999
pointscollection=None

def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    newscore = getNumber(query.strip())
    score=getscore()
    results=[]
    if(newscore):
        keyboard = [
            [InlineKeyboardButton("Confirm", callback_data='1#'+str(score+newscore)),
             InlineKeyboardButton("Cancel", callback_data='2#')]]
        results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title='Request '+str(score)+"+"+str(newscore)+'='+str(score+newscore),
                reply_markup=InlineKeyboardMarkup(keyboard),
                input_message_content=InputTextMessageContent(
                    'Request for'+str(score)+"+"+str(newscore)+'='+str(score+newscore)+' points')),
           )
    results.append(  InlineQueryResultArticle(
                id=uuid4(),
                title='Points: '+str(score),
                input_message_content=InputTextMessageContent(
                    'Total points: '+str(score))))


    update.inline_query.answer(results,cache_time=5)

def firebaseSetup():
    print('Firebase setup')
    global pointscollection
    # Use a service account
    cred = credentials.Certificate('serviceaccount.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    print('Firebase initialized')
    pointscollection = db.collection(u'points')
    print(getFirebaseScore())

def getFirebaseScore():
    print('Get score ')
    if not pointscollection:
        firebaseSetup()
    docs = pointscollection.stream()
    pointsvalue = []
    for doc in docs:
        pointsvalue.append(doc.to_dict())
    # docs[0].set(values)
    print('score '+str(pointsvalue[0]["value"]))
    return pointsvalue[0]["value"]

def writeFirebaseScore(score):
    if not pointscollection:
        firebaseSetup()
    pointscollection.document('1').set({'value': score})
def getNumber(score):
    try:
        return int(score)
    except ValueError:
        pass

def button(bot, update):
    query = update.callback_query
    if query.data.startswith("1#"):
        newscore=query.data[2:].strip()
        score = getNumber(newscore)
        if(score):
            writescore(score)
            query.edit_message_text(text="Total points : "+str(score))
    elif query.data.startswith("2#"):
        query.edit_message_text(text="Request Rejected")

def writescore(newscore):
    global score
    score = newscore
    # file = os.open("score", "w")
    # file.write(file,str(score))
    # file.close
    writeFirebaseScore(score)

def getscore():
    global score
    # if score!=-999:
    #     return score
    score= getFirebaseScore()
    return score


def sboss(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        # chat_id = update.message.chat.id
        # Reply with the same message
        # bot.sendMessage(chat_id=chat_id, text=update.message.text+'1')
    return "ok"

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_handler(CallbackQueryHandler(button))
firebaseSetup()
# writeFirebaseScore(100)