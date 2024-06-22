bl_info = {
    "name": "BgView",
    "description":  "A blender Add-on to visualize the parallax effect for New Super Mario Bros. 2 background models.",
    "author": "hus_mighty",
    "blender": (3, 4, 1),
    "version": (1, 1, 0),
    "category": "Object"
}

import bpy 


def resetCam():
    scene = bpy.context.scene
    scene.objects["PreviewCam_Controller"].location.z = 0
    scene.objects["PreviewCam_Controller"].location.y = -200
    scene.objects["PreviewCam_Controller"].location.x = 0
    
def createScene():
    scene = bpy.context.scene
    #camera
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(160, -170, 96), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
    scene.render.resolution_x = 400
    scene.render.resolution_y = 240
    bpy.context.object.data.ortho_scale = 320
    bpy.context.object.data.clip_end = 2000
    bpy.context.object.data.type = 'ORTHO'
    bgcam = scene.objects["Camera"]
    bgcam.name = "Preview_Cam"
    


    #empty
    bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=(0, -200, 0), scale=(1, 1, 1))
    camcontrol = scene.objects["Empty"]
    camcontrol.name = "PreviewCam_Controller"
    camcontrol.lock_location[1] = True


    #screen reference
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(160, 1200, 96), scale=(1, 1, 1), rotation=(1.5708, 0, 0))
    screenref = scene.objects["Plane"]
    screenref.name = "ScreenSize_Reference"
    screenref.dimensions = (320, 192, 0)

    #parenting
    bpy.ops.object.select_all(action='DESELECT')
    screenref.select_set(True)
    bgcam.select_set(True)
    camcontrol.select_set(True)

    bpy.context.view_layer.objects.active = camcontrol #parent
    bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=False)
    bgcam.hide_select = True




def createParallax():
    scene = bpy.context.scene
    for x in bpy.data.objects:
        if(x.name[0:6] == "joint_"):
            parallax = scene.objects[x.name].location[1]
            if (not x.constraints):
                
                #x axis
                constraintx = scene.objects[x.name].constraints.new(type='COPY_LOCATION')
                constraintx.name = "xpos"
                constraintx.use_y = False
                constraintx.use_z = False
                constraintx.influence = -0.0005 * parallax + 0.5
                constraintx.target = scene.objects["PreviewCam_Controller"]
                
                #y axis
                constrainty = scene.objects[x.name].constraints.new(type='COPY_LOCATION')
                constrainty.name = "ypos"
                constrainty.use_x = False
                constrainty.use_y = False
                constrainty.influence = 0.0007 * parallax + 0.7
                constrainty.target = scene.objects["PreviewCam_Controller"]


def updateParallax():
    scene = bpy.context.scene
    for x in bpy.data.objects:
        parallax = scene.objects[x.name].location[1]
        if(x.name[0:6] == "joint_" and x.constraints):
            x.constraints[0].influence = 0.0005 * parallax + 0.5
            x.constraints[1].influence = 0.0003 * parallax + 0.7
            x.constraints[0].target = scene.objects["PreviewCam_Controller"]
            x.constraints[1].target = scene.objects["PreviewCam_Controller"]
            
def noparallax():
    scene = bpy.context.scene
    for x in bpy.data.objects:
        parallax = scene.objects[x.name].location[1]
        if(x.name[0:6] == "joint_" and x.constraints):
            x.constraints[0].influence = 0
            x.constraints[1].influence = 0
            x.constraints[0].target = scene.objects["PreviewCam_Controller"]
            x.constraints[1].target = scene.objects["PreviewCam_Controller"]
            
def noxparallax():
    scene = bpy.context.scene
    for x in bpy.data.objects:
        parallax = scene.objects[x.name].location[1]
        if(x.name[0:6] == "joint_" and x.constraints):
            x.constraints[0].influence = 0
            x.constraints[0].target = scene.objects["PreviewCam_Controller"]

            
def noyparallax():
    scene = bpy.context.scene
    for x in bpy.data.objects:
        parallax = scene.objects[x.name].location[1]
        if(x.name[0:6] == "joint_" and x.constraints):
            x.constraints[1].influence = 0
            x.constraints[1].target = scene.objects["PreviewCam_Controller"]


class mainpanel(bpy.types.Panel):
    bl_label = "BgView"
    bl_idname = "bgtool_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NSMB2Hax"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        obj = context.object
        row = layout.row()
        
        
        row = layout.row()
        row.operator("bgtool.createscene")
        row = layout.row()
        row.operator("bgtool.createparallax")
        row = layout.row()
        row.operator("bgtool.resetcampos")
        row = layout.row()
        row.operator("bgtool.updateparallax")
        row = layout.row()
        row.operator("bgtool.noparallax")
        row = layout.row()
        row.operator("bgtool.noxparallax")
        row = layout.row()
        row.operator("bgtool.noyparallax")


    
#button operators
class createscene(bpy.types.Operator):
    bl_label = "Create Scene"
    bl_idname = "bgtool.createscene"
        
    def execute(self,context):
        createScene()
        return {"FINISHED"}


class createparallax(bpy.types.Operator):
    bl_label = "Create Parallax"
    bl_idname = "bgtool.createparallax"

    def execute(self,context):
        createParallax()
        return {"FINISHED"}
    

class updateparallax(bpy.types.Operator):
    bl_label = "Update Parallax Values"
    bl_idname = "bgtool.updateparallax"

    def execute(self,context):    
        updateParallax()
        return {"FINISHED"}
    
class resetcampos(bpy.types.Operator):
    bl_label = "Reset Camera"
    bl_idname = "bgtool.resetcampos"

    def execute(self,context):    
        resetCam()
        return {"FINISHED"}

class noparallax(bpy.types.Operator):
    bl_label = "All Parallax Off"
    bl_idname = "bgtool.noparallax"

    def execute(self,context):    
        noparallax()
        return {"FINISHED"}
    
class noXparallax(bpy.types.Operator):
    bl_label = "X Parallax Off"
    bl_idname = "bgtool.noxparallax"

    def execute(self,context):    
        noxparallax()
        return {"FINISHED"}
    
class noYparallax(bpy.types.Operator):
    bl_label = "Y Parallax Off"
    bl_idname = "bgtool.noyparallax"

    def execute(self,context):    
        noyparallax()
        return {"FINISHED"}
    

classes = [mainpanel, createscene, createparallax, updateparallax, resetcampos, noparallax, noXparallax, noYparallax]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.mytool


if __name__ == "__main__":
    register()
