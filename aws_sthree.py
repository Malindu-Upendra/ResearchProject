from email.mime import audio
import logging
import os
import boto3
import glob
from botocore.exceptions import ClientError
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import shutil
from pydub.playback import play
from pathlib import Path
import errno

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
    data_file_folder = os.path.join(os.getcwd(), 'AAC_audios')
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


@app.get("/downloadFiles/{bookId}")
async def getName(bookId: str):
    downloadedFilesDir = "Files Download/"
    mergedFileDir = "Merged files/"
    generatedFile = "final.wav"

    path = bookId

    # Handle missing / at end of prefix
    if not path.endswith('/'):
        path += '/'

    paginator = client_s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=path):
        # Download each file individually
        for key in result['Contents']:
            # Calculate relative path
            rel_path = key['Key'][len(path):]
            # Skip paths ending in /
            if not key['Key'].endswith('/'):
                local_file_path = os.path.join(downloadedFilesDir, rel_path)
                # Make sure directories exist
                local_file_dir = os.path.dirname(local_file_path)
                assert_dir_exists(local_file_dir)
                client_s3.download_file(
                    bucket_name, key['Key'], local_file_path)

    combined = AudioSegment.empty()
    filenames = glob.glob(downloadedFilesDir+"*.wav")

    for filename in filenames:
        # print(filename)
        audiofilename = AudioSegment.from_file(filename, "wav")
        # print(audiofilename)
        combined += audiofilename

    combined.export(mergedFileDir + generatedFile, format="wav")

    client_s3.upload_file(
                    os.path.join(os.getcwd(), 'Merged files/final.wav'),
                    bucket_name,
                    path + "final.wav"
                )

    for filename in filenames:
        os.remove(filename)

    final_merged_file = mergedFileDir + generatedFile

    os.remove(final_merged_file)

    return True
    

def assert_dir_exists(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@app.get("/getUrl")
def returnUrlOfFile():
    try:
        response = client_s3.generate_presigned_url('get_object', Params={
                                                    'Bucket': bucket_name, 'Key': "4Lrt2s6T9b0ltqSF0vse/final.wav"})
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


"""
testing API call from flutter

"""


@app.get("/testApi")
def testApi():
    return {"hello world"}

# @app.get("/combineMp4")
# def combinedmpfour():
#     downloadedFilesDir = "Files Download/"
#     mergedFileDir = "Merged files/"
#     generatedFile = "combined_file.wav"
#     combined = AudioSegment.empty()

#     filenames = glob.glob(downloadedFilesDir+"*.wav")

#     for filename in filenames:
#         # print(filename)
#         audiofilename = AudioSegment.from_file(filename, "wav")
#         # print(audiofilename)
#         combined += audiofilename

#     combined.export(mergedFileDir + generatedFile, format="wav")
