from scipy.io.wavfile import write
from IPython.display import Audio, display

import io

class AudioUtils:
    @staticmethod
    def convert_numpy2bytes(numpy_array, sample_rate=44100):
        # numpy to wav ByteIo
        wav_file = io.BytesIO()
        write(wav_file, sample_rate, numpy_array)
        wav_bytes = wav_file.getvalue()
        return wav_bytes

    @staticmethod
    def save_audio(audio_values,sampling_rate):
        for i in range(audio_values.shape[0]):
            write(f"test_{i}.wav", rate=sampling_rate, data=audio_values[i, 0].numpy())

    @staticmethod
    def display_audio(audio_values,sampling_rate):
        for i in range(audio_values.shape[0]):
            display(Audio(audio_values[i,0].numpy(), rate=sampling_rate))
