from genericpath import isdir
import sys

#from threefive import Cue
# print()
# b64 = sys.argv[1]
# scte35 = Cue(b64)
# scte35.decode()
# scte35.show()

import threefive
import os
import logging

logging.basicConfig(level=logging.WARN)

# base64
# ts file
input = sys.argv[1]
if os.path.isdir(input):
    dir = input
    for dirent in os.scandir(dir):
        if dirent.is_file() and dirent.path.endswith(".ts"):
            print(dirent.path.encode(sys.stdout.encoding, errors='replace'))
            threefive.decode(dirent.path)
else:
    threefive.decode(input)
