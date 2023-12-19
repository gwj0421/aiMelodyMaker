import os

import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
from transformers import AutoProcessor, MusicgenForConditionalGeneration

from configuration.constant import MODEL_SELECTOR, AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME, LOCATION, \
    S3_SAVE_ROOT_PATH, PRESIGN_URI_EXPIRED_IN
from service.s3 import generate_presigned_url
from utils.audio import AudioUtils
from utils.check import FileNameUtils
from datetime import datetime


class MelodyModel:
    def __init__(self, description):
        self.processor = AutoProcessor.from_pretrained(MODEL_SELECTOR.get(description))
        self.model = MusicgenForConditionalGeneration.from_pretrained(MODEL_SELECTOR.get(description))
        self.sampling_rate = self.model.config.audio_encoder.sampling_rate
        self.s3 = boto3.client('s3', region_name=LOCATION, aws_access_key_id=AWS_ACCESS_KEY,
                               aws_secret_access_key=AWS_SECRET_KEY, config=Config(signature_version='s3v4'))

    def make_audio(self, texts, token_cnt):
        inputs = self.processor(
            text=texts,
            padding=True,
            return_tensors="pt",
        )
        audio_values = self.model.generate(**inputs, max_new_tokens=token_cnt)
        return audio_values

    # def upload_to_backend(self, texts, token_cnt):
    #     content = []
    #     audio_values = self.make_audio(texts, token_cnt)
    #     for i in range(audio_values.shape[0]):
    #         audio = AudioUtils.convert_numpy2bytes(audio_values[i, 0].numpy(), self.sampling_rate)
    #         encode_audio = base64.b64encode(audio)
    #         content.append(encode_audio)
    #     return content

    def upload_to_s3(self, texts, token_cnt, user_id, file_type="wav"):
        audio_values = self.make_audio(texts, token_cnt)
        content = []

        for i in range(audio_values.shape[0]):
            try:
                s3_prefix = os.path.join(S3_SAVE_ROOT_PATH, user_id, texts[i])
                file_cnt = FileNameUtils.check_s3_path_existence_and_files(BUCKET_NAME, self.s3, s3_prefix)
                audio_value = AudioUtils.convert_numpy2bytes(audio_values[i, 0].numpy(), self.sampling_rate)
                save_path = os.path.join(s3_prefix, f"{file_cnt}.{file_type}")
                self.s3.put_object(Body=audio_value, Bucket=BUCKET_NAME, Key=save_path)
                save_uris = generate_presigned_url(self.s3, "get_object", {'Bucket': BUCKET_NAME, 'Key': save_path},
                                                   PRESIGN_URI_EXPIRED_IN)

                content.append([save_path, save_uris, int(datetime.now().timestamp()) + PRESIGN_URI_EXPIRED_IN])

            except NoCredentialsError:
                print("Credentials not available")

        return content
