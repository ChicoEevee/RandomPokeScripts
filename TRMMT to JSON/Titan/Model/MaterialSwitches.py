# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Model

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class MaterialSwitches(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MaterialSwitches()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMaterialSwitches(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # MaterialSwitches
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # MaterialSwitches
    def MaterialName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # MaterialSwitches
    def MaterialFlag(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

def MaterialSwitchesStart(builder):
    builder.StartObject(2)

def Start(builder):
    MaterialSwitchesStart(builder)

def MaterialSwitchesAddMaterialName(builder, materialName):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(materialName), 0)

def AddMaterialName(builder, materialName):
    MaterialSwitchesAddMaterialName(builder, materialName)

def MaterialSwitchesAddMaterialFlag(builder, materialFlag):
    builder.PrependUint8Slot(1, materialFlag, 0)

def AddMaterialFlag(builder, materialFlag):
    MaterialSwitchesAddMaterialFlag(builder, materialFlag)

def MaterialSwitchesEnd(builder):
    return builder.EndObject()

def End(builder):
    return MaterialSwitchesEnd(builder)
