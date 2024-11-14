# The new threefive cli 

## Decode SCTE-35
<details><summary><B>threefive decode help</B></summary>

* __Here's how to decode SCTE-35 from MPEGTS, HLS, Base64, Hex, Files, Stdin__
![image](https://github.com/user-attachments/assets/b646d89e-c318-4449-a2da-728520776f86)


</details>


## Encode SCTE-35

<details><summary><B>threefive encode help</summary</B> </summary>

*  Load JSON, XML, Base64 or Hex and encode to  JSON, XML,Base64, Hex, Int or Bytes : threefive  encode  help 
    * encode can be used to convert from one SCTE-35 format to another.
![image](https://github.com/user-attachments/assets/3e61dc4c-7072-4617-9f9a-796e871faf18)

</details>

## HLS Decode SCTE-35
#### short answer:
* threfive hls will parse an m3u8 manifest as well as MPEGTS for SCTE-35.
* Ad breaks splice points  elapsed time, PTS, SCTE-35 preroll and SCTE-35 Cues are displayed
* SCTE-35 Ad break SCTE-35 criteria is adjustable, you can define a CUE-OUT and CUE-IN.

<details><summary><B>threefive hls help</B></summary>
   
## The coolest new feature in the threefive cli is the HLS SCTE-35 parser.

The fine folks at [__tunein.com__](https://tunein.com) paid for the developement of __threefive hls__ and insisted it remain open and freely available to everyone. 


```rebol
2024-11-08T12:47:54.38Z  SCTE-35 
                        Stream PTS: 70485.651111
                        PreRoll: 3.300011
                        Splice Point: 70488.951122
                        Type: Time Signal
                        Media: index_2_8638521.ts

                                                                                
2024-11-08T12:47:59.47Z  Skipped   #EXT-OATCLS-SCTE35:/DBAAAAAAyiYAAAABQb/6+8nkAAqAihDVUVJ/////3/
/AAFyylgBFG1zbmJjX0VQMDAwMjEzOTAyNTg3IwcLr6+cHw==

                        PTS: 70489.651111
                        Media: index_2_8638523.ts

                                                                                
2024-11-08T12:47:59.47Z #EXT-X-CUE-OUT:60.068

                        PTS: 70489.651111 (Splice Point)
                        Duration: 60.068
                        Media: index_2_8638523.ts
```


you run it like this:

```awk
threefive hls https://example.com/master.m3u8
```
[ __Help__ ]

To display this help:
```sed
  threefive hls help
```

[ Input ]

__threefive hls__ takes an m3u8 URI as input.

 [ M3U8 formats ]

* master  ( When a master.m3u8 used, threefive hls parses the first rendition it finds )
* rendition

[ Segment types ]

* AAC
* AC3
* MPEGTS
    * codecs:
      * video
        * mpeg2, h.264, h.265
      * audio
        * mpeg2, aac, ac3, mp3

[ Protocols ]

  * file
  * http(s)
  * UDP
  * Multicast

 [ Encryption ]

 * AES-128 (segments are automatically decrypted)

[ HLS SCTE-35 Tags ]

threefive hls displays SCTE-35 Embedded Cues as well as SCTE-35 HLS Tags.

Supported:

  * #EXT-OATCLS-SCTE35
  * #EXT-X-CUE-OUT-CONT
  * #EXT-X-DATERANGE
  * #EXT-X-SCTE35
  * #EXT-X-CUE-IN
  * #EXT-X-CUE-OUT


[ Profiles ]
* A lot of companies have multiple SCTE-35 Tags and/or SCTE-35 embedded inthe segments. threefive hls allows you to set what you parse. This is tunable via a file called __.35rc__
* to generate .35rc run the following
```awk
threefive hls profile
```
* it will creat .35rc in the current directory
( Integers are show in hex (base 16),
          base 10 unsigned integers can also be used in .35rc )
```awk
  a@fu:~$ cat .35rc

        expand_cues = False
        parse_segments = False
        parse_manifests = True
        hls_tags = #EXT-OATCLS-SCTE35,#EXT-X-CUE-OUT-CONT,
        #EXT-X-DATERANGE,#EXT-X-SCTE35,#EXT-X-CUE-IN,#EXT-X-CUE-OUT
        command_types = 0x6,0x5
        descriptor_tags = 0x2
        starts = 0x22,0x30,0x32,0x34,0x36,0x44,0x46
```

expand_cues:       `set to True to show cues fully expanded as JSON`


parse_segments:   `set to true to enable parsing SCTE-35 from MPEGTS.`

parse_manifests:   `set to true to parse the m3u8 file for SCTE-35 HLS Tags.`

hls_tags:       `set which SCTE-35 HLS Tags to parse.`

command_types:     `set which Splice Commands to parse.`

descriptor_tags:   `set which Splice Descriptor Tags to parse.`

starts:           `set which Segmentation Type IDs to use to start breaks.`

_(Edit the file as needed and then run threefive hls from the same directory)_


[ Profile Format ]

* Values do not need to be quoted.

* Multiple values are separated by a commas

* No partial line comments. Comments must be on a separate lines.

* Comments can be started with a # or //
* Integers can be base 10 or base 16

* __threefive hls__ genrates a few output files to make it easier to debug live HLS with SCTE-35


[__Output Files__]

* Created in the current working directory
* __Output files aree Clobbered on start of threefive hls__
* this is done to prevent old files from stacking up.
*  If you want to keep a file, rename it before restarting __threefve hls__ 
    * Profile rules applied to the output:
        * __35.m3u8__  - live playable rewrite of the m3u8 
        * __35.sidecar__ - list of ( pts, HLS SCTE-35 tag ) pairs

* Profile rules not applied to the output:
   * __35.dump__  -  all of the HLS SCTE-35 tags read.
   * __35.flat__  - every time an m3u8 is reloaded, it's contents are appended to 35.flat.


[  Cool Features  ]

* ALL SCTE-35 HLS tags are supported.
* SCTE-35 can be parsed from segments and manifests.

* Automatic AES Decryption, you don't  have to do anything, __threefive hls __
 __automatically detects and decrypts AES encrypted segments__ on the fly.


*  Preroll and  splice point and diff of the splice point are displayed.
```awk
                                                                                
2024-11-08T13:01:49.60Z  SCTE-35 
                        Stream PTS: 71317.660444
                        PreRoll: 4.090678
                        Splice Point: 71321.751122
                        Type: Time Signal
                        Media: index_2_8638662.ts

                             
```

* mpegts streams are listed on start ( like ffprobe )
```awk
  Program: 1

        Service:  
        Provider: 
        Pid:      480
        Pcr Pid:  481
        Streams:
          Pid           Type
          481 [0x1e1]   0x1b    H.264
          482 [0x1e2]   0xf     ADTS AAC 
          483 [0x1e3]   0x86    SCTE-35
          484 [0x1e4]   0xfc    KLV
          485 [0x1e5]   0x15    ID
```
* profile settings are also displayed on start
```awk


Profile:

    expand_cues = False

    parse_segments = True

    parse_manifests = True

    hls_tags = ['#EXT-OATCLS-SCTE35', '#EXT-X-DATERANGE', '#EXT-X-SCTE35', '#EXT-X-CUE-OUT', '#EXT-X-CUE-OUT-CONT', '#EXT-X-CUE-IN']

    command_types = ['0x5', '0x6']

    descriptor_tags = ['0x2']

    starts = ['0x22', '0x30', '0x32', '0x34', '0x36', '0x44', '0x46']

    seg_type = ['']
```
* current wall time and PTS is displayed while threefive hls is parsing.
```awk
24-11-08T12:39:19.02Z  PTS  69935.651111 

```
* break duration and break progress are displayed during ad breaks
```js
2024-11-08T13:00:43.25Z  PTS  71253.384444  Break  203.967 / 270.035
```
* PTS is parsed directly from the HLS segments for accuracy.

* threefive hls can resume when started in the middle of an ad break.
```js
2023-10-13T05:59:50.24Z Resuming Ad Break
2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
2023-10-13T05:59:50.44Z Setting Break Duration to 60.067
```

[ Example Usage ]

 * Show this help:
```sed
   threefive hls help
```
  * Generate a new .35rc
```sed
    threefive hls profile
```
* parse an m3u8
```sed
   threefive hls  https://example.com/out/v1/547e1b8d09444666ac810f6f8c78ca82/index.m3u8
```

 

[ Example Usage ]

        * Show this help:

                threefive hls help

        * Generate a new sc.profile

                threefive hls profile

        * parse an m3u8

               threefive  https://example.com/out/v1/547e1b8d09444666ac810f6f8c78ca82/index.m3u8



</details>


## HLS Encode SCTE-35
#### short answer:
   * threefive hls encode takes an HLS master.m3u8 and a SCTE-35 sidecar file and generates HLS manifests with SCTE-35 HLS tags.
   * It works on live feeds, and threefive can run along side an encodre, in realtime.
   *  thrreefine can insert any HLS SCTE-35 tag type.
     
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
```sed
a@debian:~/sidweways$ cat sidecar.txt

38103.868589, /DAxAAAAAAAAAP/wFAUAAABdf+/+zHRtOn4Ae6DOAAAAAAAMAQpDVUVJsZ8xMjEqLYemJQ== 
38199.918911, /DAsAAAAAAAAAP/wDwUAAABef0/+zPACTQAAAAAADAEKQ1VFSbGfMTIxIxGolm0= 
```
* you can do dynamic cue injection with a Sidecar file
```asm
touch sidecar.txt

sideways -i master.m3u8 -s sidecar.txt -o bob
```
*  Open another terminal and printf cues into sidecar.txt
```asm
printf '38103.868589, /DAxAAAAAAAAAP/wFAUAAABdf+/+zHRtOn4Ae6DOAAAAAAAMAQpDVUVJsZ8xMjEqLYemJQ==\n' > sidecar.txt
```

* A CUE-OUT can be terminated early using a sidecar file.

</details>


## Inject  SCTE-35   
* Inject an mpegts stream with a SCTE-35 sidecar file at pid:  
```asm
threefive  inject  video.ts  with  sidecar.txt  at  333
```

## MPEGTS 
    
* threefive mpegts help

### packets
* Print raw SCTE-35 packets from multicast mpegts video:  
```asm
threefive  mpegts   packets  udp://@235.35.3.5:3535
```
### proxy
* Parse a https stream and write raw video to stdout:  
```asm
threefive  mpegts   proxy  https://example.com/video.ts
```
### pts
* Print PTS from mpegts video:  
```asm
threefive  mpegts   pts  video.ts
```
### sidecar
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt:
```asm
 threefive  mpegts   sidecar  https://example.com/video.ts
```
### sixfix
* Fix SCTE-35 data mangled by ffmpeg:
```asm
   threefive  mpegts   sixfix  video.ts
```
### show
* Probe mpegts video:  
```asm
threefive  mpegts   show  video.ts
```
### xml
* Parse an mpegts stream and output xml: 
```asm
threefive  mpegts   xml  video.ts
```



