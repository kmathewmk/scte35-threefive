### Two Critical things to remember when using ffmpeg with SCTE-35.
1) `-copyts` you need to keep the timestamps if you're transcoding.
2) `-muxpreload 0 -muxdelay 0` needs to be used to keep iframes and SCTE-35 aligned.  

# threefive works very well with ffmpeg. 
* __ffmpeg changes the SCTE-35 (0x86) stream type to bin data (0x6)__
* __threefive is the only SCTE35 tool that parses both  SCTE-35 `(0x86)` and bin data `(0x6)` stream types__.  
* __the threefive cli tool can convert the stream_type back to `0x86` after ffmpeg changes it.

### Example 1
---
* Transcode mpegts with a SCTE-35 stream and pipe it to threefive to parse SCTE-35
  * oldvid.ts looks like this:
```
  Program 1 
  Stream #0:0[0x31]: Video: h264 (High) ([27][0][0][0] / 0x001B), yuv420p(tv, bt709, progressive), 
  1280x720 [SAR 1:1 DAR 16:9], Closed Captions, 59.94 fps, 59.94 tbr, 90k tbn
  Stream #0:1[0x32]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:2[0x33]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:3[0x34]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:4[0x35]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:5[0x36]: Data: scte_35
```
* transcode
   * `-copyts`, keep timestamps 
   * `-map`  keep SCTE-35 stream 

```sh
ffmpeg  -copyts -i  oldvid.ts -vcodec libx265  -map 0  -muxpreload 0 -muxdelay 0 -y  newvid.ts
```

* newvid.ts looks like this
```
  Program 1 
  Stream #0:0[0x100]: Video: hevc (Main) (HEVC / 0x43564548), yuv420p(tv, bt709), 1280x720 
  [SAR 1:1 DAR 16:9], 59.94 fps, 59.94 tbr, 90k tbn
  Stream #0:1[0x101]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:2[0x102]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:3[0x103]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:4[0x104]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:5[0x105]: Data: bin_data ([6][0][0][0] / 0x0006)
```
 * You can parse it as is with the threefive cli tool
```js
threefive newvid.ts
```
* transcode with ffmpeg and pipe into threefive cli as is
```js
ffmpeg  -copyts -i  oldvid.ts -vcodec libx265  -map 0  -muxpreload 0 -muxdelay 0 -f mpegts -| threefive
```
* You can also change the stream type from `0x6` back to `0x86` with __threefive sixfix__ so other SCTE-35 parsers can read the SCTE-35.
```js
threefive mpegts sixfix sixed.ts
fixing these pids {258}
Wrote: sixfixed-newvideo.ts
```

