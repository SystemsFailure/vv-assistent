import struct
import pyaudio
import pvporcupine

# custom classes and modules and packages and functions (imports)
from commands.command_ import ResponseVoice_on_command
from .WordDetection_stt.STT_script import STT_MODEL

print(pvporcupine.KEYWORDS)

porcupine = None
pa = None
audio_stream = None

def wake_word_detection():
    try:
        stt_model = STT_MODEL(HZ=44100)
        response_on_command = ResponseVoice_on_command(size_chunk=1024)
        porcupine = pvporcupine.create(access_key='CLhQ60JK5sY7IGR1BSPeq4a4e+PIRGQ2lJVogYHEm3NtJaAAu/tcbQ==', keyword_paths=['mutations/model_wake_word/arbalest_en_windows_v2_2_0.ppn'])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            # If detect successful
            if keyword_index >= 0:
                # main command mean yes, sir?
                response_on_command.call(path_file='tests/0001.wav')
                audio_stream.close()
                stt_model.detection_()
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()