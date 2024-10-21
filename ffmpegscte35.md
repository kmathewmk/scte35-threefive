# Ffmpeg and threefive and SCTE-35

### ffmpeg changes SCTE-35 stream type from 0x86 to 0x6 when transcoding.
* threefive parses both stream type 0x86 and 0x6.
* the threefive cli tool can convert the stream type back to 0x86 
```rebol
        threefive sixfix video.ts
```
* the output video will be named sixfixed-video.ts
    
### When transcoding video containing SCTE-35 wiith ffmpeg make sure to retain the original PTS and iframe locations.
* use -copyts
* use -muxpreload 0 -muxdelay 0
```rebol
     ffmpeg -copyts -i video.ts [other ffmpeg stuff] -muxpreload 0 -muxdelay 0 outvideo.ts
```

### How to retain SCTE-35 when using ffmpeg to segment HLS. 
* create a sidecar file of the SCTE-35 Cues
```sh
        threefive sidecar video.ts
```

* segment with ffmpeg
* Use [sideways](https://github.com/futzu/sideways) to inject SCTE-35 back into the HLS
