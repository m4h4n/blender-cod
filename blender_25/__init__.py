"""
(c) 2011 by CoDEmanX

Version: alpha 3


TODO

- Enable 'Selection only' when implemented (alpha 3)
- UI for xmodel and xanim import (planned for alpha 4/5)

"""

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>


bl_info = {
    "name": "CoD model/anim addon (alpha 3)",
    "author": "CoDEmanX, Flybynyt",
    "version": (0, 2, 3),
    "blender": (2, 59, 0),
    "api": 39307,
    "location": "File > Import / File > Export",
    "description": "Export models to *.XMODEL_EXPORT and animations to *.XANIM_EXPORT for Call of Duty� modding",
    "warning": "Alpha version, please report errors and bugs!",
    "wiki_url": "http://code.google.com/p/blender-cod/",
    "tracker_url": "http://code.google.com/p/blender-cod/issues/list",
    "support": "COMMUNITY",
    "category": "Import-Export"
    }


# To support reload properly, try to access a package var, if it's there, reload everything
if "bpy" in locals():
    import imp
    if "import_xmodel" in locals():
        imp.reload(import_xmodel)
    if "export_xmodel" in locals():
        imp.reload(export_xmodel)
    if "import_xanim" in locals():
        imp.reload(import_xanim)
    if "export_xanim" in locals():
        imp.reload(export_xanim)


import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty
import bpy_extras.io_utils
from bpy_extras.io_utils import ExportHelper, ImportHelper
import time

""" Planned for alpha 4/5
class ImportXmodel(bpy.types.Operator, ImportHelper):
    '''Load a CoD XMODEL_EXPORT File'''
    bl_idname = "import_scene.xmodel"
    bl_label = "Import XMODEL_EXPORT"
    bl_options = {'PRESET'}

    filename_ext = ".XMODEL_EXPORT"
    filter_glob = StringProperty(default="*.XMODEL_EXPORT", options={'HIDDEN'})

    use_meshes = BoolProperty(name="Meshes", description="Import meshes", default=True)
    use_armature = BoolProperty(name="Armature", description="Import Armature", default=True)
    use_bind_armature = BoolProperty(name="Bind Meshes to Armature", description="Parent imported meshes to armature", default=True)

    #use_split_objects = BoolProperty(name="Object", description="Import OBJ Objects into Blender Objects", default=True)
    #use_split_groups = BoolProperty(name="Group", description="Import OBJ Groups into Blender Objects", default=True)

    #use_image_search = BoolProperty(name="Image Search", description="Search subdirs for any assosiated images (Warning, may be slow)", default=True)

    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import import_xmodel
        
        return import_xmodel.load(self, context, **self.as_keywords(ignore=("filter_glob",)))

    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.prop(self, "use_meshes")
        col.prop(self, "use_armature")
        
        row = layout.row()
        row.active = self.use_meshes and self.use_armature
        row.prop(self, "use_bind_armature")


class ImportXanim(bpy.types.Operator, ImportHelper):
    '''Load a CoD XANIM_EXPORT File'''
    bl_idname = "import_scene.xanim"
    bl_label = "Import XANIM_EXPORT"
    bl_options = {'PRESET'}

    filename_ext = ".XANIM_EXPORT"
    filter_glob = StringProperty(default="*.XANIM_EXPORT", options={'HIDDEN'})
    
    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import import_xanim

        return import_xanim.load(self, context, **self.as_keywords(ignore=("filter_glob",)))
"""

class ExportXmodel(bpy.types.Operator, ExportHelper):
    '''Save a CoD XMODEL_EXPORT File'''

    bl_idname = "export_scene.xmodel"
    bl_label = 'Export XMODEL_EXPORT'
    bl_options = {'PRESET'}

    filename_ext = ".XMODEL_EXPORT"
    filter_glob = StringProperty(default="*.XMODEL_EXPORT", options={'HIDDEN'})

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    
    use_version = EnumProperty(
        name="Format Version",
        description="XMODEL_EXPORT format version for export",
        items=(('5', "Version 5", "vCoD, CoD:UO"),
               ('6', "Version 6", "CoD2, CoD4, CoD5, CoD7")),
        default='6',
        )

    use_selection = BoolProperty(
        name="Selection Only",
        description="Export selected objects only",
        default=False
        )
        
    use_vertex_colors = BoolProperty(
        name="Vertex colors",
        description="Export vertex colors (if disabled, white color will be used)",
        default=True
        )
        
    use_apply_modifiers = BoolProperty(
        name="Apply Modifiers",
        description="Apply all mesh modifiers except Armature (preview resolution)",
        default=True
        )
        
    use_armature = BoolProperty(
        name="Armature",
        description="Export bones (if disabled, only a 'tag_origin' bone will be written)",
        default=True
        )
        
    use_armature_pose = BoolProperty(
        name="Pose animation",
        description="Export meshes with Armature modifier applied as a series of XMODEL_EXPORT files",
        default=False
        )
        
    use_frame_start = IntProperty(
        name="Start",
        description="First frame to export",
        default=1,
        min=0
        )
        
    use_frame_end = IntProperty(
        name="End",
        description="Last frame to export",
        default=250,
        min=0
        )

    
    # Not implemented
    use_create_gdt = BoolProperty(name="Create GDT", description="Create game data file for Asset Manager", default=False)


    def execute(self, context):
        from . import export_xmodel
        start_time = time.clock()
        result = export_xmodel.save(self, context, **self.as_keywords(ignore=("filter_glob", "check_existing")))
        
        if not result:
            self.report({'INFO'}, "Export finished in %.4f sec." % (time.clock() - start_time))
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, result)
            return {'CANCELLED'}


    # Extend ExportHelper invoke function to support dynamic default values
    def invoke(self, context, event):
        
        self.use_frame_start = context.scene.frame_start
        self.use_frame_end = context.scene.frame_end
        
        return super(ExportXmodel, self).invoke(context, event)


    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=True)
        row.prop(self, "use_version", expand=True)

        col = layout.column(align=True)
        col.prop(self, "use_selection")
        col.enabled = False
        
        col = layout.column(align=True)
        col.active = self.use_version == '6'
        col.prop(self, "use_vertex_colors")
        
        col = layout.column(align=True)
        col.prop(self, "use_apply_modifiers")
        
        col = layout.column(align=True)
        col.prop(self, "use_armature")
        
        box = layout.box()
        
        col = box.column(align=True)
        col.prop(self, "use_armature_pose")
        
        sub = box.column()
        #sub.active = self.use_armature_pose
        sub.enabled = False
        
        sub.label(text="Frame range: (%i frames)" % (abs(self.use_frame_end - self.use_frame_start) + 1))
        
        row = sub.row(align=True)
        row.prop(self, "use_frame_start")
        row.prop(self, "use_frame_end")
        
        
    @classmethod
    def poll(self, context):
        return (context.scene is not None)


class ExportXanim(bpy.types.Operator, ExportHelper):
    '''Save a XMODEL_XANIM File'''

    bl_idname = "export_scene.xanim"
    bl_label = 'Export XANIM_EXPORT'
    bl_options = {'PRESET'}

    filename_ext = ".XANIM_EXPORT"
    filter_glob = StringProperty(default="*.XANIM_EXPORT", options={'HIDDEN'})
    
    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    use_selection = BoolProperty(
        name="Selection Only",
        description="Export selected bones only",
        default=False
        )
    
    use_framerate = IntProperty(
        name="Framerate",
        description="Set FPS for export",
        default=24,
        min=1,
        max=100
        )
        
    use_frame_start = IntProperty(
        name="Start",
        description="First frame to export",
        default=1,
        min=0
        )
        
    use_frame_end = IntProperty(
        name="End",
        description="Last frame to export",
        default=250,
        min=0
        )
        
    use_notetracks = BoolProperty(
        name="Notetracks",
        description="Export markers as notetracks",
        default=True
        )

    use_notetrack_format = EnumProperty(
        name="Notetrack format",
        description="Always set 'CoD 7' for Black Ops even if there is no notetrack!",
        items=(('5', "CoD 5", "Separate NT_EXPORT notetrack file for 'World at War'"),
               ('7', "CoD 7", "Separate NT_EXPORT notetrack file for 'Black Ops'"),
               ('1', "all other", "Inline notetrack data for all CoD versions except WaW and BO")),
        default='1',
        )

    def execute(self, context):
        from . import export_xanim
        start_time = time.clock()
        result = export_xanim.save(self, context, **self.as_keywords(ignore=("filter_glob", "check_existing")))
        
        if not result:
            self.report({'INFO'}, "Export finished in %.4f sec." % (time.clock() - start_time))
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, result)
            return {'CANCELLED'}


    # Extend ExportHelper invoke function to support dynamic default values
    def invoke(self, context, event):
        
        self.use_frame_start = context.scene.frame_start
        self.use_frame_end = context.scene.frame_end
        self.use_framerate = round(context.scene.render.fps / context.scene.render.fps_base)
        
        # TODO: marker count / applicable markers?
        
        return super(ExportXanim, self).invoke(context, event)


    def draw(self, context):
        
        layout = self.layout
        
        # TODO: Either add a bone list with checkboxes or support selected_bones
        col = layout.column(align=True)
        col.prop(self, "use_selection")
        col.enabled = False
        
        layout.label(text="Frame range: (%i frames)" % (abs(self.use_frame_end - self.use_frame_start) + 1))
        
        row = layout.row(align=True)
        row.prop(self, "use_frame_start")
        row.prop(self, "use_frame_end")
        
        col = layout.column(align=True)
        col.prop(self, "use_framerate")
        
        # TODO: show markers in export range only?
        #layout.label("Notetracks (%i):" % len(context.scene.timeline_markers))
        col = layout.column(align=True)
        col.prop(self, "use_notetracks", text="Notetracks (%i)" % len(context.scene.timeline_markers))

        col = layout.column(align=True)
        col.prop(self, "use_notetrack_format", expand=True)
        
        
    @classmethod
    def poll(self, context):
        return (context.scene is not None)

"""
def menu_func_xmodel_import(self, context):
    self.layout.operator(ImportXmodel.bl_idname, text="CoD Xmodel (.XMODEL_EXPORT)")

def menu_func_xanim_import(self, context):
    self.layout.operator(ImportXanim.bl_idname, text="CoD Xanim (.XANIM_EXPORT)")
"""

def menu_func_xmodel_export(self, context):
    self.layout.operator(ExportXmodel.bl_idname, text="CoD Xmodel (.XMODEL_EXPORT)")
    
def menu_func_xanim_export(self, context):
    self.layout.operator(ExportXanim.bl_idname, text="CoD Xanim (.XANIM_EXPORT)")



def register():
    bpy.utils.register_module(__name__)

    #bpy.types.INFO_MT_file_import.append(menu_func_xmodel_import)
    #bpy.types.INFO_MT_file_import.append(menu_func_xanim_import)
    bpy.types.INFO_MT_file_export.append(menu_func_xmodel_export)
    bpy.types.INFO_MT_file_export.append(menu_func_xanim_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    #bpy.types.INFO_MT_file_import.remove(menu_func_xmodel_import)
    #bpy.types.INFO_MT_file_import.remove(menu_func_xanim_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_xmodel_export)
    bpy.types.INFO_MT_file_export.remove(menu_func_xanim_export)


if __name__ == "__main__":
    register()