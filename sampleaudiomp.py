import glob
from pydub import AudioSegment
from fastapi import FastAPI
import sys
import subprocess
import firebase_admin
# from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import pyrebase
import wave
import base64
# from scipy.io.wavfile import write
from smartyparse import SmartyParser
from smartyparse import ParseHelper
import smartyparse.parsers

app = FastAPI()


@app.get("/")
async def mergeaudio():
    subprocess.call('sampleaudiomp.py', shell=True)
    print("1")
    dirpath = "news/"
    headingsNewsDir = dirpath+"2019-03-01/"
    includeDir = dirpath+"/mp/"
    generatedFile = "combined.mp3"
    print("2")
    # filenames = glob.glob(headingsNewsDir+'*.mp3')
    welcome = await AudioSegment.from_mp3(includeDir + "welcome.mp3")
    thankyou = await AudioSegment.from_mp3(includeDir + "greeting.mp3")
    beep = await AudioSegment.from_mp3(includeDir + "ending.mp3")
    print("3")
    # filenameswithbeep = [welcome, beep]
    combined = AudioSegment.empty()
    combined = welcome + beep + thankyou
    # for filename in filenames:
    #     audiofilename = AudioSegment.from_mp3(filename)
    #     filenameswithbeep.extend([audiofilename, beep])
    print("4")
    # filenameswithbeep.extend([thankyou])

    # for fname in filenameswithbeep:
    #     combined += fname
    print("5")
    await combined.export(headingsNewsDir + combined, format="mp3")
    return {"message": "done"}


@app.get("/getmp")
def getmpaudio():
    dirpath = "news/"
    headingsNewsDir = dirpath+"2019-03-01/"
    includeDir = dirpath+"/include/"
    generatedFile = "combined_news_file.wav"

    filenames = glob.glob(headingsNewsDir+'*.wav')
    welcome = AudioSegment.from_wav(includeDir + "welcome.wav")
    thankyou = AudioSegment.from_wav(includeDir + "thankyou.wav")
    beep = AudioSegment.from_wav(includeDir + "beep.wav")

    # filenameswith = [welcome, beep]
    combined = AudioSegment.empty()
    # for filename in filenames:
    #     audiofilename = AudioSegment.from_wav(filename)
    #     filenameswith.extend([audiofilename, beep])

    # filenameswith.extend([thankyou])

    # for fname in filenameswith:
    #     combined += fname
    combined = welcome + beep + thankyou

    combined.export(headingsNewsDir + generatedFile, format="wav")


@app.get("/checkfirebase")
def checkfirebase():
    # firebaseConfig = {
    #     'apiKey': "AIzaSyBchIyZ1AggBKC0ozHXnejFVVy3XgFUk2Q",
    #     'authDomain': "spavis-8e4f7.firebaseapp.com",
    #     'projectId': "spavis-8e4f7",
    #     'storageBucket': "spavis-8e4f7.appspot.com",
    #     'messagingSenderId': "565341693110",
    #     'appId': "1:565341693110:web:edc5aec9d622e4c0be7217",
    #     'measurementId': "G-HPN7C616N2"
    # }

    # firebase = firebase_admin.initialize_app(firebaseConfig)
    cred = credentials.Certificate("spavis-8e4f7-0d2cabea6066.json")
    app = firebase_admin.initialize_app(cred)

    db = storage.bucket(app)

    # db = firestore.client()

    # cars_ref = db.collection(u'users')
    # docs = cars_ref.stream()

    # cars_list = []
    # for doc in docs:
    #     cars_list.append(doc.to_dict())
    # # print(u'{} => {}'.format(doc.id, doc.to_dict()))

    # return cars_list


@app.get("/checkingPyreBase")
def chekingPyreBase():

    # config = {
    #     "apiKey": "apiKey",
    #     "authDomain": "projectId.firebaseapp.com",
    #     "databaseURL": "https://databaseName.firebaseio.com",
    #     "storageBucket": "projectId.appspot.com",
    #     "serviceAccount": "spavis-8e4f7-0d2cabea6066.json"
    # }

    firebaseConfig = {
        'apiKey': "AIzaSyBchIyZ1AggBKC0ozHXnejFVVy3XgFUk2Q",
        'authDomain': "spavis-8e4f7.firebaseapp.com",
        'projectId': "spavis-8e4f7",
        'storageBucket': "spavis-8e4f7.appspot.com",
        "databaseURL": "https://spavis-8e4f7-default-rtdb.asia-southeast1.firebasedatabase.app",
        'messagingSenderId': "565341693110",
        'appId': "1:565341693110:web:edc5aec9d622e4c0be7217",
        'measurementId': "G-HPN7C616N2",
        "serviceAccount": "spavis-8e4f7-0d2cabea6066.json"
    }

    dirpath = "news/"
    headingsNewsDir = dirpath+"2019-03-01/"
    includeDir = dirpath+"/include/"
    generatedFile = "combined_news_file.wav"

    firebase = pyrebase.initialize_app(firebaseConfig)

    storage = firebase.storage()

    # audios = storage.child().list_files()
    # .child("idhhPkSEGmC8ly0BTjjU/")
    audios = storage.child("idhhPkSEGmC8ly0BTjjU/").list_files()

    combined = AudioSegment.empty()

    nchannels = 1
    sampwidth = 1
    framerate = 8000
    nframes = 100

    name = 'output.wav'

    for audiofromdb in audios:
        print(audiofromdb)
        # audio = wave.open(name, 'wb')
        # audio.setnchannels(nchannels)
        # audio.setsampwidth(sampwidth)
        # audio.setframerate(framerate)
        # audio.setnframes(nframes)
        # blob = open(audiofromdb).read()
        # blob = audiofromdb.read()
        # combined += audio.writeframes(blob)

    

    combined.export(headingsNewsDir + generatedFile, format="wav")

# @app.get("/chechkingscipy")
# def checkingscipy():

#     samplerate = 44100; fs = 100

#     t = np.linspace(0., 1., samplerate)

#     amplitude = np.iinfo(np.int16).max

#     data = amplitude * np.sin(2. * np.pi * fs * t)

#     write("example.wav", samplerate, data.astype(np.int16))
