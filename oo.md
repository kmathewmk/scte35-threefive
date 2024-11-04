# threefive: more OO than you know.

I designed threefive to be predictable,most objects work the same way and have the same methods. 
Most classes are derived from SCTE35Base. The Splice Commands, Splice Descriptors, and Cue classes are subclassed from SCTE35Base. 
This really helps when making new SCTE-35 Cues. 

I can ramble on about it, but I think it best to show you. 

Let's make a Cue in the python shell

```py3
a@fu:~/build/SCTE35_threefive$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u2, May 20 2024, 22:08:06)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>>> from threefive import Cue, TimeSignal, AvailDescriptor
```
* let's make a TimeSignal

```py3
>>>> ts=TimeSignal()
>>>> ts
{'command_length': 0, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': None, 'pts_time': None}

````
* when you encode a Splice Command or Splice Descriptor, threefive will help you get it right.
* When reading a python stack trace, the last line is the error.
```py3
>>>> ts.encode()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/a/build/SCTE35_threefive/threefive/commands.py", line 157, in encode
    self._encode_splice_time(nbin)
  File "/home/a/build/SCTE35_threefive/threefive/commands.py", line 176, in _encode_splice_time
    self._chk_var(bool, nbin.add_flag, "time_specified_flag", 1)
  File "/home/a/build/SCTE35_threefive/threefive/base.py", line 38, in _chk_var
    raise ValueError(err_mesg)
ValueError: time_specified_flag is not set, it should be 1 bit(s) and type <class 'bool'>  <--- the last line is the error
```
* set some vars and try to encode again
```py3
>>>> ts.time_specified_flag = True
>>>> ts.pts_time=12345.6789  

>>>> ts.encode()

b'\xfeB:5\xbd'    <---  encoding returns a byte string when it works

```

* call some methods 
```py3
>>>> ts.xml()
<TimeSignal>
   <SpliceTime ptsTime="1111111101"/>
</TimeSignal>

>>>> ts.show()
{
    "command_length": 0,
    "command_type": 6,
    "name": "Time Signal",
    "time_specified_flag": true,
    "pts_time": 12345.6789
}
```
* Now let's make a Cue instance wnd add the TimeSignal to it.
```py3
>>>> cue =Cue()
>>>> cue.command=ts
>>>> cue.encode()
'/DAWAAAAAAAAAP/wBQb+Qjo1vQAAuwxz9A=='  <--- encode returns a Base64 string for a cue
```
* Calling encode on an object will recalculate several vars in the object, 
* When encoding a Cue, it will generate anything missing, including the info_section.
```py3
>>>> cue.info_section
{'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x03', 'sap_details': 'No Sap Type', 'section_length': 22, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0, 'pts_adjustment': 0, 'cw_index': '0x0', 'tier': '0xfff', 'splice_command_length': 5, 'splice_command_type': 6, 'descriptor_loop_length': 0, 'crc': '0xbb0c73f4'}
>>>> 
```
* encode(), decode(), xml(), and show() also work with Cue
```py3 
>>>> cue.xml()
<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <TimeSignal>
      <SpliceTime ptsTime="1111111101"/>
   </TimeSignal>
</SpliceInfoSection>

>>>> cue.command.xml()     <-- this is the TimeSignal
<TimeSignal>
   <SpliceTime ptsTime="1111111101"/>
</TimeSignal>

>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xbb0c73f4"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 12345.6789
    },
    "descriptors": []
}
>>>> cue.command.show()
{
    "command_length": 5,
    "command_type": 6,
    "name": "Time Signal",
    "time_specified_flag": true,
    "pts_time": 12345.6789
}
>>>> 
```
* Splice Descriptors work the same way
```py3
>>>> ad = AvailDescriptor()

>>>> ad.encode()

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/a/build/SCTE35_threefive/threefive/descriptors.py", line 166, in encode
    self._chk_var(int, nbin.add_int, "provider_avail_id", 32)
  File "/home/a/build/SCTE35_threefive/threefive/base.py", line 38, in _chk_var
    raise ValueError(err_mesg)
ValueError: provider_avail_id is not set, it should be 32 bit(s) and type <class 'int'>

>>>> ad.provider_avail_id = 1234

>>>> ad.encode()
b'CUEI\x00\x00\x04\xd2'  <--- encode returns a byte string when it works
>>>> 

```
* Add the AvailDescriptor to the Cue. 
* Cue.descriptors is a list, so append it. 
```py3
>>>> cue.descriptors.append(ad)
>>>> cue.encode()
'/DAgAAAAAAAAAP/wBQb+Qjo1vQAKAAhDVUVJAAAE0iVuWvA=' <---- Base64 string
```
* modify the AvailDescriptor and add another Descriptor
```py3
>>>> ad.provider_avail_id = 5678
>>>> ad.show()
{
    "tag": 0,
    "descriptor_length": 8,
    "name": "Avail Descriptor",
    "identifier": "CUEI",
    "provider_avail_id": 5678
}
>>>> cue.descriptors.append(ad)
>>>> len(cue.descriptors)
2
```
* You can also encode Cue to hex, or int.
```py3
>>>> cue.encode2hex()
'0xfc302a00000000000000fff00506fe423a35bd00140008435545490000162e0008435545490000162e7cf13378'
>>>> cue.encode2int()
2313572608209932854073470233617156645467305914531507959339025453988506820473289879370790529590385607701508984
```
* Everything in a Cue works of dot notation, if you want to change PTS, change it.
```py3
>>>> cue.command.pts_time
12345.6789
>>>> cue.command.pts_time=999.9987
>>>> cue.encode()
'/DAqAAAAAAAAAP/wBQb+BV1KCwAUAAhDVUVJAAAWLgAIQ1VFSQAAFi7SdffT'
```
