bl_info = {
    "name": "Auto Outline Object",
    "blender": (4, 3, 2),
    "category": "Object",
    "author": "Michal Uchwat",
    "email": "uchwatmichal@gmail.com",
    "version": (1, 0, 0),
    "description": "Automatically resets scale, removes any existing materials assigned to an object, adds a solidify modifier, and assigns materials.",
    "location": "View3D > Sidebar > Tools",
    "warning": "",
    "support": "COMMUNITY",
}

import bpy

class AutoOutlineSetupProperties(bpy.types.PropertyGroup):
    solidify_thickness: bpy.props.FloatProperty(
        name="Outline Thickness",
        default=0.5,
        min=0.0,
        description="Solidify thickness"
    )
    flip_normals: bpy.props.BoolProperty(
        name="Flip Normals",
        default=True,
        description="Flip normals of the solidify modifier"
    )
    material_offset: bpy.props.IntProperty(
        name="Material Offset",
        default=1,
        description="Material offset for the solidify modifier"
    )
    fill_color: bpy.props.FloatVectorProperty(
        name="Fill Color",
        subtype="COLOR",
        size=4,
        default=(0.188, 0.188, 0.188, 1),  # Hex 303030FF dark grey
        description="Color for the fill material"
    )
    outline_color: bpy.props.FloatVectorProperty(
        name="Outline Color",
        subtype="COLOR",
        size=4,
        default=(1, 1, 1, 1),  # Hex FFFFFF white
        description="Color for the outline material"
    )
    backface_culling: bpy.props.BoolProperty(
        name="Backface Culling Outline Color",
        default=True,
        description="Enable backface culling for the outline material"
    )
    
def reset_scale(obj):
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

def add_solidify_modifier(obj, props):
    mod = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
    mod.thickness = props.solidify_thickness
    mod.use_flip_normals = props.flip_normals
    mod.material_offset = props.material_offset
    mod.use_rim = False

def remove_existing_materials(obj):
    obj.data.materials.clear()

def add_materials(obj, props):
    # Create _fill-in_dark material
    material_fill = bpy.data.materials.get("_fill-in_dark")
    if not material_fill:
        material_fill = bpy.data.materials.new(name="_fill-in_dark")
        material_fill.use_nodes = True
        bsdf = material_fill.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs[0].default_value = props.fill_color

   # Create _outline_white material
    material_outline = bpy.data.materials.get("_outline_white")
    if not material_outline:
        material_outline = bpy.data.materials.new(name="_outline_white")
    material_outline.use_nodes = True
    material_outline.node_tree.nodes.clear()
    node_emission = material_outline.node_tree.nodes.new(type="ShaderNodeEmission")
    node_output = material_outline.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    material_outline.node_tree.links.new(node_emission.outputs[0], node_output.inputs[0])
    node_emission.inputs[0].default_value = props.outline_color

    # Enable backface culling for the outline material
    material_outline.use_backface_culling = props.backface_culling

    # Assign materials to the object
    if material_fill and material_fill.name not in obj.data.materials:
        obj.data.materials.append(material_fill)
    if material_outline and material_outline.name not in obj.data.materials:
        obj.data.materials.append(material_outline)

def process_selected_objects(props):
    for obj in bpy.context.selected_objects:
        if obj.type == "MESH":
            reset_scale(obj)
            remove_existing_materials(obj)
            add_solidify_modifier(obj, props)
            add_materials(obj, props)

class OBJECT_OT_AutoOutlineSetup(bpy.types.Operator):
    """Auto Outline Setup with Scale Reset, Solidify Modifier, and Materials"""
    bl_idname = "object.auto_outline_setup"
    bl_label = "Auto Outliner"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.auto_outline_setup_props
        process_selected_objects(props)
        return {"FINISHED"}

class VIEW3D_PT_AutoOutlineSetupPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Auto Outliner"
    bl_idname = "VIEW3D_PT_auto_outline_setup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Auto Outliner"

    def draw(self, context):
        layout = self.layout
        props = context.scene.auto_outline_setup_props
        layout.prop(props, "solidify_thickness")
        layout.prop(props, "flip_normals")
        layout.prop(props, "material_offset")
        layout.prop(props, "fill_color")
        layout.prop(props, "outline_color")
        layout.prop(props, "backface_culling")
        layout.operator("object.auto_outline_setup")

def register():
    bpy.utils.register_class(AutoOutlineSetupProperties)
    bpy.types.Scene.auto_outline_setup_props = bpy.props.PointerProperty(type=AutoOutlineSetupProperties)
    bpy.utils.register_class(OBJECT_OT_AutoOutlineSetup)
    bpy.utils.register_class(VIEW3D_PT_AutoOutlineSetupPanel)

def unregister():
    bpy.utils.unregister_class(AutoOutlineSetupProperties)
    del bpy.types.Scene.auto_outline_setup_props
    bpy.utils.unregister_class(OBJECT_OT_AutoOutlineSetup)
    bpy.utils.unregister_class(VIEW3D_PT_AutoOutlineSetupPanel)

if __name__ == "__main__":
    register()
