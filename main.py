import os
import shutil
import argparse
from variables import *
from utils import SplitWavAudioMubin, transcribe

parser = argparse.ArgumentParser(
    description='Automatic Video & Audio Transcriber')
parser.add_argument(
    '-s', '--source', help='Path to load file', required=True)
parser.add_argument(
    '-d', '--destination', help='Path to save file', required=True)
args = vars(parser.parse_args())


def run():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    transcribe(args['source'], args['destination'])
    shutil.rmtree(TEMP_DIR)


if __name__ == '__main__':
    run()
