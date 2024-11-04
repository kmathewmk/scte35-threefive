# The new threefive cli 

## Decode SCTE-35
<details><summary><B>threefive decode help</B></summary>

* Here's how to decode SCTE-35 from MPEGTS, HLS, Base64, Hex, Files, Stdin.
 
base64:    
```js
threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='
```
hex:       
```js
threefive '0xfc301600000000000000fff00506fe00a98ac700000b3baed9'
```
files:
```js
threefive myvideo.ts
```
stdin:     
```js
cat myvideo.ts | threefive
```
http(s):
```js   
threefive https://futzu.com/xaa.ts
```
udp:
```js       
threefive udp://127.0.0.1:3535
```
multicast:
```js
threefive udp://@235.35.3.5:3535
```
hls:
```js
threefive   hls  https://example.com/master.m3u8
```


</details>


## Encode SCTE-35

<details><summary><B>threefive encode help</summary</B> </summary>

*  Load JSON, XML, Base64 or Hex and encode to  JSON, XML,Base64, Hex, Int or Bytes : threefive  encode  help 
    * encode can be used to convert from one SCTE-35 format to another.

Base64 to bytes:
```js
threefive  encode   bytes   '/DAlAAAAAAAAAP/wFAUAAAAOf+/+FOvVwP4ApMuAAA4AAAAAzBon0A=='
```
Base64 to hex:  
```js
threefive  encode   hex   '/DBCAAGRZOeYAP/wBQb/ijB9aAAsAipDVUVJAAAAAX//AABSfTABFG1zbmJjX0VQMDE3MTc0MzEyNzg2NgEBAABDk4yN'
```
Base64 to xml: 
```js
threefive  encode   xml   '/DAxAAGRZOeYAP/wFAUAAAAMf+//kCYroP4AUmXAAAAAAAAMAQpDVUVJUJ8xMjEq9sE7YA=='
```
Hex to int:     
```js
threefive  encode   int  0xfc302500000000000000fff014050000000e7feffe14ebd5c0fe00a4cb80000e00000000cc1a27d0
```
        \
JSON to base64: 
```js
threefive  encode  < json.json
```

JSON to xml:    
```js
threefive  encode   xml  < json.json
```
        
xml to hex:     
```js
cat xml.xml | threefive  encode   hex 
```

</details>

## HLS Decode SCTE-35
<details><summary><B>threefive hls help</B></summary>

* Try it , you'll like it.  
```js
threefive   hls  https://example.com/master.m3u8
```
 
* SCTE-35 can be parsed from HLS from the segments and/or the manifests.
* Single manifests and master.m3u8 manifests can be decoded.
* All HLS SCTE-35 Tags are supported.
* The parsing is configurable, you can choose which HLS SCTE-35 tags should be parsed.
* Parsing SCTE-35 from the HLS segments can be enabled or disabled.
* All MPEGTS HLS is supported as well as audio only AAC.


* Simple answer
```js
  threefive hls  https://example.com/out/v1/547e1b8d09444666ac810f6f8c78ca82/index.m3u8
```

* The details
```smalltalk


[ Help ]

    To display this help:

        threefive hls help


[ Input ]

        threefive hls takes an m3u8 URI as input.

        M3U8 formats supported:

                * master  ( When a master.m3u8 used,
                           threefive hls parses the first rendition it finds )
                * rendition

        Segment types supported:

                * AAC
                * AC3
                * MPEGTS
                *codecs:
                        * video
                                * mpeg2, h.264, h.265
                        * audio
                                * mpeg2, aac, ac3, mp3

        Protocols supported:

                * file
                * http(s)
                * UDP
                * Multicast

        Encryption supported:

                * AES-128 (segments are automatically decrypted)

[ SCTE-35 ]

    threefive hls displays SCTE-35 Embedded Cues as well as SCTE-35 HLS Tags.

    Supported SCTE-35:

        * All Commands, Descriptors, and UPIDS
          in the 2022-b SCTE-35 specification.

    Supported HLS Tags.

        * #EXT-OATCLS-SCTE35
        * #EXT-X-CUE-OUT-CONT
        * #EXT-X-DATERANGE
        * #EXT-X-SCTE35
        * #EXT-X-CUE-IN
        * #EXT-X-CUE-OUT


[ SCTE-35 Parsing Profiles ]

        SCTE-35 parsing can be fine tuned by setting a parsing profile.

        running the command:

                threefive hls profile

        will generate a default profile and write a file named sc.profile
        in the current working directory.

        a@fu:~$ cat sc.profile

        expand_cues = False
        parse_segments = False
        parse_manifests = True
        hls_tags = #EXT-OATCLS-SCTE35,#EXT-X-CUE-OUT-CONT,
        #EXT-X-DATERANGE,#EXT-X-SCTE35,#EXT-X-CUE-IN,#EXT-X-CUE-OUT
        command_types = 0x6,0x5
        descriptor_tags = 0x2
        starts = 0x22,0x30,0x32,0x34,0x36,0x44,0x46

        ( Integers are show in hex (base 16),
          base 10 unsigned integers can also be used in sc.profile )

        expand_cues:       set to True to show cues fully expanded as JSON

        parse_segments:    set to true to enable parsing SCTE-35 from MPEGTS.

        parse_manifests:   set to true to parse the m3u8 file for SCTE-35 HLS Tags.

        hls_tags:          set which SCTE-35 HLS Tags to parse.

        command_types:     set which Splice Commands to parse.

        descriptor_tags:   set which Splice Descriptor Tags to parse.

        starts:            set which Segmentation Type IDs to use to start breaks.



                Edit the file as needed and then run threefive hls.


[ Profile Formatting Rules ]

        * Values do not need to be quoted.

        * Multiple values are separated by a commas.

        * No partial line comments. Comments must be on a separate lines.

        * Comments can be started with a # or //

        * Integers can be base 10 or base 16


[ Output Files ]

        * Created in the current working directory
        * Clobbered on start of showc ues

        * Profile rules applied to the output:
              * sc.m3u8  - live playable rewrite of the m3u8
              * sc.sidecar - list of ( pts, HLS SCTE-35 tag ) pairs

        * Profile rules not applied to the output:
              * sc.dump  -  all of the HLS SCTE-35 tags read.
              * sc.flat  - every time an m3u8 is reloaded,
                           it's contents are appended to sc.flat.

[ Cool Features ]

    * threefive hls can resume when started in the middle of an ad break.

            2023-10-13T05:59:50.24Z Resuming Ad Break
            2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
            2023-10-13T05:59:50.44Z Setting Break Duration to 60.067

    * mpegts streams are listed on start ( like ffprobe )

            Program: 1
                Service:
                Provider:
                Pid:    480
                Pcr Pid:        481
                Streams:
                    Pid: 481[0x1e1]     Type: 0x1b AVC Video
                    Pid: 482[0x1e2]     Type: 0xf AAC Audio
                    Pid: 483[0x1e3]     Type: 0x86 SCTE35 Data
                    Pid: 484[0x1e4]     Type: 252 Unknown
                    Pid: 485[0x1e5]     Type: 0x15 ID3 Timed Meta Data


[ Example Usage ]

        * Show this help:

                threefive hls help

        * Generate a new sc.profile

                threefive hls profile

        * parse an m3u8

               threefive  https://example.com/out/v1/547e1b8d09444666ac810f6f8c78ca82/index.m3u8


```

</details>


## HLS Encode SCTE-35

<details><summary><B>threefive  hls  encode  help</B></summary>
  
```js
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input source, is a master.m3u8(local or http(s) with
                        MPEGTS segments default: None
  -s SIDECAR_FILE, --sidecar_file SIDECAR_FILE
                        SCTE-35 Sidecar file default: None
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        output directory default:None
  -T HLS_TAG, --hls_tag HLS_TAG
                        x_scte35, x_cue, x_daterange, or x_splicepoint
                        default: x_cue
```
* Input is a master.m3u8 file,local or over http(s), as input.
* SCTE-35 data is from a sidecar file.
* The master. m3u8 and rendition index.m3u8 files are rewritten locally on your server with SCTE-35 Added to them.
* Segments with a CUE-OUT or CUE-IN tag in them, they are split at the SCTE-35 splicepoint.
* It's fast, light on the network, and uses very little CPU time. 
---

```js
#EXTM3U
#EXT-X-VERSION:4      <--- headers and settings are copied over.
#EXT-X-TARGETDURATION:7   
#EXTINF:6.0
https://example.com/0/seg541.ts    <-- expands existing segment URI, but doesn't parse the segments
#EXTINF:0.266667
./0/a-seg542.ts       <--- When there is a SCTE-35 Cue, it splits the segment at the splice point.
#EXT-X-CUE-OUT:13.0     
#EXT-X-DISCONTINUITY
#EXTINF:5.466666
./0/b-seg542.ts      < -- the second split segment is the where the CUE-OUT starts
#EXT-X-CUE-OUT-CONT:5.466666/13.0
#EXTINF:6.0
https://example.com/0/seg543.ts     <--- during  the ad break, the segments are not parsed, URIs are expanded.
#EXT-X-CUE-OUT-CONT:11.466666/13.0
#EXTINF:1.533334
./0/a-seg544.ts            
#EXT-X-CUE-IN            
#EXT-X-DISCONTINUITY
#EXTINF:4.199999
./0/b-seg544.ts   
#EXTINF:6.0
https://example.com/0/seg545.ts   

```

* The new master.m3u8 is written to your server
* Each rendition has an index.m3u8 and just the split segments in sub directories on your server.
* Each sub-directory looks like this

```smalltalk

 ls 0/
  a-seg542.ts    b-seg542.ts 
  a-seg544.ts   b-seg544.ts  
  index.m3u8 sidecar.txt
```
* the [sidecar file](#sidecar-files) contains two lines, a CUE-OUT and a CUE-IN, the  ad break is for 17 seconds.
```smalltalk
3274.0,/DAlAAAAAAAAAP/wFAUAAAABf+/+EZAnoP4AF1iQAAEAAAAAE5sHRg==
3291.0,/DAgAAAAAAAAAP/wDwUAAAABf0/+EaeAMAABAAAAAJlXlzg=
```
* the command

```js
a@fu:~/testme$ sideways -i /home/a/foam4/master.m3u8 -s ../sidecar.txt
```

* the output
```js
a@fu:~/testme$ ls -R
.:
0  1  master.m3u8

./0:
a-seg544.ts  a-seg547.ts  b-seg544.ts  b-seg547.ts  index.m3u8  sidecar.txt

./1:
a-seg544.ts  a-seg547.ts  b-seg544.ts  b-seg547.ts  index.m3u8  sidecar.txt
```
* 0 and 1 are renditon sub-directories.
* When a segment is split for SCTE-35 the name is prepended with a- and b-
* sideways  writes a copy of the sidecar to each rendition directory
* you can play the master.m3u8.
* the SCTE-35 Cues come out like this:
```js
# start: 3268.266667 
#EXTINF:5.733333
./0/a-seg544.ts     <-- seg544.ts is split into a-seg544.ts and b-seg544.ts.
# start: 3274.0 
#EXT-X-CUE-OUT:17.0
#EXT-X-DISCONTINUITY
#EXTINF:0.266667
./0/b-seg544.ts <-- The splice point is always at the start of b- segment.
# start: 3274.266667 
#EXT-X-CUE-OUT-CONT:0.266667/17.0
#EXTINF:6.0
/home/a/foam4/0/seg545.ts  
# start: 3280.266667 
#EXT-X-CUE-OUT-CONT:6.266667/17.0
#EXTINF:6.0
/home/a/foam4/0/seg546.ts
# start: 3286.266667 
#EXT-X-CUE-OUT-CONT:12.266667/17.0
#EXTINF:4.733333
./0/a-seg547.ts
# start: 3291.0 
#EXT-X-CUE-IN
#EXT-X-DISCONTINUITY
#EXTINF:1.266667
./0/b-seg547.ts
# start: 3292.266667 
```   
### Sidecar files
* load scte35 cues from a Sidecar file

* Sidecar Cues will be handled the same as SCTE35 cues from a video stream.
* line format for text file insert_pts, cue

* pts is the insert time for the cue, cue can be base64,hex, int, or bytes
```lua
a@debian:~/sidweways$ cat sidecar.txt

38103.868589, /DAxAAAAAAAAAP/wFAUAAABdf+/+zHRtOn4Ae6DOAAAAAAAMAQpDVUVJsZ8xMjEqLYemJQ== 
38199.918911, /DAsAAAAAAAAAP/wDwUAAABef0/+zPACTQAAAAAADAEKQ1VFSbGfMTIxIxGolm0= 
```
* you can do dynamic cue injection with a Sidecar file
```lua
touch sidecar.txt

sideways -i master.m3u8 -s sidecar.txt -o bob
```
*  Open another terminal and printf cues into sidecar.txt
```lua
printf '38103.868589, /DAxAAAAAAAAAP/wFAUAAABdf+/+zHRtOn4Ae6DOAAAAAAAMAQpDVUVJsZ8xMjEqLYemJQ==\n' > sidecar.txt
```

* A CUE-OUT can be terminated early using a sidecar file.

</details>


## Inject  SCTE-35   
* Inject an mpegts stream with a SCTE-35 sidecar file at pid:  
```js
threefive  inject  video.ts  with  sidecar.txt  at  333
```

## MPEGTS 
    
<details><summary><B>threefive mpegts help</B></summary>

* packets         Print raw SCTE-35 packets from multicast mpegts video:  
```js
threefive  mpegts   packets  udp://@235.35.3.5:3535
```
* proxy           Parse a https stream and write raw video to stdout:  
```js
threefive  mpegts   proxy  https://example.com/video.ts
```
* pts             Print PTS from mpegts video:  
```js
threefive  mpegts   pts  video.ts
```
* sidecar         Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt:  
```js
threefive  mpegts   sidecar  https://example.com/video.ts
```
* sixfix          Fix SCTE-35 data mangled by ffmpeg:  ```js
threefive  mpegts   sixfix  video.ts
```
* show            Probe mpegts video:  
```js 
threefive  mpegts   show  video.ts
```
*xml             Parse an mpegts stream and output xml: 
```js
threefive  mpegts   xml  video.ts
```

</details>

