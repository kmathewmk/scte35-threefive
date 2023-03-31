from genericpath import isdir
import sys
from sys import stdout, stderr

#from threefive import Cue
# print()
# b64 = sys.argv[1]
# scte35 = Cue(b64)
# scte35.decode()
# scte35.show()

import threefive
import os
import logging
import argparse
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger('dec35')

# Usage:
# python3 dec35.py --outFile stdout --outFormat json tsdir
# python3 dec35.py --outFile stdout --outFormat json test.ts
# python3 dec35.py --outFile stderr --outFormat base64 test.ts
# python3 dec35.py --outFile stdout --outFormat base64 "/DAsAAAgo7rtAP/wBQb/33AAuQAWAhRDVUVJAA0f3X//AAApvnUAADAAAB+Ivbs="
# python3 dec35.py --outFile stdout --outFormat base64 0xfc302c000020a3baed00fff00506ffdf7000b90016021443554549000d1fdd7fff000029be7500003000001f88bdbb
# python3 dec35.py --outFile stdout --outFormat base64 fc302c000020a3baed00fff00506ffdf7000b90016021443554549000d1fdd7fff000029be7500003000001f88bdbb

parser = argparse.ArgumentParser()
parser.add_argument("--outFormat", choices=["json", "base64"], default="json", help="Prints SCTE-35 in the specified format")
parser.add_argument("--outFile", choices=["stdout", "stderr"], default="stdout", help="Prints SCTE-35 to the specified file")
parser.add_argument("input", help="TS File / directory containing TS files / SCTE-35 as base64 or hex string")
args = parser.parse_args()

#logger.info(args.input)
args.outFile = stderr if args.outFile == "stderr" else stdout

if os.path.isdir(args.input):
    dir = args.input
    for dirent in os.scandir(dir):
        if dirent.is_file() and dirent.path.endswith(".ts"):
            print(f"tsFile: {dirent.path}")
            #print(dirent.path.encode(sys.stdout.encoding, errors='replace'))
            threefive.decode(dirent.path, args)
            print()
else:
    threefive.decode(args.input, args)
