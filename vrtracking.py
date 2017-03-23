import sys
import time
import openvr
import math

def GetYawValue(yaw1, yaw2):
    if (yaw1 >= 0 and yaw2 >= 0):
        return yaw1/2
    elif(yaw1 >= 0 and yaw2 < 0):
        return 1-(yaw1/2)
    elif(yaw1 < 0 and yaw2 < 0):
        return -0.5+(yaw2/2)
    elif(yaw1 < 0 and yaw2 >= 0):
        return -0.5+(yaw2/2)

def GetOffsetYawValue(value, offset):
    v = value-offset
    if v < -1:
        v = 2+v
    elif v > 1:
        v = v-2
    return round(v, 2)

def GetDistance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
    
        

openvr.init(openvr.VRApplication_Scene)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()



openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
yaw1 = (poses[0].mDeviceToAbsoluteTracking)[2][0]
yaw2 = (poses[0].mDeviceToAbsoluteTracking)[2][2]
offset = GetYawValue(yaw1, yaw2)
previous_view = offset

hmd_index = -1
left_controller_index = -1
right_controller_index = -1
for i in range(openvr.k_unMaxTrackedDeviceCount):
    device_class = openvr.VRSystem().getTrackedDeviceClass(0)
    if(device_class == openvr.TrackedDeviceClass_HMD):
        hmd_index = i
    #elif(device_class == openvr.TrackedDevic

print('hmd:', hmd_index)
        

while True:
    openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    headset_tracking = poses[0].mDeviceToAbsoluteTracking
    controller1_tracking = poses[3].mDeviceToAbsoluteTracking
    controller2_tracking = poses[2].mDeviceToAbsoluteTracking
    yaw1 = headset_tracking[2][0]
    yaw2 = headset_tracking[2][2]
    yaw_value = GetYawValue(yaw1,yaw2)
    #print(yaw_value)
    #print(GetOffsetYawValue(yaw_value, offset))

    current_view = GetOffsetYawValue(yaw_value, offset)

    diff = ((current_view) - (previous_view))
        
    if ((diff < 0.05) and (diff > -0.05)):
        #print('Nothing')
        a = 1
    else:
        #print('Changed')
        a=1
        if diff > 0.0:
            #print('Right')
            a=1
        else:
            #print('Left')
            a=1
        
        previous_view = current_view
    #print('')
    
    
    headset_x = headset_tracking[2][3]
    headset_y = headset_tracking[0][3]

    controller1_x = controller1_tracking[2][3]
    controller1_y = controller1_tracking[0][3]

    controller2_x = controller2_tracking[2][3]
    controller2_y = controller2_tracking[0][3]

    max_distance = 0.65
    distance1 = GetDistance(headset_x, headset_y, controller1_x, controller1_y)
    distance2 = GetDistance(headset_x, headset_y, controller2_x, controller2_y)

    if(distance1 > max_distance/2+0.05):
        print('left fwd')
    elif(distance1 < max_distance/2-0.05):
        print('left bckw')
    else:
        print('left stop')

    if(distance2 > max_distance/2+0.05):
        print('right fwd')
    elif(distance2 < max_distance/2-0.05):
        print('right bckw')
    else:
        print('right stop')

    event = openvr.VREvent_t()
    while(openvr.VRSystem().pollNextEvent(event)):
        t = event.eventType
        if (t == openvr.VREvent_ButtonPress and event.data.controller.button == openvr.k_EButton_SteamVR_Trigger):
            print(':D')
            #TODO
    
    sys.stdout.flush()
    time.sleep(0.2)

openvr.shutdown()

'''
poses[0] = Headset
poses[1] = basestation??
poses[2] = controller 2
poses[3] = controller 1
poses[4] = ???

[[?,   ?,   ?, Y],
 [?,   ?,   ?, Z],
 [Yaw1, ?,   Yaw2, X]]

 X = Langvegg-langvegg
 Y = Dør-vindu
 Z = Gulv - tak

 a = 0 mot kunstveggen, øker med klokka
 Yaw1 = sin a
 Yaw2 = cos a
'''
