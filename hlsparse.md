## The coolest new feature in the threefive cli is the HLS SCTE-35 parser.


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





The fine folks at [__tunein.com__](https://tunein.com) paid for the developement of __threefive hls__ and insisted it remain open and freely available to everyone. 
[__tunein.com__](https://tunein.com) has been using this code __in production since 2022__ to parse SCTE-35 from thousands of sources.
They see more SCTE-35 in a week, than you ever will
This is the exact same code they have been using..

you run it like this:

```awk
threefive hls https://example.com/master.m3u8
```
[ __Help__ ]

To display this help:
```sed
  threefive hls help
```

[ __Input__ ]

threefive hls takes an m3u8 URI as input.

 __M3U8 formats supported__:

* master  ( When a master.m3u8 used, threefive hls parses the first rendition it finds )
* rendition

 __Segment types supported__

* AAC
* AC3
* MPEGTS
    * codecs:
        * video
             * mpeg2, h.264, h.265
          * audio
             * mpeg2, aac, ac3, mp3

 __Protocols supported__:

  * file
  * http(s)
  * UDP
  * Multicast

 __Encryption supported__:

 * AES-128 (segments are automatically decrypted)

[ __SCTE-35__ ]

threefive hls displays SCTE-35 Embedded Cues as well as SCTE-35 HLS Tags.

Supported HLS Tags.

  * #EXT-OATCLS-SCTE35
  * #EXT-X-CUE-OUT-CONT
  * #EXT-X-DATERANGE
  * #EXT-X-SCTE35
  * #EXT-X-CUE-IN
  * #EXT-X-CUE-OUT


 [__Profiles and .35rc__]
* A lot of companies have multiple SCTE-35 Tags and/or SCTE-35 embedded inthe segments. threefive hls allows you to set what you parse. This is tunable via a file called __.35rc__
* to generate .35rc run the following
```js
threefive hls profile
```
* it will creat .35rc in the current directory

```js
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
( Integers are show in hex (base 16),
          base 10 unsigned integers can also be used in .35rc )


__expand_cues:__       `set to True to show cues fully expanded as JSON`


__parse_segments:__    `set to true to enable parsing SCTE-35 from MPEGTS.`

__parse_manifests:__   `set to true to parse the m3u8 file for SCTE-35 HLS Tags.`

__hls_tags:__          `set which SCTE-35 HLS Tags to parse.`

__command_types:__     `set which Splice Commands to parse.`

__descriptor_tags:__   `set which Splice Descriptor Tags to parse.`

__starts:__            `set which Segmentation Type IDs to use to start breaks.`



Edit the file as needed and then run threefive hls from the same directory.


[__Profile Formatting Rules__ ]

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

* __ALL SCTE-35 HLS tags are supported__.
* SCTE-35 can also be parsed from segments.

* __Automatic AES Decryption__, you don't  have to do anything, __threefive hls __
 __automatically detects and decrypts AES encrypted segments__ on the fly.


*  Preroll and  splice point and diff of the splice point are displayed.
```js
                                                                                
2024-11-08T13:01:49.60Z  SCTE-35 
                        Stream PTS: 71317.660444
                        PreRoll: 4.090678
                        Splice Point: 71321.751122
                        Type: Time Signal
                        Media: index_2_8638662.ts

                             
```

* mpegts streams are listed on start ( like ffprobe )
```js
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
```js


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
```js
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

 
