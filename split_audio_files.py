############   NATIVE IMPORTS  ###########################
from argparse import ArgumentParser
from os import listdir
############ INSTALLED IMPORTS ###########################
from pydub import AudioSegment
from pydub.silence import split_on_silence
############   LOCAL IMPORTS   ###########################
##########################################################
def split_audio_file(path:str,filename:str) -> None:
    PATH_IN = f"{path}{filename}.{AUDIO_FORMAT}"
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
parser.add_argument("--path",default="raw_data/audio_to_split/")
parser.add_argument("--filename_startswith")
parser.add_argument("--filename")
parser.add_argument("--filename_2")
parser.add_argument("--silence",type=int,default=1000)
parser.add_argument("--loudness",type=int,default=-16)
args = parser.parse_args()

AUDIO_FORMAT = "mp3"
SILENCE_IN_MILISECONDS = args.silence
LOUDNESS_IN_DBFS = args.loudness

if args.split:
    if args.filename_startswith:
        filenames = list(
            name.replace(f".{AUDIO_FORMAT}","") for name in listdir(args.path) if name.startswith(args.filename_startswith) and name.endswith(f".{AUDIO_FORMAT}")
        )
        input(f"{filenames}")
        for filename in filenames:
            split_audio_file(path=args.path,filename=filename)
    else:
        split_audio_file(path=args.path,filename=args.filename)

if args.merge:
    join_two_audio_files(filename_1=args.filename, filename_2=args.filename_2)