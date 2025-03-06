# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Animation

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class TrackMaterial(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TrackMaterial()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsTrackMaterial(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # TrackMaterial
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # TrackMaterial
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # TrackMaterial
    def InitValues(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from Titan.Animation.TrackMaterialInit import TrackMaterialInit
            obj = TrackMaterialInit()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TrackMaterial
    def InitValuesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TrackMaterial
    def InitValuesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # TrackMaterial
    def AnimValues(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from Titan.Animation.TrackMaterialAnim import TrackMaterialAnim
            obj = TrackMaterialAnim()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TrackMaterial
    def AnimValuesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TrackMaterial
    def AnimValuesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

def TrackMaterialStart(builder):
    builder.StartObject(3)

def Start(builder):
    TrackMaterialStart(builder)

def TrackMaterialAddName(builder, name):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)

def AddName(builder, name):
    TrackMaterialAddName(builder, name)

def TrackMaterialAddInitValues(builder, initValues):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(initValues), 0)

def AddInitValues(builder, initValues):
    TrackMaterialAddInitValues(builder, initValues)

def TrackMaterialStartInitValuesVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartInitValuesVector(builder, numElems: int) -> int:
    return TrackMaterialStartInitValuesVector(builder, numElems)

def TrackMaterialAddAnimValues(builder, animValues):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(animValues), 0)

def AddAnimValues(builder, animValues):
    TrackMaterialAddAnimValues(builder, animValues)

def TrackMaterialStartAnimValuesVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartAnimValuesVector(builder, numElems: int) -> int:
    return TrackMaterialStartAnimValuesVector(builder, numElems)

def TrackMaterialEnd(builder):
    return builder.EndObject()

def End(builder):
    return TrackMaterialEnd(builder)
