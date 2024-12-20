"""
decode.py

decode is a SCTE-35 decoder function
with input type auto-detection.

SCTE-35 data can be parsed with just
one function call.

the arg stuff is the input.
if stuff is not set, decode will attempt
to read mpegts video from sys.stdin.buffer.

SCTE-35 data is printed in JSON format.

For more parsing and output control,
see the Cue and Stream classes.

"""

import sys
from sys import stdout, stderr
import logging
import json
logger = logging.getLogger('decode')

from .cue import Cue

from .stream import show_cue, show_cue_stderr, show_cue_base64, show_cue_base64_stderr
from .stream import Stream


def _read_stuff(stuff, args):
    try:
        return _read_ts(stuff, args)
    except Exception as e:
        logger.warn(f"Decode as TS failed. Retrying decode as cue...")
        try:
            return _read_cue(stuff, args)
        except Exception as e1:
            logger.error(f"Decode as cue failed")
            logger.error(e1, exc_info=True)
            return False

def _read_ts(stuff, args):
    if args.outFormat == "json":
        format_func = show_cue_stderr if args.outFile == stderr else show_cue
    elif args.outFormat == "base64":
        format_func = show_cue_base64_stderr if args.outFile == stderr else show_cue_base64
    else:
        raise Exception(f"Unexpected SCTE-35 output format '{args.outFormat}'")
    # Mpegts Video
    strm = Stream(stuff)
    strm.decode_fu(format_func)
    return True


def _read_cue(stuff, args):
    cue = Cue(stuff)
    cue.decode()
    if args.outFormat == "json":
        cue.show(args.outFile)
    elif args.outFormat == "base64":
        cue.show_base64(args.outFile)
    elif args.outFormat == "none":
        pass
    elif args.outFormat == "input+":
        pass
    else:
        raise Exception(f"Unexpected SCTE-35 output format '{args.outFormat}'")
    return True, cue.get_json()

def decode(stuff=None, args={"outFormat": "json", "outFile": stdout, "inType": None}):
    """
    decode is a SCTE-35 decoder function
    with input type auto-detection.

    SCTE-35 data is printed in JSON format.

    Use like:

    # Base64
    stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    threefive.decode(stuff)

    # Bytes
    payload = b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96"
    threefive.decode(payload)

    # Hex String
    stuff = '0XFC301100000000000000FFFFFF0000004F253396'
    threefive.decode(stuff)

    # Hex Literal
    threefive.decode(0XFC301100000000000000FFFFFF0000004F253396)

    # Integer
    big_int = 1439737590925997869941740173214217318917816529814
    threefive.decode(big_int)

    # Mpegts File
    threefive.decode('/path/to/mpegts')

    # Mpegts HTTP/HTTPS Streams
    threefive.decode('https://futzu.com/xaa.ts')

    """
    if args.inType == "base64Scte35":
        _read_cue_safe(stuff, args)
    elif args.inType == "base64Scte35File":
        if stuff == "-":
            fh = sys.stdin
        else:
            fh = open(stuff, "r", encoding="utf-8")
        with fh as file:
            for line in file:
                try:
                    words = line.strip().split()
                    base64_scte35 = words[args.inCol-1]
                    res, cue_json = _read_cue_safe(base64_scte35, args)
                    descriptors = json.loads(cue_json)["descriptors"]
                    if args.outFormat == "input+":
                        seg_type_id, upid = (str(descriptors[0].get("segmentation_type_id", "-")), descriptors[0].get("segmentation_upid", "-")) if len(descriptors) > 0 else ("-", "-")
                        words.append(seg_type_id)
                        words.append(upid)
                        print("  ".join(words))
                except Exception as e1:
                    logger.error(f"Decode line as base64 SCTE-35 failed", words)
                    #logger.error(e1, exc_info=True)
    else:
        if stuff in [None]:
            # Mpegts stream or file piped in
            stuff = sys.stdin.buffer
        elif isinstance(stuff, int):
            stuff = hex(stuff)
        return _read_stuff(stuff, args)

def _read_cue_safe(stuff, args):
        try:
            return _read_cue(stuff, args)
        except Exception as e1:
            logger.error(f"Decode as base64 SCTE-35 failed")
            logger.error(e1, exc_info=True)
            return False
