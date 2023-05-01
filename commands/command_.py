import wave
import pyaudio
import os
    
# this is class for use response on the question from some man
class ResponseVoice_on_command:
    def __init__(self, size_chunk) -> None:
        self.CHUNK = size_chunk
    
    def call(self, path_file:str) -> None:
        if(os.path.exists(path_file) is False):
            print('so path: {} not found'.format(path_file))
            return
        with wave.open(path_file, 'rb') as wf:
            p = pyaudio.PyAudio()
            # Open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # Play samples from the wave file (3)
            while len(data := wf.readframes(self.CHUNK)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            # Release PortAudio system resources (5)
            stream.close()
            p.terminate()