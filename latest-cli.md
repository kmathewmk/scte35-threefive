# The threefive cli tool
   * [decode](#decode) __Decode SCTE-35.__ _this is the default action._
   * [encode](#encode) __Encode SCTE-35__ _and convert SCTE-35 formats._
   * [hls](#hls) __HLS SCTE-35 Decoding and Encoding.__
   * [xml](#xml)  __Xml__ _output for_ _SCTE-35.__
   * [inject](#inject) __Inject SCTE-35__ _packets into mpegts streams._
   * [packets](#packets) _Output raw SCTE-35 packets from mpegts._
   * [proxy](#proxy) _Parse SCTE-35 from mpegts and copy video stream to stdout._
   * [pts](#pts) _Show PTS in realtime from live streams._
   * [sidecar](#sidecar) _Parse MPEGTS and_ __generate a SCTE-35 sidecar file.__
   * [sixfix](#sixfix) __ffmpeg mangles SCTE-35__, _sixfix is how to fix it._
   * [show](#show) _Display stream information for mpegts._ 
   * [version](#version) _Print threefive version._
   * [help](#help)  _Show threefive help._
---
# `decode`    
* Decode SCTE-35 from Base64,Hex,MPEGTS, etc..

#### Base64:     
```asm
      threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='
```
#### Hex:    
```asm     
      threefive 0xfc301600000000000000fff00506fe00a98ac700000b3baed9
```
#### Files:      
```asm    
      threefive myvideo.ts
```
#### Stdin:      
```asm      
      cat myvideo.ts | threefive
```
#### Http(s):
```asm
      threefive https://futzu.com/xaa.ts
```
#### Multicast:
```asm
      threefive udp://@235.35.3.5:3535
```
___
# `encode`    
* Encode SCTE-35 to JSON, XML, Base64, Hex, Int etc.. 

#### Base64 to Hex:  
```asm
      threefive  encode hex  '/DAlAAAAAAAAAP/wFAUAAAAOf+/+FOvVwP4ApMuAAA4AAAAAzBon0A=='
```
#### Hex to Xml:     
```asm
      threefive  encode xml  '0xfc301600000000000000fff00506fe00a98ac700000b3baed9' 
```
#### JSON to Base64: 
```asm
      threefive  encode  < json.json
```
#### JSON to Xml: 
```asm
      threefive  encode  xml  < json.json
```
#### Xml to Hex: 
```asm
      cat xml.xml | threefive  encode hex 
```
___
# `hls`  
* SCTE-35  Decoding and Encoding for HLS
       
#### HLS decode SCTE-35: 
```asm
      threefive hls https://example.com/master.m3u8
      
      threefive hls help
```
#### HLS encode SCTE-35: 
```asm
      threefive hls  -i https://example.com/master.m3u8 -s sidecar.txt -o output_dir

      threefive hls encode help
```
___
# `xml`       
* Xml output:

#### Base64
* xml format
```asm
      threefive xml '/DAsAAAAAAAAAP/wBQb+7YaD1QAWAhRDVUVJAADc8X+/DAVPVkxZSSIAAJ6Gk2Q='
```
* xml+bin format
```asm
      threefive xml binary '/DAsAAAAAAAAAP/wBQb+7YaD1QAWAhRDVUVJAADc8X+/DAVPVkxZSSIAAJ6Gk2Q='
```
#### MPEGTS
* xml format
```asm                                                                                           
      threefive xml https://example.com/video.ts 
```
* xml+bin format
```asm                                                                                           
      threefive xml binary https://example.com/video.ts 
```
___
#  `inject`
* Inject an mpegts stream with a SCTE-35 sidecar file at pid:
```asm
      threefive inject video.ts with sidecar.txt at 333
```
___
# `packets`
* Print raw SCTE-35 packets from multicast mpegts video:
```asm
        threefive packets https://example.com/video.ts
```
___
# `proxy`
* Parse a https stream and write raw video to stdout:
```asm
      threefive proxy https://example.com/video.ts
```
___
# `pts`       
* Print PTS from mpegts video:
```asm
      threefive pts video.ts
```
___
# `sidecar`
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt:
```asm
      threefive sidecar https://example.com/video.ts
```
___
#  `sixfix`    
* Fix SCTE-35 data mangled by ffmpeg: 
```asm
      threefive sixfix video.ts
```
___
# `show`      
* Probe mpegts video: 
```asm
      threefive show video.ts
```
___
# `version`  
```asm
      threefive version
```
___                 
# `help`      
```asm      
      threefive help
```
___
