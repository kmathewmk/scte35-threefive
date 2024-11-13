# Xml as of v2.4.93

#### xml in the Cli  
*  [SCTE-35 xml input](#xml-input)
*  [SCTE-35 xml output](#xml-output)
*  [SCTE-35 xml output from MPEGTS](#xml-output-from-mpegts-video) 

#### xml in the Cue class 
* [SCTE-35 xml input](#xml-as-input)
* [SCTE-35 xml output](#the-cue-class-can-return-xml-as-output)
* [reoving SCTE-35 xml attributes](#removing-xml-attributes)
* [removing or changing the scte35 namespace](#removing-or-changing-the-namespace)

# Cli

### Xml input 

* SCTE-35 Xml can be encoded to base64,bytes,hex, int, or json using the `encode` keyword 


```xml

a@fu:~/build/SCTE35_threefive$ cat xml.xml
<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <TimeSignal>
      <SpliceTime ptsTime="3985015765"/>
   </TimeSignal>
   <!-- Break Start -->
   <SegmentationDescriptor segmentationEventId="56561" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="34" segmentNum="0" segmentsExpected="0">
      <!-- UPID: MPU  -->
      <SegmentationUpid segmentationUpidType="12" segmentationUpidFormat="hexbinary" formatIdentifier="1331055705" privateData="73">4f564c5949</SegmentationUpid>
   </SegmentationDescriptor>
</SpliceInfoSection>
```

* Xml to Base64

```js
a@fu:~/build/SCTE35_threefive$ .threefive encode  < xml.xml

/DAsAAAAAAAAAP/wBQb+7YaD1QAWAhRDVUVJAADc8X+/DAVPVkxZSSIAAJ6Gk2Q=

```

* Xml to  hex

```js
a@fu:~/build/SCTE35_threefive$  threefive encode  hex < xml.xml
0xfc302c00000000000000fff00506feed8683d500160214435545490000dcf17fbf0c054f564c59492200009e869364

```

* Xml to int
```js
a@fu:~/build/SCTE35_threefive$  threefive encode  int  < xml.xml
151622312799635087445131038116901140411521203255173124307448868984487395583746158940007186416525810106184013091684
```

### Xml output
* the cli can convert SCTE-35 base64, hex, or json to xml 
```js
a@fu:~/build/SCTE35_threefive$ threefive encode xml '0xfc302c00000000000000fff00506feed8683d500160214435545490000dcf17fbf0c054f564c59492200009e869364'
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="3985015765"/>
   </scte35:TimeSignal>
   <!-- Break Start -->
   <scte35:SegmentationDescriptor segmentationEventId="56561" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="34" segmentNum="0" segmentsExpected="0">
      <!-- MPU -->
      <scte35:SegmentationUpid segmentationUpidType="12" segmentationUpidFormat="hexbinary" formatIdentifier="1331055705" privateData="73">4f564c5949</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```

### Xml output from mpegts video

* MPEGTS streams can be parsed for SCTE-35 and the output encoded in Xml

```js
a@fu:~/build/SCTE35_threefive$ threefive xml  sixed.ts
```
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="207000" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="false" eventIdComplianceFlag="true" availNum="1" availsExpected="1" outOfNetworkIndicator="true" uniqueProgramId="39321">
      <scte35:Program>
         <scte35:SpliceTime ptsTime="6554297154"/>
      </scte35:Program>
      <scte35:BreakDuration autoReturn="true" duration="10798788"/>
   </scte35:SpliceInsert>
   <!-- Provider Placement Opportunity Start -->
   <scte35:SegmentationDescriptor segmentationEventId="0" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="52" segmentNum="0" segmentsExpected="0" subSegmentNum="0" subSegmentsExpected="0" segmentationDuration="10800000">
      <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false" noRegionalBlackoutFlag="false" archiveAllowedFlag="false" deviceRestrictions="0"/>
      <!-- Deprecated -->
      <scte35:SegmentationUpid segmentationUpidType="1" segmentationUpidFormat="hexbinary">10100000</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>

```

* threefive prints output to stderr, stdout is used for piping data. 
* To save the output of the cli tool redirect 2.
```js
threefive xml  sixed.ts 2> fu.xml
```

# Xml with the Cue class.

###  The Cue class can return xml as output

```py3
a@fu:~/build/SCTE35_threefive$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u2, May 20 2024, 22:08:06)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import Cue
>>>> cue=Cue('/DA4AAAAAAAA///wBQb+AKpFLgAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAABZE5vg=')
>>>> cue.decode()
True
>>>> cue.xml()
```
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11158830"/>
   </scte35:TimeSignal>
   <!-- Program Start -->
   <scte35:SegmentationDescriptor segmentationEventId="3" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="16" segmentNum="0" segmentsExpected="0" segmentationDuration="2702700">
      <!-- AdID -->
      <scte35:SegmentationUpid segmentationUpidType="3" segmentationUpidFormat="text">ABCD0123456H</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
* the Cue class can also return xml in the xml+bin format
* set the optional binary arg to True
```py3
>>>> cue.xml(binary=True)
```
```xml
<Signal xmlns="https://scte.org/schemas/35">
   <scte35:Binary>/DA4AAAAAAAA///wBQb+AKpFLgAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAABZE5vg=</scte35:Binary>
</Signal>
```

### Xml as input

* xml can now be passed in  to a Cue instance when initialized
* both xml and xml+bin formats can be used.
```xml
x="
<Signal xmlns="https://scte.org/schemas/35">
   <Binary>/DA4AAAAAAAA///wBQb+AKpFLgAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAABZE5vg=</Binary>
</Signal>
"
```
```py3
>>>> cue2=Cue(x)
>>>> cue2.decode()
True
>>>> cue2.xml()
```
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11158830"/>
   </scte35:TimeSignal>
   <!-- Program Start -->
   <scte35:SegmentationDescriptor segmentationEventId="3" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="16" segmentNum="0" segmentsExpected="0" segmentationDuration="2702700">
      <!-- AdID -->
      <scte35:SegmentationUpid segmentationUpidType="3" segmentationUpidFormat="text">ABCD0123456H</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```

# What is proper SCTE-35 xml?

* this is difficult question to answer. there are multiple specifications that conflict in some areas, the schema is several years out of date, and some is just not very clear.The majority of the issues are with the attributes of the complex UPIDs, which most people do not use. Howeveer, if you do use them , you can make adjustments if needed.
### Removing xml attributes
* If you want to remove an attribute, you can use rm_xmlattr function.

```py3
>>>> from threefive.xml import rm_xmlattr
>>>> from threefive import Cue
>>>> cue=Cue('/DA4AAAAAAAA///wBQb+AKpFLgAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAABZE5vg=')
>>>> cue.decode()
>>>> x = cue.xml()
>>>> print(x)
```
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11158830"/>
   </scte35:TimeSignal>
   <!-- Program Start -->
   <scte35:SegmentationDescriptor segmentationEventId="3" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="16" segmentNum="0" segmentsExpected="0" segmentationDuration="2702700">
      <!-- AdID -->
      <scte35:SegmentationUpid segmentationUpidType="3" segmentationUpidFormat="text">ABCD0123456H</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
```py3
>>>> y = rm_xmlattr(x,"sapType")
>>>> print(y)
```
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0"  tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11158830"/>
   </scte35:TimeSignal>
   <!-- Program Start -->
   <scte35:SegmentationDescriptor segmentationEventId="3" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="16" segmentNum="0" segmentsExpected="0" segmentationDuration="2702700">
      <!-- AdID -->
      <scte35:SegmentationUpid segmentationUpidType="3" segmentationUpidFormat="text">ABCD0123456H</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
### Removing or changing the namespace

* the namespace can be removed or changed  in either the xml or xml+bin format
* to remove the scte35 namespace, set the optional ns arg  to an empty string

```py3
>>>> cue.xml(ns='')
```
```xml
<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <TimeSignal>
      <SpliceTime ptsTime="11158830"/>
   </TimeSignal>
   <!-- Program Start -->
   <SegmentationDescriptor segmentationEventId="3" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="16" segmentNum="0" segmentsExpected="0" segmentationDuration="2702700">
      <!-- AdID -->
      <SegmentationUpid segmentationUpidType="3" segmentationUpidFormat="text">ABCD0123456H</SegmentationUpid>
   </SegmentationDescriptor>
</SpliceInfoSection>
```

