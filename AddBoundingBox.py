bl_info = {
    "name": "Add Bounding Box From Selection",
    "author": "Class Outside",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "Object > Right-Click Context Menu",
    "description": "Adds a bounding box object based on the selection",
    "category": "Object",
}

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty
from mathutils import Vector, Matrix


def create_bounding_box():
    # Get the active object (the selected object)
    active_object = bpy.context.active_object
    
    # Apply scale to the object
    bpy.ops.object.transform_apply(scale=True)

    # Get the object's bounding box
    bounding_box = active_object.bound_box
    
    # Calculate the dimensions of the bounding box
    min_x, min_y, min_z = bounding_box[0]
    max_x, max_y, max_z = bounding_box[6]
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z

    # Create the bounding box cube
    bpy.ops.mesh.primitive_cube_add(size=1)
    bounding_cube = bpy.context.object

    # Scale the cube to match the dimensions of the object's bounding box
    bounding_cube.scale = Vector((width, height, depth))

    # Position the cube at the center of the object's bounding box
    bounding_cube.location = Vector(((max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2))
    
    # Set the name of the bounding box object based on width, height, and depth
    bounding_cube.name = f"{width:.2f}mW_{height:.2f}mH_{depth:.2f}mD"


class Add_Bounding_Box(Operator):
    bl_idname = "object.add_bounding_box"
    bl_label = "Add Bounding Box From Selection"
    bl_description = "Adds a bounding box object based on the selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        create_bounding_box()

        return {'FINISHED'}


def draw_func(self, context):
    layout = self.layout
    layout.operator(Add_Bounding_Box.bl_idname)


def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(Add_Bounding_Box.bl_idname)


def register():
    bpy.utils.register_class(Add_Bounding_Box)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(Add_Bounding_Box)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()
