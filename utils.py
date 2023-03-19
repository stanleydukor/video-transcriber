import os
from pydub import AudioSegment
import speech_recognition as sr
import moviepy.editor as mp
from variables import *
import math


class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename

        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self):
        return self.audio.duration_seconds

    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(
            self.folder + f'/{TEMP_DIR}/' + split_filename, format='wav')

    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        count = 1
        for i in range(0, total_mins, min_per_split):
            split_fn = '0'*count + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            count += 1
            if i == total_mins - min_per_split:
                print('All splited successfully')


def transcribe(source, destination):
    filename, file_extension = os.path.splitext(source)
    if file_extension.lower() in ['.mp4', '.avi', '.mobi']:
        clip = mp.VideoFileClip(source)
        clip.audio.write_audiofile(f'{filename}.wav')
    if file_extension.lower() == '.mp3':
        sound = AudioSegment.from_mp3(source)
        sound.export(f'{filename}.wav', format='wav')

    audioSplitter = SplitWavAudioMubin('.', f'{filename}.wav')
    audioSplitter.multiple_split(2)

    totalResult = ''
    for i in reversed(os.listdir(TEMP_DIR)):
        print(i)
        r = sr.Recognizer()
        audio = sr.AudioFile(os.path.join(TEMP_DIR, i))
        with audio as source:
            r.adjust_for_ambient_noise(source, duration=2)
            audio_file = r.record(source)
        result = r.recognize_google(audio_file, language='en-US')
        totalResult = totalResult + '\n' + result

    with open(f'{destination}.txt', mode='w') as file:
        file.write(totalResult)
        print('ready!')
