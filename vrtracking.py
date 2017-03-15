import sys
import time
import openvr

openvr.init(openvr.VRApplication_Scene)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()

while True:
    openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    #print(hmd_pose.mDeviceToAbsoluteTracking)
    print(poses[3].mDeviceToAbsoluteTracking)
    sys.stdout.flush()
    time.sleep(0.2)

openvr.shutdown()

'''
poses[0] = Headset
poses[1] = basestation??
poses[2] = ???
poses[3] = controller 1
poses[4] = controller 2

[[?,   ?,   ?, X(?)],
 [?,   ?,   ?, Y(?)],
 [Yaw, ?,   ?, Z(?)]]
'''
