import os
import boto3
import glob
from botocore.exceptions import ClientError
from fastapi import FastAPI
from pydub import AudioSegment

app = FastAPI()

@app.get("/mergeFile")
async def getName():
    aacAudios = "AAC_audios/"
    mergedFileDir = "Merged files/"
    generatedFile = "combined_file_aac.aac"

    filenames = glob.glob(aacAudios+'*.aac')

    combined = AudioSegment.empty()

    for filename in filenames:
        # print(filename)
        audiofilename = await AudioSegment.from_file(filename, "aac")
        print(audiofilename)
        # combined += audiofilename

    # combined.export(mergedFileDir + generatedFile, format="aac")