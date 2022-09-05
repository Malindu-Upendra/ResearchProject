import os
import boto3
import glob
from botocore.exceptions import ClientError
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


access_key = 'AKIARGVZWKLBUL5KGBTC'
access_secret = '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'
bucket_name = 'spavis'

"""
Connect to s3 Service
"""

client_s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret
)

"""
UPload files to S3 Bucket
"""

@app.get("/uploadFiles")
def getName():
    data_file_folder = os.path.join(os.getcwd(), 'Data files')
    for file in os.listdir(data_file_folder):
        if not file.startswith('~'):
            try:
                print('Uploading file {0}...'.format(file))
                client_s3.upload_file(
                    os.path.join(data_file_folder, file),
                    bucket_name,
                    file
                )
            except ClientError as e:
                print('Credential is incorrect')
                print(e)
            except Exception as e:
                print(e)


"""
Downloading files from s3 bucket
"""

@app.get("/downloadFiles")
def getName():
    downloadedFilesDir = "Files Download/"
    mergedFileDir = "Merged files/"
    generatedFile = "combined_file.wav"
    combined = AudioSegment.empty()

    list = client_s3.list_objects(Bucket='spavis')['Contents']
    for key in list:
        client_s3.download_file(bucket_name, key['Key'], os.path.join(
            './Files Download', key['Key']))

    filenames = glob.glob(downloadedFilesDir+'*.wav')

    for filename in filenames:
        audiofilename = AudioSegment.from_wav(filename)
        combined += audiofilename

    combined.export(mergedFileDir + generatedFile, format="wav")

"""
testing API call from flutter

"""


class AudioClip(BaseModel):
    name: str
    uid: str
    chapter: int
    file: UploadFile

@app.post("/testFlutterAPI")
def flutterAPI(audioClip: AudioClip):
    print("api called")
    print(audioClip)
    return {'result': True}

@app.get("/testApi")
def testApi():
    return {"hello world"}
# @app.post("/uploadBill")
# def root(file: UploadFile = File(...)):
#     result = uploadFile(file.file)
#     return {"result": result}