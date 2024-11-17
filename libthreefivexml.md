# lib threefive & xml 
For xml, we wrote our own xml parser and xml generator, despite python have at least four xml parsers in the standard library. After doing just the parser with ElementTree, the python folks deprecated ElementTree. So I did the parser again using expat. By the time I was done with the expat version of the parser, it was about 180 lines of codr. threefive.xml.XmlParser is only 72 lines of code and does exactly what we need it to do.
all of the functions and classes... everything in threefive.xm is only 172 lines of readable and understandable code. I know the code is readable and understandable because often reference the code, and know what they're talking about.
Let me show you how well it works.   

* it's all 'cut and paste'-able if you want to follow along at home.

# There are two formats 
* the easy to use SCTE-35 xml+bin format
* the old and deprecated SCTE-35 xml SpliceInfoSection format

# SCTE-35 xml+bin format   ( Use This One )

```js
./threefive.py xml binary '/DAgAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAAANaNPVc=' 2> xml.xml
 cat xml.xml
<Signal xmlns="https://scte.org/schemas/35">
   <scte35:Binary>/DAgAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAAANaNPVc=</scte35:Binary>
</Signal>
```
* Fire up a python shell
```py3
a@fu:~/build/SCTE35_threefive$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u2, May 20 2024, 22:08:06)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
* import Cue
		from threefive import Cue

* read the xml into a string
		with open('xml.xml','r') as ex: exemel= ex.read()
* initialize a Cue instance with the exemel and call encode()
 
		cue=Cue(exemel)
		cue.show()
```js
cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 32,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0xd68d3d57"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 120.0,
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": []
}
```
* encode in the old SCTE-35 xml format

	node = cue.xml()
 	node
	<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   		<scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" 
			availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="1">
      		<scte35:BreakDuration autoReturn="true" duration="10800000"/>
   		</scte35:SpliceInsert>
	</scte35:SpliceInfoSection>

if you want to add a descriptor, do it the same as you would normally to the Cue instance


		from threefive import AvailDescriptor
		ad=AvailDescriptor()
 		ad.provider_avail_id= 999
 		cue.descriptors.append(ad)
* Anytime you add to or modify an existing Cue instance, call Cue.encode() to recalculate lengths , crc, etc...
		cue.encode()
		'/DAqAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAACgAIQ1VFSQAAA+eZrLoV'


* show the new SCTE-35 xml+bin format

		cue.xml(binary=True)
		<Signal xmlns="https://scte.org/schemas/35">
   			<scte35:Binary>/DAqAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAACgAIQ1VFSQAAA+eZrLoV</scte35:Binary>
		</Signal>

* show the SCTE-35 data as josn

 cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 42,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x99acba15"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 120.0,
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "name": "Avail Descriptor",
            "identifier": "CUEI",
            "provider_avail_id": 999
        }
    ]
}
```

* If you're using the new SCTE-35 xml+bin format, that's everything you need to know.

* If you're using the old SCTE-35 xml format, keep reading. 

---


### Old SCTE-35 xml SpliceInfoSection (this is deprecated but still in use. it kind of sucks.) 


```js
./threefive.py xml '/DAgAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAAANaNPVc=' 2> xml.xml

cat xml.xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="true" duration="10800000"/>
   </scte35:SpliceInsert>
</scte35:SpliceInfoSection>
`````

* Fire up a python shell
```py3
a@fu:~/build/SCTE35_threefive$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u2, May 20 2024, 22:08:06)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
* import Cue
		from threefive import Cue

* read the xml into a string
		with open('xml.xml','r') as ex: exemel= ex.read()
* initialize a Cue instance with the exemel and call encode()
 
		cue=Cue(exemel)
		cue.encode()

* cue.xml returns a threefive.xml.Node instance

		node =cue.xml()
		node
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="true" duration="10800000"/>
   </scte35:SpliceInsert>
</scte35:SpliceInfoSection>
```
* to use the xml+bin format call Cue.xml(binary=True)

* A Node can have children
* Node.children is a list.

		node.children
		[   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" 	                 
               availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="1">
              <scte35:BreakDuration autoReturn="true" duration="10800000"/>
           </scte35:SpliceInsert>
			]	
		node.children[0].children
			[      <scte35:BreakDuration autoReturn="true" duration="10800000"/>]
* A Node has a name
* Node.name is a string
		node.name
		'scte35:SpliceInfoSection'
* A Node can have a value, this one does not.
* <aNode>value</aNode>

		node.value
* A Node can have attrs ( attributes )
* Node.attrs is a dict and can be used as such.
* <aNode attr="true"/> 
		node.attrs
		{'xmlns': 'https://scte.org/schemas/35', 'pts_adjustment': 0, 'protocol_version': 0, 'sap_type': '0x03', 'tier': '0x0fff'}


* If you want to add a Comment Node

>>>> node.add_comment("Cool Xml")
>>>> node
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="false" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="true" duration="10800000"/>
   </scte35:SpliceInsert>
   <!-- Cool Xml -->    # New Comment
</scte35:SpliceInfoSection>

* Node.children is a list of Node instances. 
* Add a comment to node.children[0]

 		node.children[0].add_comment("Child 0")
 		node
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="false" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="true" duration="10800000"/>
      <!-- Child 0 -->    # Comment on node.Children[0]
   </scte35:SpliceInsert>
   <!-- Cool Xml -->   # Comment on node
</scte35:SpliceInfoSection>
```
* Node.children is a list so reordering children is easy.
		nc = node.children
		node.children =[nc[1],nc[0]]
		node
```xml
<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <!-- Cool Xml -->        # Comment is now first
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="false" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="true" duration="10800000"/>
      <!-- Child 0 -->
   </scte35:SpliceInsert>
</scte35:SpliceInfoSection>
```


* Add a Splice Descriptor to node
```py3
from threefive import AvailDescriptor
ad =AvailDescriptor()

ad.provider_avail_id=555

ad.encode()

b'CUEI\x00\x00\x02+'
 

adx=ad.xml()   # Calling xml returns a Node instance

type(adx)
<class 'threefive.xml.Node'>

```
* call node.add_child to attach the descriptor
* you could also call node.children.append(adx) since Node.children is a list

 	node.add_child(adx)
	node
	<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   		<sc<scte35:SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   			<!-- Cool Xml -->
   			<scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" 
				availNum="0" availsExpected="false" outOfNetworkIndicator="true" uniqueProgramId="1">
      			<scte35:BreakDuration autoReturn="true" duration="10800000"/>
      			<!-- Child 0 -->
   			</scte35:SpliceInsert>
   			<scte35:AvailDescriptor providerAvailId="555"/>
		</scte35:SpliceInfoSection>

 


* Generate new SCTe-35 from the xml with the new Avail Descriptor 
	* A Cue instance can be initialize with a Node instance
			newcue=Cue(node)
			newcue.encode()
			'/DAqAAAAAAAAAP/wDwUAAAABf7/+AKTLgAABAAAACgAIQ1VFSQAAAisioHpA'

			newcue.show()

```js
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 42,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": 4095,
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x22a07a40"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 120.0,
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": false,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 0,
        "avails_expected": false
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "name": "Avail Descriptor",
            "identifier": "CUEI",
            "provider_avail_id": 555
        }
    ]
}

```

* the help is always available for all threefive classes and functions

		from threefive.xml import Node
		help(Node)

```js
Help on class Node in module threefive.xml:

class Node(builtins.object)
 |  Node(name, value=None, attrs={}, ns=None)
 |  
 |  The Node class is to create an xml node.
 |  
 |  An instance of Node has:
 |  
 |      name :      <name> </name>
 |      value  :    <name>value</name>
 |      attrs :     <name attrs[k]="attrs[v]">
 |      children :  <name><children[0]></children[0]</name>
 |      depth:      tab depth for printing (automatically set)
 |  
 |  Use like this:
 |  
 |      from threefive.xml import Node
 |  
 |      ts = Node('TimeSignal')
 |      st = Node('SpliceTime',attrs={'pts_time':3442857000})
 |      ts.add_child(st)
 |      print(ts)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, name, value=None, attrs={}, ns=None)
 |  
 |  __repr__(self)
 |  
 |  add_attr(self, attr, value)
 |      add_attr add an attribute
 |  
 |  add_child(self, child, slot=None)
 |      add_child adds a child node
 |      set slot to insert at index slot.
 |  
 |  add_comment(self, comment, slot=None)
 |      add_comment add a Comment node
 |  
 |  get_indent(self)
 |      get_indent returns a string of spaces the required depth for a node
 |  
 |  mk(self, obj=None)
 |      mk makes the node obj,
 |      and it's children into
 |      an xml representation.
 |  
 |  rm_attr(self, attr)
 |      rm_attr remove an attribute
 |  
 |  rm_child(self, child)
 |      rm_child remove a child
 |      
 |      
 |      example:
 |      a_node.rm_child(a_node.children[3])
```
