#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import json
import glob
import hashlib
import thread

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from random import shuffle

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS

DISCOVERY_URL = (
    'https://{api}.googleapis.com/$discovery/rest?'
    'version={apiVersion}'
)

def prepare_phrases(lines):
    phrases = remove_duplicates(' '.join(lines).replace('-', ' ').replace('.', '').replace('?', '').replace('!', '').lower().split(' '))
    phrases = filter(None, phrases)
    phrases.sort(key=len, reverse=True)
    phrases = phrases[:50]

    return phrases

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform']
    )
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1', http=http, discoveryServiceUrl=DISCOVERY_URL
    )

def transcribe(speech_file, phrases):
    with open(speech_file, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = speech_service()

    service_request = service.speech().recognize(
        body={
            'initialRequest': {
                'encoding': 'LINEAR16',
                'sampleRate': 48000,
                'maxAlternatives': 5,
                'speechContext': {
                    'phrases': [
                        phrases
                    ]
                }
            },
            'audioRequest': {
                'content': speech_content.decode('UTF-8')
            }
        }
    )

    response = service_request.execute()
    return response

script = open('alarms_script.txt')
#script = open('sleep_sounds_script.txt')
#script = open('bunnyvoice_benjo_script.txt')
script = script.read().decode('utf-8')

lines = []
hashes = []

for line in script.splitlines():
    line = line.strip().split('[')[0].strip()
    lines.append(line)

phrases = prepare_phrases(lines)
files = glob.glob('audio/alarms/alarms_*.wav')
#files = glob.glob('audio/sleep_sounds/sleep_sounds_*.wav')
#files = glob.glob('audio/original/voicebunny_benjo_*.wav')

#shuffle(files)

for name in files:
    transcription = transcribe(name, phrases)

    if 'responses' in transcription:
        transcript = transcription['responses'][0]['results'][0]['alternatives'][0]['transcript']

        #print len(transcription['responses'][0]['results'][0]['alternatives'])

        options = []

        print transcription

        for option in transcription['responses'][0]['results'][0]['alternatives']:
            options.append(process.extractOne(option['transcript'], lines))
            #print option['transcript']
            #print process.extractOne(option['transcript'], lines)

        #print options
        options.sort(key=lambda x: int(x[1]), reverse=True)
        #print options
        #exit()

        matches = process.extract(transcript, lines, limit=5)
        #match = process.extractOne(transcript, lines)
        match = options[0]

        #if match[1] < 95:
        if match[1] > 85:
            if match[1] < 100:
                print 'Transcription:'
                print transcription
                print 'Options:'
                print options
                print 'Matches:'
                print matches

            hashed = hashlib.md5(match[0].encode('utf-8')).hexdigest()

            if hashed not in hashes:
                print 'Hash:', hashed
                print 'File:', name
                print 'Line:', (lines.index(match[0]) + 1)
                print 'Script:', match[0]
                print 'Google:', transcript
                print 'Confidence:', match[1]
                print ''
                hashes.append(hashed)
                #play_audio(name)
                #exit()

hits = "{0:.2f}".format((float(len(hashes)) / float(len(lines))) * 100)
print 'Hits:', str(hits) + '% (' + str(len(hashes)) + ')'
print 'Misses:', str(100 - float(hits)) + '% (' + str(len(lines) - len(hashes)) + ')'
print 'Files:', len(files)
print ''
print 'Unmatched:'

for line in lines:
    hashed = hashlib.md5(line.encode('utf-8')).hexdigest()

    if hashed not in hashes:
        print line

#transcribe('audio/original/voicebunny_benjo_180.800-183.650.wav')
#transcribe('audio/audio.raw')

"""
FILE = 'audio/original/voicebunny_benjo.wav'

#[flagsInd, classesAll, acc] = aS.mtFileClassification("FILE", "pyAudioAnalysis/data/svmSM", "svm", False)

[Fs, x] = aIO.readAudioFile(FILE)
segments = aS.silenceRemoval(x, Fs, 0.020, 0.020, smoothWindow = 0.1, Weight = 0.6, plot = True)

classifyFolderWrapper('audio/split/voicebunny_benjo_', 'svm', 'data/svnSM')

python pyAudioAnalysis/audioAnalysis.py silenceRemoval -i audio/original/voicebunny_benjo.wav --smoothing 0.1 --weight 0.6
python pyAudioAnalysis/audioAnalysis.py silenceRemoval -i audio/original/voicebunny_benjo.wav --smoothing 1 --weight 0.5
python pyAudioAnalysis/audioAnalysis.py classifyFolder -i audio/split/voicebunny_benjo_ --model svm --classifier pyAudioAnalysis/data/svmSM --detail
python pyAudioAnalysis/audioAnalysis.py classifyFolder -i audio/original/voicebunny_benjo_ --model svm --classifier pyAudioAnalysis/data/svmSM --detail

python pyAudioAnalysis/audioAnalysis.py silenceRemoval -i audio/sleep_sounds/sleep_sounds.wav --smoothing 1 --weight 0.5

python pyAudioAnalysis/audioAnalysis.py silenceRemoval -i audio/alarms/alarms.wav --smoothing 1 --weight 0.5


export GOOGLE_APPLICATION_CREDENTIALS=~/hello/hanasu/google-credentials.json
export GCLOUD_PROJECT=hello-speech

ffmpeg -i audio/original/voicebunny_benjo_180.800-183.650.wav -f s16be -ar 16000 -acodec pcm_s16be audio/original/voicebunny_benjo_180.800-183.650.raw

"""
