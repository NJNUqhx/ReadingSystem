# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:07:23 2022

@author: lenovo
"""
from aip import AipSpeech
from ffmpy import FFmpeg
import os


# url='http://vop.baidu.com/server_api'


class Voice:
    def __init__(self):

        self.APP_ID = '28539468'

        self.API_KEY = '1WVq0iD4wgafFlyR6iaTeSVw'
        self.SECRET_KEY = 'hytBUK1zPCBL1eYYU71GRGLpoDeriSSD'
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.frame_rate = 16000
        self.num_samples = 2000
        self.n_channels = 1
        self.samp_width = 2

    def recognize(self, file):
        with open(file, 'rb') as f:
            data = f.read()
        result = self.client.asr(data, 'wav', 16000, {'dev_pid': 1536})
        return result['result'][0] if 'result' in result else result

    def mp3towav(self, file, output_dir):
        fmt = os.path.basename(file).strip().split('.')[-1]
        if fmt != 'mp3':
            raise Exception('该文件不是MP3格式')
        result = os.path.join(output_dir, '{}.{}'.format(os.path.basename(file).strip().split('.')[0], 'wav'))
        cmder = '-f wav -ac 1 -ar 16000'
        path = "D:\\MyDownload\\ffmpeg-5.1.2-full_build\\bin\\ffmpeg.exe"
        ff = FFmpeg(executable=path, inputs={file: None}, outputs={result: cmder})
        ff.run()
        return result

    # def record(self, file, seconds):
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=pyaudio.paInt16, channels=self.n_channels, rate=self.frame_rate, input=True,
    #                     frames_per_buffer=self.num_samples)
    #     buf = []
    #     t = time.time()
    #     while time.time() < t + seconds:
    #         data = stream.read(self.num_samples)
    #         buf.append(data)
    #     wf = wave.open(file, 'wb')
    #     wf.setnchannels(self.n_channels)
    #     # wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    #     wf.setsampwidth(self.samp_width)
    #     wf.setframerate(self.frame_rate)
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #     wf.writeframes(b''.join(buf))
    #     wf.close()

    # def play(self, file):
    #     p = pyaudio.PyAudio()
    #     wf = wave.open(file, 'rb')
    #     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
    #                     rate=wf.getframerate(), output=True)
    #     data = wf.readframes(self.num_samples)
    #     while len(data) > 0:
    #         stream.write(data)
    #         data = wf.readframes(self.num_samples)
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #     wf.close()


voice = Voice()