from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

pointscollection=None

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
    docs = pointscollection.stream()
    pointsvalue = []
    values=dict()
    values['value']=60
    pointscollection.document('1').set({'value': 80})
    for doc in docs:
        pointsvalue.append(doc.to_dict())
    # docs[0].set(values)
    return pointsvalue[0]["value"]

# firebaseSetup()