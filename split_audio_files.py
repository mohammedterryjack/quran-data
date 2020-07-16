############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from pydub import AudioSegment
from pydub.silence import split_on_silence
############   LOCAL IMPORTS   ###########################
##########################################################

FILENAME = "001"
AUDIO_FORMAT = "mp3"
PATH_TO_FFMPEG = "C:\\Users\\mdtj500\\desktop\\ffmpeg\\bin\\ffmpeg.exe"
PATH_IN = f"raw_data/audio_to_split/hamza_nuh/{FILENAME}.{AUDIO_FORMAT}"
SILENCE_IN_MILISECONDS = 1200
LOUDNESS_IN_DBFS = -16

for INDEX, audio_chunk in enumerate(
    split_on_silence(
        audio_segment=AudioSegment.from_mp3(PATH_IN), 
        min_silence_len=SILENCE_IN_MILISECONDS,
        silence_thresh=LOUDNESS_IN_DBFS,
        keep_silence=True
    )
):
    PATH_OUT = f"raw_data/audio_to_split/split_audio/{FILENAME}{str(INDEX).zfill(3)}.{AUDIO_FORMAT}"
    audio_chunk.export(PATH_OUT, format=AUDIO_FORMAT)