import flatbuffers
import json
import Titan.Model.TRMMT  # Import TRMMT schema
import Titan.Animation.TRACM  # Import TRACM schema
import sys

def parse_track_material_value(value):
    """ Parses TrackMaterialValue. """
    return {
        "time": value.Time(),
        "value": value.Value(),
        "config_0": value.Config0(),
        "config_1": value.Config1(),
        "config_2": value.Config2()
    }

def parse_track_material_value_list(value_list):
    """ Parses TrackMaterialValueList. """
    return [parse_track_material_value(value_list.Values(i)) for i in range(value_list.ValuesLength())]

def parse_track_material_channels(channels):
    """ Parses TrackMaterialChannels. """
    return {
        "red": parse_track_material_value_list(channels.Red()),
        "green": parse_track_material_value_list(channels.Green()),
        "blue": parse_track_material_value_list(channels.Blue()),
        "alpha": parse_track_material_value_list(channels.Alpha())
    }

def parse_track_material(material):
    """ Parses TrackMaterial. """
    return {
        "name": material.Name().decode(),
        "init_values": [
            {
                "name": init.Name().decode(),
                "list": parse_track_material_value_list(init.List())
            }
            for init in (material.InitValues(i) for i in range(material.InitValuesLength()))
        ],
        "anim_values": [
            {
                "name": anim.Name().decode(),
                "list": parse_track_material_channels(anim.List())
            }
            for anim in (material.AnimValues(i) for i in range(material.AnimValuesLength()))
        ]
    }

def parse_track_material_timeline(timeline):
    """ Parses TrackMaterialTimeline. """
    return {
        "res_0": timeline.Res0(),
        "res_1": timeline.Res1(),
        "material_track": [parse_track_material(timeline.MaterialTrack(i)) for i in range(timeline.MaterialTrackLength())],
        "unk_3": timeline.Unk3(),
        "unk_4": timeline.Unk4()
    }

def parse_blendshape_timeline(blendshape):
    """ Parses BlendShapeTimeline. """
    return {
        "res_0": blendshape.Res0(),
        "res_1": blendshape.Res1(),
        "material_track": [parse_track_material(blendshape.MaterialTrack(i)) for i in range(blendshape.MaterialTrackLength())],
        "unk_3": blendshape.Unk3(),
        "unk_4": blendshape.Unk4()
    }

def parse_track(track):
    """ Parses Track table. """
    return {
        "track_path": track.TrackPath().decode(),
        "res_1": track.Res1(),
        "res_2": track.Res2(),
        "res_3": track.Res3(),
        "material_animation": parse_track_material_timeline(track.MaterialAnimation()),
    }

def parse_tracm(tracm_bytes):
    """ Parses TRACM FlatBuffer from EmbeddedTRACM. """
    tracm = Titan.Animation.TRACM.TRACM.GetRootAsTRACM(tracm_bytes, 0)
    
    return {
        "config": {
            "res_0": tracm.Config().Res0(),
            "duration": tracm.Config().Duration(),
            "framerate": tracm.Config().Framerate()
        },
        "tracks": [parse_track(tracm.Tracks(i)) for i in range(tracm.TracksLength())],
        "len_1": tracm.Len1(),
        "len_2": tracm.Len2()
    }

def parse_embedded_tracm(tracm):
    """ Extracts and parses the EmbeddedTRACM FlatBuffer. """
    if not tracm:
        return None

    tracm_bytes = tracm.BytebufferAsNumpy().tobytes()
    return parse_tracm(tracm_bytes)

def parse_mmt(mmt):
    """ Parses MMT table. """
    return {
        "name": mmt.Name().decode() if mmt.Name() else "",
        "material_name": [mmt.MaterialName(i).decode() for i in range(mmt.MaterialNameLength())],
        "material_switches": [
            {
                "material_name": mmt.MaterialSwitches(i).MaterialName().decode(),
                "material_flag": mmt.MaterialSwitches(i).MaterialFlag()
            }
            for i in range(mmt.MaterialSwitchesLength())
        ],
        "material_properties": [
            {
                "name": prop.Name().decode(),
                "mappers": [
                    {
                        "mesh_name": mapper.MeshName().decode(),
                        "material_name": mapper.MaterialName().decode(),
                        "layer_name": mapper.LayerName().decode(),
                    }
                    for mapper in (prop.Mappers(j) for j in range(prop.MappersLength()))
                ],
                "res_2": prop.Res2(),
                "unk_3": prop.Unk3(),
                "tracm": parse_embedded_tracm(prop.Tracm()),  # Parse embedded TRACM
                "res_5": [prop.Res5(j) for j in range(prop.Res5Length())]
            }
            for prop in (mmt.MaterialProperties(i) for i in range(mmt.MaterialPropertiesLength()))
        ]
    }

def read_trmmt(file_path):
    """ Reads and parses TRMMT FlatBuffer. """
    with open(file_path, "rb") as f:
        buf = f.read()
    
    trmmt = Titan.Model.TRMMT.TRMMT.GetRootAsTRMMT(buf, 0)

    json_data = {
        "res_0": trmmt.Res0(),
        "res_1": trmmt.Res1(),
        "material": [parse_mmt(trmmt.Material(i)) for i in range(trmmt.MaterialLength())]
    }

    return json_data

# Example usage
file_path = sys.argv[1]
json_output = read_trmmt(file_path)

# Save to a file or print
with open("output.json", "w") as f:
    json.dump(json_output, f, indent=4)

print(json.dumps(json_output, indent=4))
