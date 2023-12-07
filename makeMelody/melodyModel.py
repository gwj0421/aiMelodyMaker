from configuration.constant import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME, LOCATION, S3_SAVE_ROOT_PATH
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from configuration.constant import MODEL_SELECTOR
from IPython.display import Audio, display
from scipy.io.wavfile import write
from botocore.exceptions import NoCredentialsError
from utils.audio import AudioUtils
from utils.check import FileNameUtils
import boto3
import os


class MelodyModel:
    def __init__(self, description):
        self.processor = AutoProcessor.from_pretrained(MODEL_SELECTOR.get(description))
        self.model = MusicgenForConditionalGeneration.from_pretrained(MODEL_SELECTOR.get(description))
        self.sampling_rate = self.model.config.audio_encoder.sampling_rate
        self.s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    def processInput(self, texts):
        return self.processor(text=texts, padding=True, return_tensors="pt")

    def makeAudioWithPadding(self, texts, token_cnt):
        return self.model.generate(**self.processInput(texts), max_new_tokens=token_cnt)

    def postProcess(self, audio_values, inputs):
        return self.processor.batch_decode(audio_values, padding_mask=inputs.padding_mask)

    def makeAudio(self, texts, token_cnt):
        inputs = self.processInput(texts)
        audio_values = self.makeAudioWithPadding(texts, token_cnt)
        return self.postProcess(audio_values, inputs)

    def saveAudio(self, audio_values):
        for i in range(audio_values.shape[0]):
            write(f"test_{i}.wav", rate=self.sampling_rate, data=audio_values[i, 0].numpy())

    def upload_to_s3(self, texts, token_cnt, user_id, file_type="wav"):
        audio_values = self.makeAudioWithPadding(texts, token_cnt)

        for i in range(audio_values.shape[0]):
            try:
                s3_prefix = os.path.join(S3_SAVE_ROOT_PATH, user_id, texts[i])
                file_cnt = FileNameUtils.check_s3_path_existence_and_files(BUCKET_NAME, self.s3, s3_prefix)
                audio = AudioUtils.convert_numpy2bytes(audio_values[i, 0].numpy(), self.sampling_rate)
                save_path = os.path.join(s3_prefix, f"{file_cnt}.{file_type}")
                self.s3.put_object(Body=audio, Bucket=BUCKET_NAME, Key=save_path)
            except NoCredentialsError:
                print("Credentials not available")

    def displayAudio(self, texts, token_cnt):
        audio_values = self.makeAudioWithPadding(texts, token_cnt)
        for audio in audio_values:
            display(Audio(audio.numpy(), rate=self.sampling_rate))
