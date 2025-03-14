# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Animation

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class TrackFlagsInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TrackFlagsInfo()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsTrackFlagsInfo(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # TrackFlagsInfo
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # TrackFlagsInfo
    def ValuesType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # TrackFlagsInfo
    def Values(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def TrackFlagsInfoStart(builder):
    builder.StartObject(2)

def Start(builder):
    TrackFlagsInfoStart(builder)

def TrackFlagsInfoAddValuesType(builder, valuesType):
    builder.PrependUint8Slot(0, valuesType, 0)

def AddValuesType(builder, valuesType):
    TrackFlagsInfoAddValuesType(builder, valuesType)

def TrackFlagsInfoAddValues(builder, values):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(values), 0)

def AddValues(builder, values):
    TrackFlagsInfoAddValues(builder, values)

def TrackFlagsInfoEnd(builder):
    return builder.EndObject()

def End(builder):
    return TrackFlagsInfoEnd(builder)
