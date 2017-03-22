import sys
import time
import openvr

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
    return v
        

openvr.init(openvr.VRApplication_Scene)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()

openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
yaw1 = (poses[0].mDeviceToAbsoluteTracking)[2][0]
yaw2 = (poses[0].mDeviceToAbsoluteTracking)[2][2]
offset = GetYawValue(yaw1, yaw2)

while True:
    openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    #print(hmd_pose.mDeviceToAbsoluteTracking)
    #print((poses[0].mDeviceToAbsoluteTracking)[2][0])
    #print((poses[0].mDeviceToAbsoluteTracking)[2][2])
    #print('###################')
    yaw1 = (poses[0].mDeviceToAbsoluteTracking)[2][0]
    yaw2 = (poses[0].mDeviceToAbsoluteTracking)[2][2]
    yaw_value = GetYawValue(yaw1,yaw2)
    print(yaw_value)
    print(GetOffsetYawValue(yaw_value, offset))
    print('')                               
    sys.stdout.flush()
    time.sleep(0.2)

openvr.shutdown()

'''
poses[0] = Headset
poses[1] = basestation??
poses[2] = ???
poses[3] = controller 1
poses[4] = controller 2

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
