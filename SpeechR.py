from twitch_grabber import TwitchAudioGrabber

import speech_recognition as sr
import numpy as np
from io import BytesIO
from pydub import AudioSegment
from pydub.exceptions import CouldntEncodeError


"""
Pop an audio segment raw file. If there is an audio segment, convert it into a flac file using AudioSegment library. Use speech recognition library from
Py to read audio and translate it into text. Uses google speech recognition. Does not use grab method which converts bytes to numpy array.
"""

if __name__ == "__main__":

    audio_grabber = TwitchAudioGrabber(twitch_url='https://www.twitch.tv/nick_shox',
                                       dtype=np.int16,
                                       channels=1,
                                       rate=16000)
    i = 0
    try:
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
                    raw_wav.export(f"Audio{i}.flac", format='flac')
                    data = raw_flac.read()

                    # wtf is goin on
                    r = sr.Recognizer()
                    with sr.AudioFile(f"Audio{i}.flac") as source:
                        audio = r.record(source)
                    transcript_dict = r.recognize_google(audio, language = 'en-IN', show_all = True)
                    print(f"----------------------------------------------------------- \nAudio file {i}:" )
                    print(type(transcript_dict))
                    print(transcript_dict)
                    print("-----------------------------------------------------------")
                    i += 1
    except KeyboardInterrupt:
        print("Ended")
        pass
        
