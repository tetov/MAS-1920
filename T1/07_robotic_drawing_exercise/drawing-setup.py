import sys
#sys.path.append('C:\\Users\\a\\repos\\MAS-1920\\T1\\07_robotic_drawing_exercise\\robotic_drawing')

import robotic_drawing.robotic_drawing as rd


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

plane_1 = rg.Plane(rg.Point3d(400.0,20.0,100),rg.Vector3d.ZAxis)
plane_2 = rg.Plane(rg.Point3d(400.0,277,100),rg.Vector3d.ZAxis)
plane_3 = rg.Plane(rg.Point3d(20,277,100),rg.Vector3d.ZAxis)

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
