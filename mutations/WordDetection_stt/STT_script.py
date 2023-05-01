# custom classes and modules and packages and functions (imports)
from vosk import Model, KaldiRecognizer

# inject package
import pyaudio
import json

class STT_MODEL:
    HZ = None
    def __init__(self, HZ) -> None:
        self.HZ = HZ

    def detection(self) -> None:
        model = Model(r"mutations/WordDetection_stt/model/vosk-model-small-ru-0.22") # полный путь к модели
        rec = KaldiRecognizer(model, self.HZ)
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16, 
            channels=1, 
            rate=self.HZ,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()

        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if(rec.AcceptWaveform(data)) and (len(data) > 0):
                response = json.loads(rec.Result())
                if(response['text']):
                    yield response['text']
    def detection_(self):
        for text in self.detection():
            print(text)
            

if __name__ == '__main__':
    stt = STT_MODEL(HZ=16000)
    stt.detection_()