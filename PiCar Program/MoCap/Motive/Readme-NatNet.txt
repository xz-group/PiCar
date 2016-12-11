NaturalPoint, Inc.

NatNet SDK is a simple Client/Server networking SDK for sending and receiving
NaturalPoint data across networks.  NatNet uses the UDP protocol in conjunction
with either multicasting or point-to-point unicasting for transmitting data.

Please refer to the NatNet API USer's Guide for more information.


Change Log
-----------
Version 2.8.0 (4/15/2015)
-----------------------

* Note to Direct Depackatization Clients : No bitstream syntax change from 2.7.0 to 2.8.0

Added:   Motive 1.8 streaming support

Added:   New MATLAB wrapper sample.

Added:   Add playback range and looping commands ("SetPlaybackStartFrame,frameNumber","SetPlaybackStopFrame,frameNumber","SetPlaybackLooping,0or1")
         to NatNet command list, update NatNet SDK Winforms and PacketClient samples to illustrate usage.

Added:   Add DecodeID() helper routine, illustrate usage in Winforms and SampleClient apps for decoding legacy marker id
         into modelID, markerID pairs.

Fixed:   Fix for PointCloud solved bit indcator.

Added:   Updated Unity3D streaming sample to stream rigid bodies and skeletons.

Added:   Add Z-up quaternion to euler decoding example to WinForms sample when streaming Z-UP from Motive.

Added:   Add support and examples for explicitly disconnecting unicast clients.

Added:   Add support for Z-Up streaming, update SampleClient 3D to illustrate usage

Changed: (NatNet Managed Library (NatNetML) only) Change GetLastFrameOfData() routine  in managed client to lock the frame
         and return a copy of the data (polling clients only), update WinForms sample app to illustrate usage. 

Changed: (NatNet Managed Library (NatNetML) only) Provide copy constructors to simplify .NET client data deep copy operations,
         update Winforms sample with data copy operation.

Changed: (NatNet Managed Library (NatNetML) only) Fix graphing for correct frame aligmnment for Motive.

Changed: (NatNet Managed Library (NatNetML) only) Add timing testing operations and reporting.

Fixed:   Fix for Debug x64 WinformsSample not compiling out of the box.

Fixed:   Fix for RigidBody tracked flag in managed clients.


Version 2.7.0 (10/15/2014)
-----------------------

* Note to Direct Depackatization Clients : bitstream syntax changed from 2.6.0 to 2.7.0 (see below for details)

Added:   Motive 1.7 streaming support

Added:   New timing sample for validating mocap streaming frame timing.

Added:   New Broadcast Trigger sample illustrating how to use remote record
         trigger/listen using XML formatted UDP broadcast packets instead of NatNet commands.

Added:   NatNetML - added SMPTE Timecode and Timecode Subframe members.  See WinForms sample for usage.

Fixed:   Fix for FrameID periodically displays dropped/duplicate packets during live mode.

Fixed:   Fix for PacketClient incorrectly decoding rigid Body IsTracked parameter.

Fixed:   Fix for crash in GetDataDescriptions() when streaming a Rigid Body with a single character name.

Fixed:   Sample Client incorrectly reports skeleton marker data

Changed: Update SampleClient3D to clarify quaterion decomposition, add new visuals.

Changed: Maximum markers per rigid body changed from 10 to 20 to match new RigidBody tracking
         capabilities in Motive.

Changed: Frame timestamp now keyed off hardware frame id.  fTimestamp resolution increased
         from float to double *.  
         
* DirectDepackatization clients should update their code (see timestamp in PacketClient.cpp for an example).

         
Version 2.6.0 (5/8/2014)
------------------------------
Added:   Motive 1.6 Streaming support

Added:   RigidBody tracking state parameter

Added:   IsRecording flag on FrameOfMocapData indicating frame was recorded in Motive

Added:   ModelsChanged flag on FrameOfMocapData indicating actively tracked model list has changed.

Added:   Additional flags on LabelMarkerList indicating marker occlusion and marker position
         calculation method.

Added:   Additional FrameOfMocapData timestamp

Added:   NatCap remote capture sample for illustrating send/receive remote Motive control commands via
         UDP broadcast direct.

Added:   UDP Repeater / Unity3D

Changed: Increase unlabeled/other marker count cap to 1000

Fixed:   SampleClient latency value


Version 2.5.0 (9/2013)
------------------------------
Added:   Motive 1.5 streaming support.

Added:   New Matlab sample.

Added:   Additional function signature overloads to better support MatLab.

Added:   Motive remote control commands Start/Stop Recording, Start/Stop Playback,
         LiveMode, EditMode, SetRecordTakeName, SetLiveTakeName.  Refer to WinForms sample for usage examples.

Added:   Motive record broadcast message parser sample.

Added:   Samples updated to illustrate accessing point cloud model solved marker locations.

Added:   Timing information to WinForms sample.

Added:   New QuaternionToEuler() helper routines

Changed: Winforms Sample update for newer layout, sample Command/Requests for use with Motive

Fixed:   SimplerServer compile issue.

Fixed:   SampleClient when >2 skeletons are streaming.


Version 2.4.0 (3/19/2013)
------------------------------
Added:   Motive 1.0 support.

Fixed:   Memory leak in Client.

Fixed:   Timecode during playback from file.

Fixed:   Fix for crashes during large actor count (4-5) streaming.

Changed: Force "Dont Fragment" bit in IP header to off (0).

Changed: Update Winforms 2010 sample to target .NET 4.0 framework (same as NatNetML.dll assembly).

Changed: NatNetML - added additional MatLab compatible event signature (OnFrameReady2).

Version 2.3.0 (12/28/2011)
------------------------------

Added:   SMPTE Timecode support (where supported, adds timecode stamp to every frame of mocap data).

Added:   New "LabeledMarker" data type.  This data type is used for labeled markers not associated
         with a pre-defined "MarkerSet".

Changed: PacketClient example updated to reflect the new bitstream syntax containing "LabeledMarkers".

Changed: PacketClient example updated to reflect the new bitstream syntax containing Timecode data.



Version 2.2.0 (4/25/2010)
------------------------------
Added:   New Unicast Point-to-Point connection type.  Servers and clients can now 
         use MultiCast or Unicast as their connection type.  Connection type between
         server and client must be the same. 

Added:   Application-definable command and data port assignments, including Multicast address.
         
Added:   VC redistributable installer (\Samples\VCRedist\vcredist_x86.exe) for running
         the pre-compiled samples on machines without VisualStudio and/or the correct
         version of the CRT runtime installed on them.

Changed: Changed PacketClient to support shared addresses (SO_REUSEADDR).  Necessary
         when server and client are running on same machine.

Changed: Updates to SimpleServer, SampleClient, and Winforms client to illustrate
         Unicast usage.

Changed: Default Multicast address/port to IANA safe default values.

Fixed:   Precompiled WinForms sample crashes on some machines.



Version 2.1.0 (11/20/2009)
------------------------------
Added:   New "Skeleton" data type, representing a named, hierarchical collection
         of RigidBodies.


Version 2.0.0 (11/12/2009)
------------------------------       
Added:   New RigidBody parameters
          - RigidBody Name to RigidBody description
          - MarkerData to RigidBody Data, including ID, position, and size
          - MeanError to RigidBody data

Added:   New managed (.NET) class library (NatNetML.dll).  Allows for NatNetClient
         and NatNet data types to be consumed directly in .NET compatible
         environments (e.g. VB.Net, C#, LabView, MatLab).
       
Added:   New WinForms .NET sample application illustrating NatNetML consumption.

Added:   New depacketization sample (PacketClient) to replace the bitstream syntax.
         This sample can be used to decode NatNet packets directly without the need 
         for the NatNet SDK.  Intended only for clients that cannot use the NatNet SDK (e.g. Unix clients).

Added:   New SDK documentation.

Added:   Basic Client/Server message passing support (SendMessage(..)/SendMessageAndWait(..))

Added:   Allow connections to a single server from multiple clients on same and/or different machines.

Changed: SampleClient updated to illustrate MarkerSet and RigidBody data handling.

Changed: SampleServer and SimpleServer samples merged into a single, simplified NatNet Server example.

Changed: SampleClient3D to include conversion and display of RigidBody quaternions to euler angles.

Changed: Updated to IPV6 protocol.

        
Version 1.2.0 (1/23/2008)
------------------------------
Added:   VC8 static library (NatNetLibStatic.lib)

Added:   VC6 static library (NatNetvc6StaticLib.lib)

Added:   x64 libraries (dynamic and static)

Added:   Bitstream syntax documentation.

Added:   Rigid body data type support.

Added:   Versioning information.  NatNet version information is now available from
         file (DLL), local version (NatNetHelper::NatNetVersion), and fom the
         connected application(ServerDescription.NatNetVersion()) to help ensure NatNet
         server/client versions are in synch.

Changed: Updated to Visual Studio 2005 Project files.

Changed: Removed all /clr references.  NatNet and the samples use strictly
         native code.

Changed: NatNet types and helper routines cleaned up to improve usage.

Changed: SampleServer and Sampleclient programs updated to illustrate new usages.

