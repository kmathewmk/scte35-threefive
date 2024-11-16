
### decode    
    * Decode SCTE-35 from Base64,Hex,MPEGTS, etc..
* Base64:     
```js
threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='
```
* Hex:    

```js
threefive 0xfc301600000000000000fff00506fe00a98ac700000b3baed9
```
* Files:      
```js
threefive myvideo.ts
```
 * Stdin:      
```js
cat myvideo.ts | threefive
```
* Http(s):    
```js
threefive https://futzu.com/xaa.ts
```
* Multicast:  
```js
threefive udp://@235.35.3.5:3535
```
### encode    

    * Encode SCTE-35 to JSON, XML, Base64, Hex, Int etc.. 

* Base64 to Hex:  
```js
threefive  encode hex  '/DAlAAAAAAAAAP/wFAUAAAAOf+/+FOvVwP4ApMuAAA4AAAAAzBon0A=='
```
 * Hex to Xml:     
```js
threefive  encode xml  '0xfc301600000000000000fff00506fe00a98ac700000b3baed9' 
```
* JSON to Base64: 
```js
threefive  encode  < json.json
```
* JSON to Xml: 
```js
threefive  encode  xml  < json.json
```
* Xml to Hex: 
```js
cat xml.xml | threefive  encode hex 
```
### hls  
    * SCTE-35  Decoding and Encoding for HLS      
* HLS decode SCTE-35: threefive hls help
```js
threefive hls https://example.com/master.m3u8
```
* HLS encode SCTE-35: threefive hls encode help
```js
threefive hls  -i https://example.com/master.m3u8 -s sidecar.txt -o output_dir
```

### `xml`       
    * Xml output:
```js
threefive xml '/DAsAAAAAAAAAP/wBQb+7YaD1QAWAhRDVUVJAADc8X+/DAVPVkxZSSIAAJ6Gk2Q='
                                                                                                                                                                                                             
threefive xml https://example.com/video.ts 
```
###  inject

* Inject an mpegts stream with a SCTE-35 sidecar file at pid:                                                                                                                                         
```js
threefive inject video.ts with sidecar.txt at 333
```

### packets
* Print raw SCTE-35 packets from multicast mpegts video:                                                                                                                                              
```js
threefive packets https://example.com/video.ts
```

### proxy
* Parse a https stream and write raw video to stdout:                                                                                                                                                 
```js
threefive proxy https://example.com/video.ts
```

### `pts`       
* Print PTS from mpegts video: 
```js
threefive pts video.ts
```
### `sidecar`
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt:
```js
threefive sidecar https://example.com/video.ts
```
### `sixfix`    
* Fix SCTE-35 data mangled by ffmpeg: 

```js
threefive sixfix video.ts
```

### `show`      
* Probe mpegts video: 

```js
threefive show video.ts
```
### `version`   
* Show version
```js
threefive version
```                    
### `help`      
* Help: 

```js
threefive help
```
