import pyaudio
import numpy as np
import time

from pprint import pprint
from datetime import datetime

from octolib import mc


pa = pyaudio.PyAudio()
all_data = []

def callback(in_data, frame_count, time_info, flag):
    audio_data = np.fromstring(in_data, dtype=np.float32)
    # Instead of printing, process here the audio chunk 'audio_data' with libROSA
    # [...]
    # pprint(audio_data)
    ad_len = audio_data.size
    ad_max = audio_data.max()
    ad_min = audio_data.min()
    pprint(['len: {}'.format(ad_len), 'min: {}'.format(ad_min), 'max: {}'.format(ad_max)])
    all_data.append(audio_data)

    return None, pyaudio.paContinue


def stream_audio(time_limit=0):
    stream = pa.open(format=pyaudio.paFloat32,
                     channels=1,
                     rate=44100,
                     output=False,
                     input=True,
                     stream_callback=callback)

    stream.start_stream()
    start_time = datetime.now()

    while (stream.is_active() and (
            (datetime.now() - start_time).seconds < time_limit)
            or time_limit == 0
    ):
        time.sleep(0.25)
    stream.close()
    pa.terminate()

    pprint('{} rows in all_data'.format(len(all_data)))
    mc.set('pyaudio', all_data)


if __name__ == '__main__':
    stream_audio()
