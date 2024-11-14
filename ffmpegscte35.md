# Ffmpeg and threefive and SCTE-35

### ffmpeg changes SCTE-35 stream type from 0x86 to 0x6 when transcoding.
* threefive parses both stream type 0x86 and 0x6.
* the threefive cli tool can convert the stream type back to 0x86 
```rebol
threefive sixfix video.ts
```
* the output video will be named sixfixed-video.ts
* [threefive can handle ffmpeg rewriting SCTE-35 packets](https://github.com/futzu/SCTE-35/blob/master/ffrewrite.md)    
### When transcoding video containing SCTE-35 wiith ffmpeg make sure to retain the original PTS and iframe locations.
* use -copyts
* use -muxpreload 0 -muxdelay 0
```rebol
ffmpeg -copyts -i video.ts [other ffmpeg stuff] -muxpreload 0 -muxdelay 0 outvideo.ts
```

### How to retain SCTE-35 when using ffmpeg to segment ABR HLS Live. 
* __This can be done in realtime on live streams__
* create a sidecar file of the SCTE-35 Cues with `threefive proxy`
* pipe the MPEGTS from threefive to ffmpeg
* Create renditions and master.m3u8 with ffmpeg

```smalltalk
threefive mpegts proxy video.ts | ffmpeg -copyts -i - [..ffmpeg stuff..] master.m3u8
```

* Start threefive to inject SCTE-35 back into the HLS

```smalltalk
threefive hls encode -i master.m3u8 -s sidecar.txt -o output_dir
```
*  threefive will process the renditions from the master.m3u8 and add SCTE-35 Cues from the sidecar file live.
*  SCTE-35 is translated to HLS tags. __All SCTE-35 HLS Tags are Supported__. 
*  SCTE-35 is added to new manifest files in output_dir
*  Original segments from ffmpeg are used. Segments are split if needed for Cue Outs. 
