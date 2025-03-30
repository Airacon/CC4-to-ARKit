bl_info = {
    "name": "CC4 to ARKit Renamer with Jaw Open",
    "author": "ChatGPT (Merged)",
    "version": (3, 0, 3),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar (N Panel) > CC4 ARKit",
    "description": ("Allows user selection of an Armature, Jaw Bone and Base Mesh. "
                    "When converting, the Jaw Open process is performed and CC4 shape keys are renamed to ARKit names. "
                    "If Teeth and/or Tongue exist, vertex groups are created so that during conversion these parts are merged. "
                    "The jaw bone is restored to its original rotation after conversion. "
                    "The Revert functionality remains in the code but its UI button is disabled."),
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy
import math

# --- Custom Property Key for conversion flag ---
CONVERSION_PROP = "cc4_to_arkit_converted"

# --- Helper Functions (global scope) ---
def needs_conversion(obj):
    if not obj or not obj.data.shape_keys:
        return False
    shape_keys = obj.data.shape_keys.key_blocks
    convertible = set(arkit_mapping_standard.values()).union(set(arkit_mapping_extended.values()))
    for sk in shape_keys:
        if sk.name in convertible:
            return True
    return False

def detect_expression_type(obj):
    if not (obj and obj.data.shape_keys):
        return None
    shape_keys = obj.data.shape_keys.key_blocks
    standard_matches = sum(1 for sk in shape_keys if sk.name in arkit_mapping_standard.values())
    extended_matches = sum(1 for sk in shape_keys if sk.name in arkit_mapping_extended.values())
    if extended_matches > standard_matches:
        return "Extended"
    elif standard_matches > 0:
        return "Standard"
    return None

# --- ARKit Mappings ---
arkit_mapping_standard = {
    "EyeBlinkLeft": "Eye_Blink_L",
    "EyeBlinkRight": "Eye_Blink_R",
    "EyeLookDownLeft": "Eye_L_Look_Down",
    "EyeLookDownRight": "Eye_R_Look_Down",
    "EyeLookInLeft": "Eye_L_Look_R",
    "EyeLookInRight": "Eye_R_Look_L",
    "EyeLookOutLeft": "Eye_L_Look_L",
    "EyeLookOutRight": "Eye_R_Look_R",
    "EyeLookUpLeft": "Eye_LookUp_L",
    "EyeLookUpRight": "Eye_LookUp_R",
    "JawForward": "Jaw_Forward",
    "JawOpen": "Jaw_Open",  # Original CC4 key
    "MouthClose": "Mouth_Close",
    "MouthFunnel": "Mouth_Funnel",
    "MouthPucker": "Mouth_Pucker",
    "MouthSmileLeft": "Mouth_Smile_L",
    "MouthSmileRight": "Mouth_Smile_R",
    "MouthFrownLeft": "Mouth_Frown_L",
    "MouthFrownRight": "Mouth_Frown_R",
    "MouthDimpleLeft": "Mouth_Dimple_L",
    "MouthDimpleRight": "Mouth_Dimple_R",
    "MouthStretchLeft": "Mouth_Stretch_L",
    "MouthStretchRight": "Mouth_Stretch_R",
    "MouthPressLeft": "Mouth_Press_L",
    "MouthPressRight": "Mouth_Press_R",
    "MouthLowerDownLeft": "Mouth_Down_Lower_L",
    "MouthLowerDownRight": "Mouth_Down_Lower_R",
    "MouthUpperUpLeft": "Mouth_UpperUp_L",
    "MouthUpperUpRight": "Mouth_UpperUp_R",
    "BrowDownLeft": "Brow_Drop_L",
    "BrowDownRight": "Brow_Drop_R",
    "BrowInnerUpLeft": "Brow_Raise_Inner_L",
    "BrowInnerUpRight": "Brow_Raise_Inner_R",
    "BrowOuterUpLeft": "Brow_Raise_Outer_L",
    "BrowOuterUpRight": "Brow_Raise_Outer_R",
    "CheekPuffLeft": "Cheek_Puff_L",
    "CheekPuffRight": "Cheek_Puff_R",
    "CheekSquintLeft": "Cheek_Raise_L",
    "CheekSquintRight": "Cheek_Raise_R",
    "NoseSneerLeft": "Nose_Sneer_L",
    "NoseSneerRight": "Nose_Sneer_R",
    "TongueOut": "Tongue_Out"
}

arkit_mapping_extended = {
    "BrowInnerUpLeft": "Brow_Raise_Inner_L",
    "BrowInnerUpRight": "Brow_Raise_Inner_R",
    "BrowOuterUpLeft": "Brow_Raise_Outer_L",
    "BrowOuterUpRight": "Brow_Raise_Outer_R",
    "BrowDownLeft": "Brow_Drop_L",
    "BrowDownRight": "Brow_Drop_R",
    "EyeBlinkLeft": "Eye_Blink_L",
    "EyeBlinkRight": "Eye_Blink_R",
    "EyeSquintLeft": "Eye_Squint_L",
    "EyeSquintRight": "Eye_Squint_R",
    "EyeWideLeft": "Eye_Wide_L",
    "EyeWideRight": "Eye_Wide_R",
    "EyeLookOutLeft": "Eye_L_Look_L",
    "EyeLookInRight": "Eye_R_Look_L",
    "EyeLookInLeft": "Eye_L_Look_R",
    "EyeLookOutRight": "Eye_R_Look_R",
    "EyeLookUpLeft": "Eye_L_Look_Up",
    "EyeLookUpRight": "Eye_R_Look_Up",
    "EyeLookDownLeft": "Eye_L_Look_Down",
    "EyeLookDownRight": "Eye_R_Look_Down",
    "NoseSneerLeft": "Nose_Sneer_L",
    "NoseSneerRight": "Nose_Sneer_R",
    "CheekSquintLeft": "Cheek_Raise_L",
    "CheekSquintRight": "Cheek_Raise_R",
    "CheekPuffLeft": "Cheek_Puff_L",
    "CheekPuffRight": "Cheek_Puff_R",
    "MouthSmileLeft": "Mouth_Smile_L",
    "MouthSmileRight": "Mouth_Smile_R",
    "MouthFrownLeft": "Mouth_Frown_L",
    "MouthFrownRight": "Mouth_Frown_R",
    "MouthStretchLeft": "Mouth_Stretch_L",
    "MouthStretchRight": "Mouth_Stretch_R",
    "MouthDimpleLeft": "Mouth_Dimple_L",
    "MouthDimpleRight": "Mouth_Dimple_R",
    "MouthPressLeft": "Mouth_Press_L",
    "MouthPressRight": "Mouth_Press_R",
    "MouthLeft": "Mouth_L",
    "MouthRight": "Mouth_R",
    "MouthShrugUpper": "Mouth_Shrug_Upper",
    "MouthShrugLower": "Mouth_Shrug_Lower",
    "MouthUpperUpLeft": "Mouth_Up_Upper_L",
    "MouthUpperUpRight": "Mouth_Up_Upper_R",
    "MouthLowerDownLeft": "Mouth_Down_Lower_L",
    "MouthLowerDownRight": "Mouth_Down_Lower_R",
    "MouthClose": "Mouth_Close",
    "TongueOut": "Tongue_Out",
    "TongueUp": "Tongue_Up",
    "TongueDown": "Tongue_Down",
    "TongueTipUp": "Tongue_Tip_Up",
    "TongueTipDown": "Tongue_Tip_Down",
    "TongueNarrow": "Tongue_Narrow",
    "TongueWide": "Tongue_Wide",
    "TongueRoll": "Tongue_Roll",
    "TongueLeft": "Tongue_L",
    "TongueRight": "Tongue_R",
    "TongueBulgeLeft": "Tongue_Bulge_L",
    "TongueBulgeRight": "Tongue_Bulge_R",
    "JawOpen": "Jaw_Open",
    "JawForward": "Jaw_Forward",
    "JawLeft": "Jaw_L",
    "JawRight": "Jaw_R"
}

# --- Property Group for User Settings ---
class CC4_ARKit_Settings(bpy.types.PropertyGroup):
    armature_obj: bpy.props.PointerProperty(
        name="Armature",
        type=bpy.types.Object,
        description="Select the Armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    base_mesh: bpy.props.PointerProperty(
        name="Base Mesh",
        type=bpy.types.Object,
        description="Select the Base Mesh to convert",
        poll=lambda self, obj: obj.type == 'MESH'
    )
    def get_jaw_bone_items(self, context):
        items = []
        if self.armature_obj and self.armature_obj.data:
            for bone in self.armature_obj.data.bones:
                items.append((bone.name, bone.name, ""))
        return items
    jaw_bone: bpy.props.EnumProperty(
        name="Jaw Bone",
        description="Select the Jaw Bone from the Armature",
        items=get_jaw_bone_items
    )

# --- ARKit Conversion Functions ---
def convert_cc4_to_arkit():
    obj = bpy.context.scene.cc4_arkit_settings.base_mesh
    if not (obj and obj.type == 'MESH' and obj.data.shape_keys):
        return {'CANCELLED'}
    expr_type = detect_expression_type(obj)
    mapping = (arkit_mapping_extended if expr_type == "Extended" else arkit_mapping_standard)
    shape_keys = obj.data.shape_keys.key_blocks
    converted = 0
    for arkit_name, cc4_name in mapping.items():
        for sk in shape_keys:
            if sk.name == cc4_name:
                sk.name = arkit_name
                converted += 1
                break
    print(f"Converted {converted} shape key(s).")
    obj[CONVERSION_PROP] = True
    return {'FINISHED'}

def revert_arkit_to_cc4():
    obj = bpy.context.scene.cc4_arkit_settings.base_mesh
    if not (obj and obj.type == 'MESH' and obj.data.shape_keys):
        return {'CANCELLED'}
    shape_keys = obj.data.shape_keys.key_blocks

    # Handle the Jaw key specifically:
    if "JawOpen" in shape_keys:
        has_driver = False
        if obj.data.shape_keys.animation_data:
            for d in obj.data.shape_keys.animation_data.drivers:
                if d.data_path == 'key_blocks["JawOpen"].value':
                    has_driver = True
                    break
        if has_driver:
            if obj.get("original_jaw_open", False):
                shape_keys["JawOpen"].name = "Jaw_Open"
                print("Renamed JawOpen back to Jaw_Open (original existed).")
                del obj["original_jaw_open"]
            else:
                idx = shape_keys.find("JawOpen")
                if idx != -1:
                    obj.active_shape_key_index = idx
                    bpy.ops.object.shape_key_remove()
                    print("Removed converted JawOpen shape key.")
        else:
            shape_keys["JawOpen"].name = "Jaw_Open"
            print("Renamed JawOpen back to Jaw_Open (no driver found).")
    
    expr_type = detect_expression_type(obj)
    mapping = (arkit_mapping_extended if expr_type == "Extended" else arkit_mapping_standard)
    reverted = 0
    for sk in shape_keys:
        if sk.name in ("Jaw_Open", "JawOpen"):
            continue
        if sk.name in mapping:
            sk.name = mapping[sk.name]
            reverted += 1
    print(f"Reverted {reverted} shape key(s).")
    if CONVERSION_PROP in obj:
        del obj[CONVERSION_PROP]
    if "original_jaw_open" in obj:
        del obj["original_jaw_open"]

    # --- Separate Teeth and Tongue using Vertex Groups and rename them ---
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    if "VG_Teeth" in obj.vertex_groups:
        bpy.ops.mesh.select_all(action='DESELECT')
        obj.vertex_groups.active = obj.vertex_groups["VG_Teeth"]
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        separated_obj = bpy.context.active_object
        separated_obj.name = "CC_Base_Teeth"
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    if "VG_Tongue" in obj.vertex_groups:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='DESELECT')
        obj.vertex_groups.active = obj.vertex_groups["VG_Tongue"]
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        separated_obj = bpy.context.active_object
        separated_obj.name = "CC_Base_Tongue"
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return {'FINISHED'}

def detect_expression_type(obj):
    if not (obj and obj.data.shape_keys):
        return None
    shape_keys = obj.data.shape_keys.key_blocks
    standard_matches = sum(1 for sk in shape_keys if sk.name in arkit_mapping_standard.values())
    extended_matches = sum(1 for sk in shape_keys if sk.name in arkit_mapping_extended.values())
    if extended_matches > standard_matches:
        return "Extended"
    elif standard_matches > 0:
        return "Standard"
    return None

def perform_jaw_open(settings):
    body_obj = settings.base_mesh
    arm_obj = settings.armature_obj
    if not (body_obj and arm_obj):
        raise Exception("Base Mesh or Armature not set.")
    
    # --- Create Vertex Groups for Teeth and Tongue if present ---
    teeth_obj = bpy.data.objects.get("CC_Base_Teeth")
    tongue_obj = bpy.data.objects.get("CC_Base_Tongue")
    if teeth_obj:
        vg = teeth_obj.vertex_groups.get("VG_Teeth")
        if vg is None:
            vg = teeth_obj.vertex_groups.new(name="VG_Teeth")
        vg.add(range(len(teeth_obj.data.vertices)), 1.0, 'REPLACE')
    if tongue_obj:
        vg = tongue_obj.vertex_groups.get("VG_Tongue")
        if vg is None:
            vg = tongue_obj.vertex_groups.new(name="VG_Tongue")
        vg.add(range(len(tongue_obj.data.vertices)), 1.0, 'REPLACE')
    
    # If teeth or tongue exist, join them with base mesh.
    if teeth_obj or tongue_obj:
        bpy.ops.object.select_all(action='DESELECT')
        body_obj.select_set(True)
        if teeth_obj:
            teeth_obj.select_set(True)
        if tongue_obj:
            tongue_obj.select_set(True)
        bpy.context.view_layer.objects.active = body_obj
        bpy.ops.object.join()
        print("Joined Teeth and/or Tongue into Base Mesh.")
        settings.base_mesh = bpy.context.view_layer.objects.active

    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    jaw_root = arm_obj.pose.bones.get(settings.jaw_bone)
    if jaw_root is None:
        raise Exception(f"Bone '{settings.jaw_bone}' not found in the armature.")
    orig_rot = jaw_root.rotation_euler.copy()
    jaw_root["orig_rot"] = orig_rot.copy()
    jaw_root.rotation_mode = 'XYZ'
    jaw_root.rotation_euler = (orig_rot[0], orig_rot[1], math.radians(20))
    bpy.context.view_layer.update()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = body_obj.evaluated_get(depsgraph)
    mesh_data = mesh_eval.to_mesh()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = body_obj
    if not body_obj.data.shape_keys:
        body_obj.shape_key_add(name="Basis", from_mix=False)
    if "Jaw_Open" in body_obj.data.shape_keys.key_blocks:
        body_obj["original_jaw_open"] = True
        idx = body_obj.data.shape_keys.key_blocks.find("Jaw_Open")
        if idx != -1:
            body_obj.active_shape_key_index = idx
            bpy.ops.object.shape_key_remove()
            print("Removed original Jaw_Open shape key.")
    if "JawOpen" in body_obj.data.shape_keys.key_blocks:
        print("JawOpen shape key already exists; skipping creation.")
        jaw_root.rotation_euler = jaw_root["orig_rot"]
        del jaw_root["orig_rot"]
        bpy.context.view_layer.update()
        return body_obj, arm_obj
    jaw_key = body_obj.shape_key_add(name="JawOpen", from_mix=False)
    if len(body_obj.data.vertices) != len(mesh_data.vertices):
        raise Exception("Vertex count mismatch in Base Mesh!")
    for i, v in enumerate(mesh_data.vertices):
        jaw_key.data[i].co = v.co
    body_obj.to_mesh_clear()

    jaw_root.rotation_euler = jaw_root["orig_rot"]
    del jaw_root["orig_rot"]
    bpy.context.view_layer.update()

    if "jaw_ctrl" not in jaw_root:
        jaw_root["jaw_ctrl"] = 0.0
    driver = jaw_key.driver_add("value").driver
    driver.expression = "jaw_ctrl"
    var = driver.variables.new()
    var.name = "jaw_ctrl"
    var.type = 'SINGLE_PROP'
    var.targets[0].id = arm_obj
    var.targets[0].data_path = f'pose.bones["{settings.jaw_bone}"]["jaw_ctrl"]'
    print("JawOpen shape key created and driven by 'jaw_ctrl' on", settings.jaw_bone)
    return body_obj, arm_obj

# --- Operator: Convert ---
class OBJECT_OT_convert_cc4_to_arkit(bpy.types.Operator):
    bl_idname = "object.convert_cc4_to_arkit"
    bl_label = "Convert CC4 to ARKit"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        settings = context.scene.cc4_arkit_settings
        if not (settings.armature_obj and settings.base_mesh and settings.jaw_bone):
            return False
        obj = settings.base_mesh
        if not (obj and obj.type == 'MESH' and obj.data.shape_keys):
            return False
        if obj.get(CONVERSION_PROP, False):
            return False
        if "Jaw_Open" in obj.data.shape_keys.key_blocks:
            return False
        if "JawOpen" in obj.data.shape_keys.key_blocks:
            if obj.data.shape_keys.animation_data:
                for d in obj.data.shape_keys.animation_data.drivers:
                    if d.data_path == 'key_blocks["JawOpen"].value':
                        return False
        return needs_conversion(obj)

    def execute(self, context):
        settings = context.scene.cc4_arkit_settings
        if not (settings.armature_obj and settings.base_mesh and settings.jaw_bone):
            self.report({'ERROR'}, "Please select Armature, Base Mesh, and Jaw Bone.")
            return {'CANCELLED'}
        try:
            body_obj, arm_obj = perform_jaw_open(settings)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        bpy.context.view_layer.objects.active = body_obj
        convert_cc4_to_arkit()
        body_obj[CONVERSION_PROP] = True
        bpy.ops.object.select_all(action='DESELECT')
        self.report({'INFO'}, "Conversion complete. All objects deselected.")
        return {'FINISHED'}

# --- Operator: Revert (Disabled) ---
class OBJECT_OT_revert_arkit_to_cc4(bpy.types.Operator):
    bl_idname = "object.revert_arkit_to_cc4"
    bl_label = "Revert ARKit to CC4"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Disable revert by always returning False.
        return False

    def execute(self, context):
        result = revert_arkit_to_cc4()
        if result == {'CANCELLED'}:
            self.report({'INFO'}, "No ARKit shape keys found to revert.")
            return {'CANCELLED'}
        self.report({'INFO'}, "Revert complete. Mesh is now eligible for conversion.")
        return {'FINISHED'}

# --- UI Panel ---
class VIEW3D_PT_cc4_to_arkit_panel(bpy.types.Panel):
    bl_label = "CC4 ARKit Renamer"
    bl_idname = "VIEW3D_PT_cc4_to_arkit_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CC4 ARKit"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.cc4_arkit_settings

        layout.prop(settings, "armature_obj")
        layout.prop(settings, "base_mesh")
        layout.prop(settings, "jaw_bone")

        missing = []
        if not settings.armature_obj:
            missing.append("Armature")
        if not settings.base_mesh:
            missing.append("Base Mesh")
        if not settings.jaw_bone:
            missing.append("Jaw Bone")
        if missing:
            layout.label(text="Missing: " + ", ".join(missing), icon='ERROR')
        else:
            obj = settings.base_mesh
            if needs_conversion(obj):
                layout.label(text="Valid mesh selected (needs conversion)", icon='CHECKMARK')
            else:
                layout.label(text="Invalid Mesh", icon='INFO')

        layout.separator()
        layout.operator("object.convert_cc4_to_arkit", icon='SHAPEKEY_DATA', text="Convert CC4 to ARKit")
        layout.separator()
        # The revert button is disabled (hidden) by its poll method.
        layout.operator("object.revert_arkit_to_cc4", icon='LOOP_BACK', text="Revert ARKit to CC4 (Disabled)")

classes = (
    CC4_ARKit_Settings,
    OBJECT_OT_convert_cc4_to_arkit,
    OBJECT_OT_revert_arkit_to_cc4,
    VIEW3D_PT_cc4_to_arkit_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cc4_arkit_settings = bpy.props.PointerProperty(type=CC4_ARKit_Settings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cc4_arkit_settings

if __name__ == "__main__":
    register()
