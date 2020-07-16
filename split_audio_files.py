############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from pydub import AudioSegment
from pydub.silence import split_on_silence
############   LOCAL IMPORTS   ###########################
##########################################################

FILENAME = "bla"
AUDIO_FORMAT = "mp3"
PATH_IN = f"raw_data/audio_to_split/{FILENAME}.{AUDIO_FORMAT}"
SILENCE_IN_MILISECONDS = 500
LOUDNESS_IN_DBFS = -16

for index, audio_chunk in enumerate(
    split_on_silence(
        audio_segment=AudioSegment.from_mp3(PATH_IN), 
        min_silence_len=SILENCE_IN_MILISECONDS,
        silence_thresh=LOUDNESS_IN_DBFS
    )
):
    PATH_OUT = f"raw_data/audio_to_split/split_audio/{FILENAME}_{INDEX}.{AUDIO_FORMAT}"
    audio_chunk.export(PATH_OUT, format=AUDIO_FORMAT)