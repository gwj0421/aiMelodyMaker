import boto3


class FileNameUtils:
    @staticmethod
    def check_s3_path_existence_and_files(bucket, s3, s3_prefix):
        # 폴더당 1000개까지 지원
        objects = s3.list_objects_v2(Bucket=bucket, Prefix=s3_prefix)

        # 경로의 존재 여부 확인
        path_exists = 'Contents' in objects

        # 경로에 있는 파일 개수 확인
        file_cnt = len(objects.get('Contents', [])) if path_exists else 0

        return file_cnt