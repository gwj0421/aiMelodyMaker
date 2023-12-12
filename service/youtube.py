# from configuration.constant import LOCAL_YOUTUBE_SAVE_ROOT_PATH
# import pytube
# import os
# import librosa
#
#
# def download_youtube_audio(url):
#     # YouTube 동영상을 가져옵니다.
#     video = pytube.YouTube(url)
#
#     # 음성 스트림을 가져옵니다.
#     audio_stream = video.streams.filter(only_audio=True).first()
#     filename = f"{video.title}.wav"
#     file_path = os.path.join(LOCAL_YOUTUBE_SAVE_ROOT_PATH, filename)
#
#     if not os.path.exists(file_path):
#         # 음성 스트림을 다운로드합니다.
#         audio_stream.download(LOCAL_YOUTUBE_SAVE_ROOT_PATH,filename)
#     return file_path
#
# def get_audio_from_youtube_uri(url):
#     y, _ = librosa.load(download_youtube_audio(url))
#     return y