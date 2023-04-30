# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: intrusion_zone.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import zone_pb2 as zone__pb2
import action_pb2 as action__pb2
import device_pb2 as device__pb2
import card_pb2 as card__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='intrusion_zone.proto',
  package='intrusion_zone',
  syntax='proto3',
  serialized_options=_b('\n!com.supremainc.sdk.intrusion_zoneP\001Z\035biostar/service/intrusionZone'),
  serialized_pb=_b('\n\x14intrusion_zone.proto\x12\x0eintrusion_zone\x1a\nzone.proto\x1a\x0c\x61\x63tion.proto\x1a\x0c\x64\x65vice.proto\x1a\ncard.proto\"<\n\x06Member\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\r\n\x05input\x18\x02 \x01(\r\x12\x11\n\toperation\x18\x03 \x01(\r\"t\n\x05Input\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0c\n\x04port\x18\x02 \x01(\r\x12&\n\nswitchType\x18\x03 \x01(\x0e\x32\x12.device.SwitchType\x12\x10\n\x08\x64uration\x18\x04 \x01(\r\x12\x11\n\toperation\x18\x05 \x01(\r\"7\n\x06Output\x12\r\n\x05\x65vent\x18\x01 \x01(\r\x12\x1e\n\x06\x61\x63tion\x18\x02 \x01(\x0b\x32\x0e.action.Action\"\x9e\x02\n\x08ZoneInfo\x12\x0e\n\x06zoneID\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x64isabled\x18\x03 \x01(\x08\x12\x10\n\x08\x61rmDelay\x18\x04 \x01(\r\x12\x12\n\nalarmDelay\x18\x05 \x01(\r\x12\x0f\n\x07\x64oorIDs\x18\x06 \x03(\r\x12\x10\n\x08groupIDs\x18\x07 \x03(\r\x12 \n\x05\x63\x61rds\x18\x08 \x03(\x0b\x32\x11.card.CSNCardData\x12\'\n\x07members\x18\t \x03(\x0b\x32\x16.intrusion_zone.Member\x12%\n\x06inputs\x18\n \x03(\x0b\x32\x15.intrusion_zone.Input\x12\'\n\x07outputs\x18\x0b \x03(\x0b\x32\x16.intrusion_zone.Output\"\x1e\n\nGetRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"6\n\x0bGetResponse\x12\'\n\x05zones\x18\x01 \x03(\x0b\x32\x18.intrusion_zone.ZoneInfo\"5\n\x10GetStatusRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\"5\n\x11GetStatusResponse\x12 \n\x06status\x18\x01 \x03(\x0b\x32\x10.zone.ZoneStatus\"G\n\nAddRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\'\n\x05zones\x18\x02 \x03(\x0b\x32\x18.intrusion_zone.ZoneInfo\"\r\n\x0b\x41\x64\x64Response\"2\n\rDeleteRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\"\x10\n\x0e\x44\x65leteResponse\"$\n\x10\x44\x65leteAllRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"\x13\n\x11\x44\x65leteAllResponse\"A\n\rSetArmRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\x12\r\n\x05\x61rmed\x18\x03 \x01(\x08\"\x10\n\x0eSetArmResponse\"E\n\x0fSetAlarmRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\x12\x0f\n\x07\x61larmed\x18\x03 \x01(\x08\"\x12\n\x10SetAlarmResponse*J\n\tInputType\x12\x0e\n\nINPUT_NONE\x10\x00\x12\x0e\n\nINPUT_CARD\x10\x01\x12\r\n\tINPUT_KEY\x10\x02\x12\x0e\n\tINPUT_ALL\x10\xff\x01*\x92\x01\n\rOperationType\x12\x12\n\x0eOPERATION_NONE\x10\x00\x12\x11\n\rOPERATION_ARM\x10\x01\x12\x14\n\x10OPERATION_DISARM\x10\x02\x12\x14\n\x10OPERATION_TOGGLE\x10\x03\x12\x13\n\x0fOPERATION_ALARM\x10\x04\x12\x19\n\x15OPERATION_CLEAR_ALARM\x10\x08\x32\x99\x04\n\x12IntrusionAlarmZone\x12>\n\x03Get\x12\x1a.intrusion_zone.GetRequest\x1a\x1b.intrusion_zone.GetResponse\x12P\n\tGetStatus\x12 .intrusion_zone.GetStatusRequest\x1a!.intrusion_zone.GetStatusResponse\x12>\n\x03\x41\x64\x64\x12\x1a.intrusion_zone.AddRequest\x1a\x1b.intrusion_zone.AddResponse\x12G\n\x06\x44\x65lete\x12\x1d.intrusion_zone.DeleteRequest\x1a\x1e.intrusion_zone.DeleteResponse\x12P\n\tDeleteAll\x12 .intrusion_zone.DeleteAllRequest\x1a!.intrusion_zone.DeleteAllResponse\x12G\n\x06SetArm\x12\x1d.intrusion_zone.SetArmRequest\x1a\x1e.intrusion_zone.SetArmResponse\x12M\n\x08SetAlarm\x12\x1f.intrusion_zone.SetAlarmRequest\x1a .intrusion_zone.SetAlarmResponseBD\n!com.supremainc.sdk.intrusion_zoneP\x01Z\x1d\x62iostar/service/intrusionZoneb\x06proto3')
  ,
  dependencies=[zone__pb2.DESCRIPTOR,action__pb2.DESCRIPTOR,device__pb2.DESCRIPTOR,card__pb2.DESCRIPTOR,])

_INPUTTYPE = _descriptor.EnumDescriptor(
  name='InputType',
  full_name='intrusion_zone.InputType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INPUT_NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INPUT_CARD', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INPUT_KEY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INPUT_ALL', index=3, number=255,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1209,
  serialized_end=1283,
)
_sym_db.RegisterEnumDescriptor(_INPUTTYPE)

InputType = enum_type_wrapper.EnumTypeWrapper(_INPUTTYPE)
_OPERATIONTYPE = _descriptor.EnumDescriptor(
  name='OperationType',
  full_name='intrusion_zone.OperationType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OPERATION_NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPERATION_ARM', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPERATION_DISARM', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPERATION_TOGGLE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPERATION_ALARM', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPERATION_CLEAR_ALARM', index=5, number=8,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1286,
  serialized_end=1432,
)
_sym_db.RegisterEnumDescriptor(_OPERATIONTYPE)

OperationType = enum_type_wrapper.EnumTypeWrapper(_OPERATIONTYPE)
INPUT_NONE = 0
INPUT_CARD = 1
INPUT_KEY = 2
INPUT_ALL = 255
OPERATION_NONE = 0
OPERATION_ARM = 1
OPERATION_DISARM = 2
OPERATION_TOGGLE = 3
OPERATION_ALARM = 4
OPERATION_CLEAR_ALARM = 8



_MEMBER = _descriptor.Descriptor(
  name='Member',
  full_name='intrusion_zone.Member',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.Member.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input', full_name='intrusion_zone.Member.input', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operation', full_name='intrusion_zone.Member.operation', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=92,
  serialized_end=152,
)


_INPUT = _descriptor.Descriptor(
  name='Input',
  full_name='intrusion_zone.Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.Input.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='intrusion_zone.Input.port', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='switchType', full_name='intrusion_zone.Input.switchType', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration', full_name='intrusion_zone.Input.duration', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operation', full_name='intrusion_zone.Input.operation', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=270,
)


_OUTPUT = _descriptor.Descriptor(
  name='Output',
  full_name='intrusion_zone.Output',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='event', full_name='intrusion_zone.Output.event', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='intrusion_zone.Output.action', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=272,
  serialized_end=327,
)


_ZONEINFO = _descriptor.Descriptor(
  name='ZoneInfo',
  full_name='intrusion_zone.ZoneInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='zoneID', full_name='intrusion_zone.ZoneInfo.zoneID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='intrusion_zone.ZoneInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disabled', full_name='intrusion_zone.ZoneInfo.disabled', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='armDelay', full_name='intrusion_zone.ZoneInfo.armDelay', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alarmDelay', full_name='intrusion_zone.ZoneInfo.alarmDelay', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='doorIDs', full_name='intrusion_zone.ZoneInfo.doorIDs', index=5,
      number=6, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='groupIDs', full_name='intrusion_zone.ZoneInfo.groupIDs', index=6,
      number=7, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cards', full_name='intrusion_zone.ZoneInfo.cards', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='members', full_name='intrusion_zone.ZoneInfo.members', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inputs', full_name='intrusion_zone.ZoneInfo.inputs', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outputs', full_name='intrusion_zone.ZoneInfo.outputs', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=616,
)


_GETREQUEST = _descriptor.Descriptor(
  name='GetRequest',
  full_name='intrusion_zone.GetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.GetRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=618,
  serialized_end=648,
)


_GETRESPONSE = _descriptor.Descriptor(
  name='GetResponse',
  full_name='intrusion_zone.GetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='zones', full_name='intrusion_zone.GetResponse.zones', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=650,
  serialized_end=704,
)


_GETSTATUSREQUEST = _descriptor.Descriptor(
  name='GetStatusRequest',
  full_name='intrusion_zone.GetStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.GetStatusRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zoneIDs', full_name='intrusion_zone.GetStatusRequest.zoneIDs', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=706,
  serialized_end=759,
)


_GETSTATUSRESPONSE = _descriptor.Descriptor(
  name='GetStatusResponse',
  full_name='intrusion_zone.GetStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='intrusion_zone.GetStatusResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=761,
  serialized_end=814,
)


_ADDREQUEST = _descriptor.Descriptor(
  name='AddRequest',
  full_name='intrusion_zone.AddRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.AddRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zones', full_name='intrusion_zone.AddRequest.zones', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=816,
  serialized_end=887,
)


_ADDRESPONSE = _descriptor.Descriptor(
  name='AddResponse',
  full_name='intrusion_zone.AddResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=889,
  serialized_end=902,
)


_DELETEREQUEST = _descriptor.Descriptor(
  name='DeleteRequest',
  full_name='intrusion_zone.DeleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.DeleteRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zoneIDs', full_name='intrusion_zone.DeleteRequest.zoneIDs', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=904,
  serialized_end=954,
)


_DELETERESPONSE = _descriptor.Descriptor(
  name='DeleteResponse',
  full_name='intrusion_zone.DeleteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=956,
  serialized_end=972,
)


_DELETEALLREQUEST = _descriptor.Descriptor(
  name='DeleteAllRequest',
  full_name='intrusion_zone.DeleteAllRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.DeleteAllRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=974,
  serialized_end=1010,
)


_DELETEALLRESPONSE = _descriptor.Descriptor(
  name='DeleteAllResponse',
  full_name='intrusion_zone.DeleteAllResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1012,
  serialized_end=1031,
)


_SETARMREQUEST = _descriptor.Descriptor(
  name='SetArmRequest',
  full_name='intrusion_zone.SetArmRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.SetArmRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zoneIDs', full_name='intrusion_zone.SetArmRequest.zoneIDs', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='armed', full_name='intrusion_zone.SetArmRequest.armed', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1033,
  serialized_end=1098,
)


_SETARMRESPONSE = _descriptor.Descriptor(
  name='SetArmResponse',
  full_name='intrusion_zone.SetArmResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1100,
  serialized_end=1116,
)


_SETALARMREQUEST = _descriptor.Descriptor(
  name='SetAlarmRequest',
  full_name='intrusion_zone.SetAlarmRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='intrusion_zone.SetAlarmRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zoneIDs', full_name='intrusion_zone.SetAlarmRequest.zoneIDs', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alarmed', full_name='intrusion_zone.SetAlarmRequest.alarmed', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1118,
  serialized_end=1187,
)


_SETALARMRESPONSE = _descriptor.Descriptor(
  name='SetAlarmResponse',
  full_name='intrusion_zone.SetAlarmResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1189,
  serialized_end=1207,
)

_INPUT.fields_by_name['switchType'].enum_type = device__pb2._SWITCHTYPE
_OUTPUT.fields_by_name['action'].message_type = action__pb2._ACTION
_ZONEINFO.fields_by_name['cards'].message_type = card__pb2._CSNCARDDATA
_ZONEINFO.fields_by_name['members'].message_type = _MEMBER
_ZONEINFO.fields_by_name['inputs'].message_type = _INPUT
_ZONEINFO.fields_by_name['outputs'].message_type = _OUTPUT
_GETRESPONSE.fields_by_name['zones'].message_type = _ZONEINFO
_GETSTATUSRESPONSE.fields_by_name['status'].message_type = zone__pb2._ZONESTATUS
_ADDREQUEST.fields_by_name['zones'].message_type = _ZONEINFO
DESCRIPTOR.message_types_by_name['Member'] = _MEMBER
DESCRIPTOR.message_types_by_name['Input'] = _INPUT
DESCRIPTOR.message_types_by_name['Output'] = _OUTPUT
DESCRIPTOR.message_types_by_name['ZoneInfo'] = _ZONEINFO
DESCRIPTOR.message_types_by_name['GetRequest'] = _GETREQUEST
DESCRIPTOR.message_types_by_name['GetResponse'] = _GETRESPONSE
DESCRIPTOR.message_types_by_name['GetStatusRequest'] = _GETSTATUSREQUEST
DESCRIPTOR.message_types_by_name['GetStatusResponse'] = _GETSTATUSRESPONSE
DESCRIPTOR.message_types_by_name['AddRequest'] = _ADDREQUEST
DESCRIPTOR.message_types_by_name['AddResponse'] = _ADDRESPONSE
DESCRIPTOR.message_types_by_name['DeleteRequest'] = _DELETEREQUEST
DESCRIPTOR.message_types_by_name['DeleteResponse'] = _DELETERESPONSE
DESCRIPTOR.message_types_by_name['DeleteAllRequest'] = _DELETEALLREQUEST
DESCRIPTOR.message_types_by_name['DeleteAllResponse'] = _DELETEALLRESPONSE
DESCRIPTOR.message_types_by_name['SetArmRequest'] = _SETARMREQUEST
DESCRIPTOR.message_types_by_name['SetArmResponse'] = _SETARMRESPONSE
DESCRIPTOR.message_types_by_name['SetAlarmRequest'] = _SETALARMREQUEST
DESCRIPTOR.message_types_by_name['SetAlarmResponse'] = _SETALARMRESPONSE
DESCRIPTOR.enum_types_by_name['InputType'] = _INPUTTYPE
DESCRIPTOR.enum_types_by_name['OperationType'] = _OPERATIONTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Member = _reflection.GeneratedProtocolMessageType('Member', (_message.Message,), dict(
  DESCRIPTOR = _MEMBER,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.Member)
  ))
_sym_db.RegisterMessage(Member)

Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), dict(
  DESCRIPTOR = _INPUT,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.Input)
  ))
_sym_db.RegisterMessage(Input)

Output = _reflection.GeneratedProtocolMessageType('Output', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUT,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.Output)
  ))
_sym_db.RegisterMessage(Output)

ZoneInfo = _reflection.GeneratedProtocolMessageType('ZoneInfo', (_message.Message,), dict(
  DESCRIPTOR = _ZONEINFO,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.ZoneInfo)
  ))
_sym_db.RegisterMessage(ZoneInfo)

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.GetRequest)
  ))
_sym_db.RegisterMessage(GetRequest)

GetResponse = _reflection.GeneratedProtocolMessageType('GetResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETRESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.GetResponse)
  ))
_sym_db.RegisterMessage(GetResponse)

GetStatusRequest = _reflection.GeneratedProtocolMessageType('GetStatusRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETSTATUSREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.GetStatusRequest)
  ))
_sym_db.RegisterMessage(GetStatusRequest)

GetStatusResponse = _reflection.GeneratedProtocolMessageType('GetStatusResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETSTATUSRESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.GetStatusResponse)
  ))
_sym_db.RegisterMessage(GetStatusResponse)

AddRequest = _reflection.GeneratedProtocolMessageType('AddRequest', (_message.Message,), dict(
  DESCRIPTOR = _ADDREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.AddRequest)
  ))
_sym_db.RegisterMessage(AddRequest)

AddResponse = _reflection.GeneratedProtocolMessageType('AddResponse', (_message.Message,), dict(
  DESCRIPTOR = _ADDRESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.AddResponse)
  ))
_sym_db.RegisterMessage(AddResponse)

DeleteRequest = _reflection.GeneratedProtocolMessageType('DeleteRequest', (_message.Message,), dict(
  DESCRIPTOR = _DELETEREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.DeleteRequest)
  ))
_sym_db.RegisterMessage(DeleteRequest)

DeleteResponse = _reflection.GeneratedProtocolMessageType('DeleteResponse', (_message.Message,), dict(
  DESCRIPTOR = _DELETERESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.DeleteResponse)
  ))
_sym_db.RegisterMessage(DeleteResponse)

DeleteAllRequest = _reflection.GeneratedProtocolMessageType('DeleteAllRequest', (_message.Message,), dict(
  DESCRIPTOR = _DELETEALLREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.DeleteAllRequest)
  ))
_sym_db.RegisterMessage(DeleteAllRequest)

DeleteAllResponse = _reflection.GeneratedProtocolMessageType('DeleteAllResponse', (_message.Message,), dict(
  DESCRIPTOR = _DELETEALLRESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.DeleteAllResponse)
  ))
_sym_db.RegisterMessage(DeleteAllResponse)

SetArmRequest = _reflection.GeneratedProtocolMessageType('SetArmRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETARMREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.SetArmRequest)
  ))
_sym_db.RegisterMessage(SetArmRequest)

SetArmResponse = _reflection.GeneratedProtocolMessageType('SetArmResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETARMRESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.SetArmResponse)
  ))
_sym_db.RegisterMessage(SetArmResponse)

SetAlarmRequest = _reflection.GeneratedProtocolMessageType('SetAlarmRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETALARMREQUEST,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.SetAlarmRequest)
  ))
_sym_db.RegisterMessage(SetAlarmRequest)

SetAlarmResponse = _reflection.GeneratedProtocolMessageType('SetAlarmResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETALARMRESPONSE,
  __module__ = 'intrusion_zone_pb2'
  # @@protoc_insertion_point(class_scope:intrusion_zone.SetAlarmResponse)
  ))
_sym_db.RegisterMessage(SetAlarmResponse)


DESCRIPTOR._options = None

_INTRUSIONALARMZONE = _descriptor.ServiceDescriptor(
  name='IntrusionAlarmZone',
  full_name='intrusion_zone.IntrusionAlarmZone',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1435,
  serialized_end=1972,
  methods=[
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='intrusion_zone.IntrusionAlarmZone.Get',
    index=0,
    containing_service=None,
    input_type=_GETREQUEST,
    output_type=_GETRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetStatus',
    full_name='intrusion_zone.IntrusionAlarmZone.GetStatus',
    index=1,
    containing_service=None,
    input_type=_GETSTATUSREQUEST,
    output_type=_GETSTATUSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Add',
    full_name='intrusion_zone.IntrusionAlarmZone.Add',
    index=2,
    containing_service=None,
    input_type=_ADDREQUEST,
    output_type=_ADDRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Delete',
    full_name='intrusion_zone.IntrusionAlarmZone.Delete',
    index=3,
    containing_service=None,
    input_type=_DELETEREQUEST,
    output_type=_DELETERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteAll',
    full_name='intrusion_zone.IntrusionAlarmZone.DeleteAll',
    index=4,
    containing_service=None,
    input_type=_DELETEALLREQUEST,
    output_type=_DELETEALLRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetArm',
    full_name='intrusion_zone.IntrusionAlarmZone.SetArm',
    index=5,
    containing_service=None,
    input_type=_SETARMREQUEST,
    output_type=_SETARMRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetAlarm',
    full_name='intrusion_zone.IntrusionAlarmZone.SetAlarm',
    index=6,
    containing_service=None,
    input_type=_SETALARMREQUEST,
    output_type=_SETALARMRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_INTRUSIONALARMZONE)

DESCRIPTOR.services_by_name['IntrusionAlarmZone'] = _INTRUSIONALARMZONE

# @@protoc_insertion_point(module_scope)