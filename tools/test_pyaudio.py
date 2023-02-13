import pyaudio
import numpy as np
import time
import librosa

from pprint import pprint
from datetime import datetime

from octolib import mc


DEFAULT_SAMPLE_RATE = 44100
DEFUALT_CHUNK_SIZE = 64
DEFAULT_BUFFER_SIZE = 2000      # ths is the number of audio chunks to keep
DEFAULT_REPORT_INTERVAL = 0.5   # seconds between reports

all_data = []
buffer_size = 500


class StreamTime:
    def __init__(self):
        self.start_time = datetime.now().timestamp()

    def get_stream_time(self, adc_time):
        stream_time = adc_time - self.start_time
        return stream_time


st = StreamTime()


class AudioStreamBuffer:
    def __init__(self, buffer_size: int = DEFAULT_BUFFER_SIZE):
        self.audio_buffer: list = []
        self.stats_buffer: list = []
        self.buffer_size = buffer_size
        self.latest_stream_time = 0

    def add(self, audio_data: np.array, stream_time: float):
        self.audio_buffer.append(audio_data)
        self.latest_stream_time = stream_time
        stats_data = {'time': stream_time}
        self.stats_buffer.append(stats_data)
        self.audio_buffer = self.audio_buffer[-buffer_size:]
        self.stats_buffer = self.stats_buffer[-buffer_size:]

    def get_raw_audio(self, chunks):
        audio_compiled = np.concatenate(self.audio_buffer[-chunks:])
        return audio_compiled


class RawStreamProcessor:
    def __init__(self, report_interval: float = DEFAULT_REPORT_INTERVAL):
        self.buffer = AudioStreamBuffer()
        self.last_report_time: float = 0
        self.report_interval = report_interval

    def add_raw_audio(self, audio_data: np.array, stream_time: float):
        self.buffer.add(audio_data, stream_time)
        if stream_time - self.last_report_time > self.report_interval:
            self.last_report_time = stream_time
            self.report()

    def report(self, chunk_count: int = 500):
        raw_audio = self.buffer.get_raw_audio(chunk_count)
        max = raw_audio.max()
        count = len(raw_audio)
        stream_time = self.buffer.latest_stream_time
        print(f'{stream_time: 08.2f}s, max: {max: 06d} ({count} records)')


processor = RawStreamProcessor()


def process_raw_audio(audio_data: np.array, stream_time: float):
    processor.add_raw_audio(audio_data, stream_time)


def callback(in_data, frame_count, time_info, flag):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    # music = librosa.load(audio_data)

    # beat = librosa.feature.tempogram(audio_data)
    # pprint(beat)
    # Instead of printing, process here the audio chunk 'audio_data' with libROSA
    # [...]
    # pprint(audio_data)
    ad_max = audio_data.max()
    ad_min = audio_data.min()
    stream_time = st.get_stream_time(time_info['input_buffer_adc_time'])

    # pprint(f'{ad_min:06d} ---> {ad_max:06d}  {stream_time:08.3f}')
    process_raw_audio(audio_data, stream_time)

    return None, pyaudio.paContinue


def stream_audio(pa: pyaudio.PyAudio, time_limit: float = 0.0, chunk_size: int = DEFUALT_CHUNK_SIZE):
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=DEFAULT_SAMPLE_RATE,
                     output=False,
                     input=True,
                     stream_callback=callback,
                     frames_per_buffer=chunk_size)

    try:
        stream.start_stream()
        start_time = datetime.now()

        while (stream.is_active() and (
                (datetime.now() - start_time).seconds < time_limit)
                or time_limit == 0
        ):
            time.sleep(0.1)
    except Exception as e:
        raise e
    finally:
        print('cleaning up streams and pyaudio ...')
        stream.close()
        pa.terminate()


if __name__ == '__main__':
    pa = pyaudio.PyAudio()
    stream_audio(pa)
