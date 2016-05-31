#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "EVERTims, real-time auralization framework",
    "author": "David Poirier-Quinot",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "3D View > Toolbox",
    "description": "A collection of tools to configure your EVERTims environment.",
    "warning": "",
    'tracker_url': "https://evertims.github.io/website/#contact",
    "wiki_url": "https://evertims.github.io/website",
    'support': 'COMMUNITY',
    "category": "Game Engine"
}

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
else:
    import bpy
    import os
    from bpy.props import (
            StringProperty,
            EnumProperty,
            BoolProperty,
            IntProperty,
            FloatProperty,
            PointerProperty
            )
    from bpy.types import (
            PropertyGroup
            )
    from . import (
            ui,
            operators
            )
import imp


ignore_change_props_list = (
    "rna_type", "screen_setup", "name", "bl_rna",
    "__dict__", "__doc__", "__module__", "__weakref__"
)

def update_evertims_props(self, context):
    scene = context.scene
    evertims = scene.evertims

    # get logic object
    obj = bpy.context.scene.objects.get('Logic_EVERTims')

    if obj:
        bpy.context.scene.objects.active = obj

        # sync. properties (for bge access) with GUI's
        for propName in dir(evertims):
            if not propName in ignore_change_props_list:
                propValue = eval('evertims.' + propName)
                obj.game.properties[propName].value = propValue




class EVERTimsSettings(PropertyGroup):

    enable_evertims = BoolProperty(
            name="Enable EVERTims",
            description='Activate EVERTims module in BGE',
            default=True,
            update=update_evertims_props
            )
    debug_rays = BoolProperty(
            name="Draw Rays",
            description='Enable visual feedback on EVERTims ratracing in BGE',
            default=False,
            update=update_evertims_props
            )
    debug_logs = BoolProperty(
            name="Print Logs",
            description='Print python logs in BGE console',
            default=False,
            update=update_evertims_props
            )
    ip_local = StringProperty(
            name="IP local",
            description="IP of the computer running Blender",
            default="127.0.0.1", maxlen=1024,
            update=update_evertims_props
            )
    ip_client = StringProperty(
            name="IP EVERTims client",
            description="IP of the computer running EVERTims",
            default="127.0.0.1", maxlen=1024,
            update=update_evertims_props
            )
    port_write = IntProperty(
            name="Port write",
            description="Port used by EVERTims client to read data sent by the BGE",
            default=3858,
            update=update_evertims_props
            )
    port_read = IntProperty(
            name="Port read",
            description="Port used by the BGE to read data sent by the EVERTims client",
            default=3862,
            update=update_evertims_props
            )
    movement_jnd = FloatProperty(
            name="Move JND",
            description="Minimum value a listener / source must move to be updated on EVERTims client",
            default=1.0,
            update=update_evertims_props
            )

# ############################################################
# Un/Registration
# ############################################################

def register():

    bpy.utils.register_class(EVERTimsSettings)

    ui.register()
    operators.register()

    bpy.types.Scene.evertims = PointerProperty(type=EVERTimsSettings)


def unregister():

    bpy.utils.unregister_class(EVERTimsSettings)

    ui.unregister()
    operators.unregister()

    del bpy.types.Scene.evertims