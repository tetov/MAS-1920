import sys
sys.path.append('C:/Users/jennyd/Desktop/DAVIDJENNY/robotic_drawing')

import robotic_drawing as rd
rd.ROBOT_IP = '192.168.10.10'

import simple_ur_script as ur
import simple_comm as c

import Rhino.Geometry as rg
import math as m

execute = True

#move_to = rg.Point3d(300.0,60.0,300.0)
#rd.move_robot_vertical(move_to)

#rd.set_robot_base_plane()

robot_base = rd.load_robot_base_plane()


zero_plane = rg.Plane(rg.Point3d(20,20,.3),rg.Vector3d.ZAxis)

plane_1 = rg.Plane(rg.Point3d(400.0,20.0,.3),rg.Vector3d.ZAxis)
plane_2 = rg.Plane(rg.Point3d(400.0,277,.3),rg.Vector3d.ZAxis)
plane_3 = rg.Plane(rg.Point3d(20,277,.3),rg.Vector3d.ZAxis)

way_planes = [zero_plane,plane_1,plane_2,plane_3]
robo_planes = []

for way_plane in way_planes:
    robo_plane = rd.rhino_to_robot_space(way_plane,robot_base)
    robo_planes.append(robo_plane)


robo_planes *= 10

accel = 0.05
vel = 0.1

script = ''
for robo_plane in robo_planes:
    script += ur.move_l(robo_plane, accel, vel)

if execute:
    script = c.concatenate_script(script)
    c.send_script(script, rd.ROBOT_IP)
else:
    script = c.concatenate_script(script)
    print script


#import random as r
#way_planes = []
#for i in range(100):
#    x = r.randint(50,370)
#    y = r.randint(50,247)
#    way_plane = rg.Plane(rg.Point3d(x,y,0.1),rg.Vector3d.ZAxis)
#    way_planes.append(way_plane)
#    way_plane = rg.Plane(rg.Point3d(x,y,100),rg.Vector3d.ZAxis)
#    way_planes.append(way_plane)



























#

#



#home_pose = [0.0,-90.0,0.0,-90.0,0.0,0.0]
#home_pose = [m.radians(n) for n in home_pose]
#script = ur.move_j(home_pose,0.02,0.1)
#c.send_script(script, rd.ROBOT_IP)