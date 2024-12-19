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

epilog = """
Sample Usage:\n
  python3 dec35.py --outFile stdout --outFormat json tsdir
  python3 dec35.py --outFile stdout --outFormat json test.ts
  python3 dec35.py --outFile stderr --outFormat base64 test.ts
  python3 dec35.py --outFile stdout --outFormat base64 "/DAsAAAgo7rtAP/wBQb/33AAuQAWAhRDVUVJAA0f3X//AAApvnUAADAAAB+Ivbs="
  python3 dec35.py --outFile stdout --outFormat base64 0xfc302c000020a3baed00fff00506ffdf7000b90016021443554549000d1fdd7fff000029be7500003000001f88bdbb
  python3 dec35.py --outFile stdout --outFormat base64 fc302c000020a3baed00fff00506ffdf7000b90016021443554549000d1fdd7fff000029be7500003000001f88bdbb
  # read base64 scte35 from 2nd column of stdin and output input along with a snippet of decode
  python3 dec35.py --inType base64Scte35File --inCol 2 --outFormat input+ -
"""
class CustomFormatter(argparse.RawTextHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

parser = argparse.ArgumentParser(epilog=epilog, formatter_class=CustomFormatter)
parser.add_argument("--outFormat", choices=["json", "base64", "input+", "none"], default="json", help="Prints SCTE-35 in the specified format\n  json  SCTE-35 JSON representation\n  base64  Base-64 representation\n  input+  Input suffixed with snippet of decode\n  none  No output")
parser.add_argument("--outFile", choices=["stdout", "stderr"], default="stdout", help="Prints SCTE-35 to the specified file")
parser.add_argument("--inType", choices=["tsFile", "tsDir", "base64Scte35", "base64Scte35File"], default=None, help="Specifies the type of input\n  tsFile  MPEG-2 TS file\n  tsDir  Directory containing MPEG-2 TS files\n  base64Scte35  SCTE-35 base-64 representation\n  base64Scte35File  File containing SCTE-35 base-64 representations (one per line)")
parser.add_argument("--inCol", default=1, type=int, help="Column position of input in each line")
parser.add_argument("input", help="One of:\nTS File\nDirectory containing TS files\nSCTE-35 as base64 or hex\nFile containing SCTE-35 as base64 or hex")
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
