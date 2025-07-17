bl_info = {
    "name": "UNITE Material Maker",
    "blender": (3, 6, 0), 
    "category": "Material",
}

import bpy
import os
import json
class TextureImporterPanel(bpy.types.Panel):
    bl_label = "Texture Importer"
    bl_idname = "MATERIAL_PT_texture_importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UNITE Materials'

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "json_path")
        layout.operator("material.create_texture_material")

class TEXTURE_PT_file_browser(bpy.types.Operator):
    bl_idname = "material.create_texture_material"
    bl_label = "Create Material with Textures"

    def execute(self, context):
        folder_path = bpy.path.abspath(context.scene.json_path)
        
        if not os.path.isdir(folder_path):
            self.report({'ERROR'}, "Invalid folder path.")
            return {'CANCELLED'}

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                json_path = os.path.join(folder_path, filename)
                material_name = os.path.splitext(filename)[0]
                self.create_or_update_material(json_path, material_name)
        
        self.report({'INFO'}, "Materials updated from JSON files in the folder.")
        return {'FINISHED'}



    def create_or_update_material(self, json_path, material_name):

        def handle_duplicates(material_name, new_material):
            # Track all materials with the same name
            duplicates = [mat for mat in bpy.data.materials if material_name in mat.name ]
            
            if len(duplicates) > 1:
                # Replace duplicate usage and delete them
                main_material = duplicates[0]  # Keep the first material as main
                for duplicate in duplicates[1:]:
                    for obj in bpy.data.objects:
                        if obj.type == 'MESH':
                            for slot in obj.material_slots:
                                if slot.material == duplicate:
                                    slot.material = main_material
                    bpy.data.materials.remove(duplicate)
                print(f"Removed {len(duplicates) - 1} duplicates for material '{material_name}'.")
        
            # Ensure the new material is named correctly
            new_material.name = material_name

        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error reading {json_path}: {e}")
            return
        saved_properties = data.get('m_SavedProperties', {}).get('m_TexEnvs', {})
        saved_properties2 = data.get('m_SavedProperties', {}).get('m_Colors', {})
        base_path = os.path.dirname(json_path.replace("\Materials", ""))
        base_color_path = os.path.join(base_path, saved_properties.get('_MainTex', {}).get('m_Texture', {}).get('Name', '') + '.png')
        try:
            basemap0_color_path = os.path.join(base_path, saved_properties.get('_BaseMap0', {}).get('m_Texture', {}).get('Name', '') + '.png')
        except:
            basemap0_color_path = None
        try:
            basemap1_color_path = os.path.join(base_path, saved_properties.get('_BaseMap1', {}).get('m_Texture', {}).get('Name', '') + '.png')
        except:
            basemap1_color_path = None
            
        mroe_path = os.path.join(base_path, saved_properties.get('_MixMap', {}).get('m_Texture', {}).get('Name', '') + '.png')
        print(saved_properties.get('_MixMap', {}).get('m_Texture', {}).get('Name', ''))
        try:
            a = saved_properties2.get('_ColorSkin', '')
            
            colorskin = (a.get('r', ''),a.get('g', ''),a.get('b', ''),a.get('a',''))
        except:
            colorskin = (0.0,0.0,0.0,1.0)
        
        normal_map_path = os.path.join(base_path, saved_properties.get('_BumpMap', {}).get('m_Texture', {}).get('Name', '') + '.png')
        if not os.path.exists(normal_map_path):
            normal_map_path = os.path.join(base_path, saved_properties.get('_NormalMap', {}).get('m_Texture', {}).get('Name', '') + '.png')
        
        # Check if material exists or create it
        material = bpy.data.materials.get(material_name)
        if not material:
            material = bpy.data.materials.new(name=material_name)
        else:
            print(f"Material '{material_name}' already exists. Updating it.")
        
        handle_duplicates(material_name, material)
        
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()  # Clear existing nodes

        # Create the material nodes
        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])
        principled_bsdf.inputs['Base Color'].default_value = colorskin
        if os.path.exists(base_color_path):
            tex_image = nodes.new(type='ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(base_color_path)
            tex_image.image.alpha_mode = 'CHANNEL_PACKED'
            links.new(tex_image.outputs['Color'], principled_bsdf.inputs['Base Color'])

        if os.path.exists(basemap0_color_path):
            mix_color1 = material.node_tree.nodes.new("ShaderNodeMixRGB")
            texmap0_image = nodes.new(type='ShaderNodeTexImage')
            texmap0_image.image = bpy.data.images.load(basemap0_color_path)
            texmap0_image.image.alpha_mode = 'CHANNEL_PACKED'
            texmap1_image = nodes.new(type='ShaderNodeTexImage')
            texmap1_image.image = bpy.data.images.load(basemap1_color_path)
            texmap1_image.image.alpha_mode = 'CHANNEL_PACKED'
            links.new(texmap0_image.outputs['Color'], mix_color1.inputs[1])
            links.new(texmap0_image.outputs['Alpha'], mix_color1.inputs[0])
            links.new(texmap1_image.outputs['Color'], mix_color1.inputs[2])
            links.new(mix_color1.outputs[0], principled_bsdf.inputs['Base Color'])

        
        if mroe_path and os.path.exists(mroe_path):
            mroe_tex_image = nodes.new(type='ShaderNodeTexImage')
            mroe_tex_image.image = bpy.data.images.load(mroe_path)
            mroe_tex_image.image.colorspace_settings.name = "Non-Color"
            separate_color = nodes.new(type='ShaderNodeSeparateColor')
            links.new(mroe_tex_image.outputs[0], separate_color.inputs[0])
            links.new(separate_color.outputs[0], principled_bsdf.inputs['Metallic'])
            links.new(separate_color.outputs[1], principled_bsdf.inputs['Roughness'])
        
        if normal_map_path and os.path.exists(normal_map_path):
            print("existeputo")
            normal_tex_image = nodes.new(type='ShaderNodeTexImage')
            normal_tex_image.image = bpy.data.images.load(normal_map_path)
            normal_tex_image.image.colorspace_settings.name = "Non-Color"
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            links.new(normal_tex_image.outputs['Color'], normal_map.inputs['Color'])
            links.new(normal_map.outputs['Normal'], principled_bsdf.inputs['Normal'])
            if "t_nm" in normal_map_path:
                links.new(normal_tex_image.outputs['Alpha'], principled_bsdf.inputs['Metallic'])

def update_texture_paths(self, context):
    pass

def register():
    bpy.utils.register_class(TextureImporterPanel)
    bpy.utils.register_class(TEXTURE_PT_file_browser)

    bpy.types.Scene.json_path = bpy.props.StringProperty(
        name="Material JSON",
        description="Path to the base color texture",
        subtype='FILE_PATH',
        update=update_texture_paths
    )

def unregister():
    bpy.utils.unregister_class(TextureImporterPanel)
    bpy.utils.unregister_class(TEXTURE_PT_file_browser)
    
    del bpy.types.Scene.json_path

if __name__ == "__main__":
    register()
