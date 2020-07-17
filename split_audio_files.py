############   NATIVE IMPORTS  ###########################
from argparse import ArgumentParser
############ INSTALLED IMPORTS ###########################
from pydub import AudioSegment
from pydub.silence import split_on_silence
############   LOCAL IMPORTS   ###########################
##########################################################
def split_audio_file(filename:str) -> None:
    PATH_IN = f"raw_data/audio_to_split/hamza_nuh/{filename}.{AUDIO_FORMAT}"
    for INDEX, audio_chunk in enumerate(
        split_on_silence(
            audio_segment=AudioSegment.from_mp3(PATH_IN), 
            min_silence_len=SILENCE_IN_MILISECONDS,
            silence_thresh=LOUDNESS_IN_DBFS,
            keep_silence=True
        )
    ):
        PATH_OUT = f"raw_data/audio_to_split/split_audio/{filename}{str(INDEX).zfill(3)}.{AUDIO_FORMAT}"
        audio_chunk.export(PATH_OUT, format=AUDIO_FORMAT)

def join_two_audio_files(filename_1:str,filename_2:str) -> None:
    PATH = "raw_data/audio_to_split/split_audio"
    chunk_1 = AudioSegment.from_mp3(f"{PATH}/{filename_1}.{AUDIO_FORMAT}")
    chunk_2 = AudioSegment.from_mp3(f"{PATH}/{filename_2}.{AUDIO_FORMAT}")
    chunk_combined = chunk_1 + chunk_2 
    PATH_OUT = f"{PATH}/{filename_1}.{AUDIO_FORMAT}"
    chunk_combined.export(PATH_OUT, format=AUDIO_FORMAT)


parser = ArgumentParser()
parser.add_argument("--split",action="store_true",default=False)
parser.add_argument("--merge",action="store_true",default=False)
parser.add_argument("--filename")
parser.add_argument("--filename_2")
parser.add_argument("--silence",type=int,default=1000)
args = parser.parse_args()

SILENCE_IN_MILISECONDS = args.silence
AUDIO_FORMAT = "mp3"
PATH_TO_FFMPEG = "C:\\Users\\mdtj500\\desktop\\ffmpeg\\bin\\ffmpeg.exe"
LOUDNESS_IN_DBFS = -16

if args.split:
    split_audio_file(filename=args.filename)

if args.merge:
    join_two_audio_files(filename_1=args.filename, filename_2=args.filename_2)