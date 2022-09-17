from twitch_grabber import TwitchAudioGrabber

import numpy as np
from io import BytesIO
from pydub import AudioSegment
from pydub.exceptions import CouldntEncodeError
from fake_useragent import UserAgent
import time
import json
import requests


def extract_transcript(resp: str):
    """
    Extract the first results from google api speech recognition
    Args:
        resp: response from google api speech.
    Returns:
        The more confident prediction from the api 
        or an error if the response is malformatted
    """
    if 'result' not in resp:
        raise ValueError({'Error non valid response from api: {}'.format(resp)})
    for line in resp.split("\n"):
        try:
            line_json = json.loads(line)
            out = line_json['result'][0]['alternative'][0]['transcript']
            return out
        except:
            continue


def api_speech(data, ua):
    """Call google api to get the transcript of an audio"""
        # Random header
    headers = {
        'Content-Type': 'audio/x-flac; rate=16000;',
        'User-Agent': ua['google chrome'],
    }
    params = (
        ('client', 'chromium'),
        ('pFilter', '0'),
        ('lang', 'en'),
        ('key', 'AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'),
    )

    proxies = None

    if len(data) == 0:
        return 

    # api call
    try:
        response = requests.post('http://www.google.com/speech-api/v2/recognize',
                                 proxies=proxies,
                                 headers=headers,
                                 params=params,
                                 data=data)
    except Exception as inst:
        print(inst)

    # Parse api response
    try:
        transcript = extract_transcript(response.text)
        return transcript
    except Exception as inst:
        print(inst)
        return


if __name__ == "__main__":

    audio_grabber = TwitchAudioGrabber(twitch_url='https://www.twitch.tv/dakillzor',
                                       dtype=np.int16,
                                       channels=1,
                                       rate=16000)

    #print("here")

    # fakes a browser instance 
    ua = UserAgent()
    i = 0
    while True:
        # we want the raw data not the numpy array to send it to google api
        audio_segment = audio_grabber.grab_raw()
        # grabbed from queue
        if audio_segment:

            raw = BytesIO(audio_segment)
            try:
                raw_wav = AudioSegment.from_raw(
                    raw, sample_width=2, frame_rate=16000, channels=1)
                # print(type(raw_wav)) --> <class 'pydub.audio_segment.AudioSegment'>
            except CouldntEncodeError:
                print("could not decode")
                continue
            raw_flac = BytesIO()
            raw_wav.export(raw_flac, format='flac')
            raw_wav.export(f"example{i}.flac", format='flac')
            i += 1
            #print(type(raw_flac))
            data = raw_flac.read()
            #print(type(data))
            transcript = api_speech(data, ua)
            print(transcript)
        
