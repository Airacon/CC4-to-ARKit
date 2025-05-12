bl_info = {
    "name": "CC4 to ARKit Renamer",
    "author": "ChatGPT",
    "version": (5, 0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar (N Panel) > CC4 ARKit",
    "description": "Renames all CC4 expression shape keys to ARKit standard names.",
    "category": "Object",
}

import bpy
from bpy.props import PointerProperty

# Custom property to mark converted objects
CONVERSION_FLAG = "cc4_to_arkit_converted"

# Combined mapping: ARKit name -> list of CC4 aliases
MAPPINGS = [
    ("eyeBlinkLeft",    ["Eye_Blink_L"]),
    ("eyeBlinkRight",   ["Eye_Blink_R"]),
    ("eyeSquintLeft",   ["Eye_Squint_L"]),
    ("eyeSquintRight",  ["Eye_Squint_R"]),
    ("eyeLookDownLeft", ["Eye_L_Look_Down"]),
    ("eyeLookDownRight",["Eye_R_Look_Down"]),
    ("eyeLookInLeft",   ["Eye_L_Look_R"]),
    ("eyeLookInRight",  ["Eye_R_Look_L"]),
    ("eyeLookOutLeft",  ["Eye_L_Look_L"]),
    ("eyeLookOutRight", ["Eye_R_Look_R"]),
    ("eyeLookUpLeft",   ["Eye_LookUp_L", "Eye_L_Look_Up"]),
    ("eyeLookUpRight",  ["Eye_LookUp_R", "Eye_R_Look_Up"]),
    ("jawOpen",         ["V_Open", "VOpen", "V Open"]),
    ("eyeWideLeft",     ["Eye_Wide_L"]),
    ("eyeWideRight",    ["Eye_Wide_R"]),
    ("jawForward",      ["Jaw_Forward"]),
    ("jawLeft",         ["Jaw_L", "Mouth_L"]),
    ("jawRight",        ["Jaw_R", "Mouth_R"]),
    ("mouthClose",      ["Mouth_Close"]),
    ("mouthFunnel",     ["Mouth_Funnel", "V_Affricate"]),
    ("mouthPucker",     ["Mouth_Pucker", "V_Tight_O"]),
    ("mouthSmileLeft",  ["Mouth_Smile_L"]),
    ("mouthSmileRight", ["Mouth_Smile_R"]),
    ("mouthFrownLeft",  ["Mouth_Frown_L"]),
    ("mouthFrownRight", ["Mouth_Frown_R"]),
    ("mouthDimpleLeft", ["Mouth_Dimple_L"]),
    ("mouthDimpleRight",["Mouth_Dimple_R"]),
    ("mouthShrugUpper", ["Mouth_Shrug_Upper"]),
    ("mouthShrugLower", ["Mouth_Shrug_Lower"]),
    ("mouthStretchLeft",["Mouth_Stretch_L"]),
    ("mouthStretchRight",["Mouth_Stretch_R"]),
    ("mouthPressLeft",  ["Mouth_Press_L", "Mouth_Upper_L"]),
    ("mouthPressRight", ["Mouth_Press_R", "Mouth_Upper_R"]),
    ("mouthLowerDownLeft",  ["Mouth_Down_Lower_L"]),
    ("mouthLowerDownRight", ["Mouth_Down_Lower_R"]),
    ("mouthUpperUpLeft",    ["Mouth_UpperUp_L", "Mouth_Up_Upper_L"]),
    ("mouthUpperUpRight",   ["Mouth_UpperUp_R", "Mouth_Up_Upper_R"]),
    ("browDownLeft",    ["Brow_Drop_L"]),
    ("browDownRight",   ["Brow_Drop_R"]),
    ("browInnerUpLeft", ["Brow_Raise_Inner_L"]),
    ("browInnerUpRight",["Brow_Raise_Inner_R"]),
    ("browOuterUpLeft", ["Brow_Raise_Outer_L"]),
    ("browOuterUpRight",["Brow_Raise_Outer_R"]),
    ("cheekPuffLeft",   ["Cheek_Puff_L"]),
    ("cheekPuffRight",  ["Cheek_Puff_R"]),
    ("cheekSquintLeft", ["Cheek_Raise_L"]),
    ("cheekSquintRight",["Cheek_Raise_R"]),
    ("noseSneerLeft",   ["Nose_Sneer_L"]),
    ("noseSneerRight",  ["Nose_Sneer_R"]),
    ("tongueOut",       ["Tongue_Out"]),
    ("tongueUp",        ["Tongue_Up"]),
    ("tongueDown",      ["Tongue_Down"]),
    ("tongueTipUp",     ["Tongue_Tip_Up"]),
    ("tongueTipDown",   ["Tongue_Tip_Down"]),
    ("tongueNarrow",    ["Tongue_Narrow"]),
    ("tongueWide",      ["Tongue_Wide"]),
    ("tongueRoll",      ["Tongue_Roll"]),
    ("tongueLeft",      ["Tongue_L"]),
    ("tongueRight",     ["Tongue_R"]),
    ("tongueBulgeLeft", ["Tongue_Bulge_L"]),
    ("tongueBulgeRight",["Tongue_Bulge_R"]),
]

class CC4ARKITSettings(bpy.types.PropertyGroup):
    base_mesh: PointerProperty(
        name="Base Mesh",
        type=bpy.types.Object,
        description="Select the mesh to convert",
        poll=lambda self, obj: obj.type == 'MESH'
    )

# Build mapping dict for quick lookup
def build_mapping():
    return {alias: arkit for arkit, aliases in MAPPINGS for alias in aliases}

# Check if object needs conversion
def needs_conversion(obj):
    if not (obj and obj.data.shape_keys):
        return False
    names = {sk.name for sk in obj.data.shape_keys.key_blocks}
    return bool(names & set(build_mapping().keys())) and not obj.get(CONVERSION_FLAG, False)

class OBJECT_OT_convert_cc4_to_arkit(bpy.types.Operator):
    bl_idname = "object.convert_cc4_to_arkit"
    bl_label = "Convert CC4 to ARKit"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.cc4_arkit_settings.base_mesh and needs_conversion(context.scene.cc4_arkit_settings.base_mesh))

    def execute(self, context):
        obj = context.scene.cc4_arkit_settings.base_mesh
        inv_map = build_mapping()
        renamed = 0
        for sk in obj.data.shape_keys.key_blocks:
            if sk.name in inv_map:
                sk.name = inv_map[sk.name]
                renamed += 1
        obj[CONVERSION_FLAG] = True
        self.report({'INFO'}, f"Renamed {renamed} shape key(s) to ARKit names.")
        return {'FINISHED'}

class OBJECT_OT_revert_arkit_to_cc4(bpy.types.Operator):
    bl_idname = "object.revert_arkit_to_cc4"
    bl_label = "Revert ARKit to CC4"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.scene.cc4_arkit_settings.base_mesh
        return bool(obj and obj.get(CONVERSION_FLAG, False))

    def execute(self, context):
        obj = context.scene.cc4_arkit_settings.base_mesh
        # revert to first listed alias
        mapping = {arkit: aliases[0] for arkit, aliases in MAPPINGS}
        reverted = 0
        for sk in obj.data.shape_keys.key_blocks:
            if sk.name in mapping:
                sk.name = mapping[sk.name]
                reverted += 1
        del obj[CONVERSION_FLAG]
        self.report({'INFO'}, f"Reverted {reverted} shape key(s) to CC4 names.")
        return {'FINISHED'}

class VIEW3D_PT_cc4_to_arkit_panel(bpy.types.Panel):
    bl_label = "CC4 → ARKit"
    bl_idname = "VIEW3D_PT_cc4_to_arkit_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CC4 ARKit"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.cc4_arkit_settings
        layout.prop(settings, "base_mesh")
        mesh = settings.base_mesh
        if not mesh:
            layout.label(text="Select a mesh to convert", icon='ERROR')
        else:
            if mesh.get(CONVERSION_FLAG):
                layout.label(text="Already converted", icon='CHECKMARK')
                layout.operator("object.revert_arkit_to_cc4", icon='LOOP_BACK')
            elif needs_conversion(mesh):
                layout.operator("object.convert_cc4_to_arkit", icon='SHAPEKEY_DATA')
            else:
                layout.label(text="No CC4 keys found to convert", icon='INFO')

classes = (
    CC4ARKITSettings,
    OBJECT_OT_convert_cc4_to_arkit,
    OBJECT_OT_revert_arkit_to_cc4,
    VIEW3D_PT_cc4_to_arkit_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cc4_arkit_settings = PointerProperty(type=CC4ARKITSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cc4_arkit_settings

if __name__ == "__main__":
    register()
