# threefive
###  the  cli
   * [default](#default) __Basic threefive cli usage.__ _(start here)_ 
   * [hls](#hls) __HLS SCTE-35 Decoding and Encoding.__
   * [xml](#xml)  __Xml__ _output for_ _SCTE-35._
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
### `default`
* The default action of the threefive cli is to take an input and make it a SCTE-35 output.
* SCTE-35 inputs are auto-detected.
* SCTE-35 output default to json, other types must be specified.

     * These inputs are supported.
       * `mpegts` , `base64`,  `hex`, `json`, `xml`, `xmlbin`

    * These outputs are supported.
       * `base64`, `bytes`,  `hex`, `json`, `xml`, `xmlbin`
  
  ### Example usage

|  Input       | Output        | Command                                                                   |
|--------------|---------------|---------------------------------------------------------------------------|
| `mpegts`       |  `base64`      | **threefive** https://example.com/video.ts  **base64**                            |
|  `xml`         |  `bytes`        | **threefive**  bytes  < xml.xml                                               |
| `base64`       |   `hex`         | **threefive** '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='  **hex**                     |
| `xmlbin`       |   `int`         | **threefive  int**  < xml.xml                                                 |
| `mpegts`       |  `json`         | **threefive** video.ts                                                        |
| `json`         |   `xml`         | **threefive**  < json.json  **xml**                                               |
|  `hex`         |  `xmlbin`       | **threefive** 0xfc301600000000000000fff00506fe00a98ac700000b3baed9  **xmlbin** 
                                                     |
___
### `hls`  
* SCTE-35  Decoding and Encoding for HLS
       
* HLS SCTE-35 Decoding: 
```asm
      threefive hls https://example.com/master.m3u8
```
* _read the help for advanced HLS SCTE-35 decoding._
```asm    
      threefive hls help
```
* HLS SCTE-35 Encoding: 
```asm
      threefive hls  -i https://example.com/master.m3u8 -s sidecar.txt -o output_dir
```
*  _read the help for advanced HLS SCTE-35 encoding._
``` asm
      threefive hls encode help
```
___
### `xml`       
* Xml output:

* Base64
  * xml splice info section format
```asm
      threefive xml '/DAsAAAAAAAAAP/wBQb+7YaD1QAWAhRDVUVJAADc8X+/DAVPVkxZSSIAAJ6Gk2Q='
```
  * xml+bin format
```asm
      threefive xml binary '/DAsAAAAAAAAAP/wBQb+7YaD1QAWAhRDVUVJAADc8X+/DAVPVkxZSSIAAJ6Gk2Q='
```
* MPEGTS
  * xml splice info section format
```asm                                                                                           
      threefive xml https://example.com/video.ts 
```
  * xml+bin format
```asm                                                                                           
      threefive xml binary https://example.com/video.ts 
```
___
###  `inject`
* Inject an mpegts stream with a SCTE-35 sidecar file at pid:
```asm
      threefive inject video.ts with sidecar.txt at 333
```
___
### `packets`
* Print raw SCTE-35 packets from multicast mpegts video:
```asm
        threefive packets https://example.com/video.ts
```
___
### `proxy`
* Parse a https stream and write raw video to stdout:
```asm
      threefive proxy https://example.com/video.ts
```
___
### `pts`       
* Print PTS from mpegts video:
```asm
      threefive pts video.ts
```
___
### `sidecar`
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt:
```asm
      threefive sidecar https://example.com/video.ts
```
___
###  `sixfix`    
* Fix SCTE-35 data mangled by ffmpeg: 
```asm
      threefive sixfix video.ts
```
___
### `show`      
* Probe mpegts video: 
```asm
      threefive show video.ts
```
___
### `version`  
```asm
      threefive version
```
___                 
### `help`      
```asm      
      threefive help
```
___
