# The new threefive cli 

* The latest docs are always available with 

```sh
threefive help
```
* Supported Network Protocols
   * Http
   * Https
   * UDP
   * Multicast 

## decode 
<details><summary>threefive decode help</summary>

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



## encode
*  Load JSON, XML, Base64 or Hex and encode to  JSON, XML,Base64, Hex, Int or Bytes : threefive  encode  help 
    * encode can be used to convert from one SCTE-35 format to another.
<details><summary>threefive encode help </summary>

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

## HLS decode
> Development was financed by the fine folks at [tunein.com](https://tunein.com),
>  they insisted it remain freely available to everyone.
> This is by far the most advaned HLS SCTE-35 decoder available anywhere.

* Try it , you'll love it.  
```js
threefive   hls  https://example.com/master.m3u8
```
 
<details><summary>threefive hls help</summary>

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
<pre>


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


</pre>

</details>
                HLS encode  SCTE-35: threefive  hls  encode  help

    inject      Inject an mpegts stream with a SCTE-35 sidecar file at pid:  threefive  inject  video.ts  with  sidecar.txt  at  333

    mpegts      Functions for mpegts  ( packet, proxy, pts, sidecar, sixfix show, xml  ) : threefive  mpegts  help

    version     Show version: threefive  version 

    help        Help:  threefive  help 
