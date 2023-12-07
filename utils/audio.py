from scipy.io.wavfile import write
import io

class AudioUtils:
    @staticmethod
    def getListFromData(inputs,identifier):
        return inputs.split(identifier)

    @staticmethod
    def convert_numpy2bytes(numpy_array, sample_rate=44100):
        # WAV 파일로 저장하지 않고 NumPy 배열을 바이트로 변환
        wav_file = io.BytesIO()
        write(wav_file, sample_rate, numpy_array)
        wav_bytes = wav_file.getvalue()
        return wav_bytes