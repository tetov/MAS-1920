import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

import random as r

# enable/disable redraw
rs.EnableRedraw(False)

# add pt with rs
rs.AddPoint((0,0,0))

# add multiple pts
pts = []
for i in range(10):
    for j in range(10):
        for k in range(10):
            pts.append(rs.AddPoint((i,j,k)))

for i,pt in enumerate(pts):
    rs.MoveObject(pt, [1,5,8])
    radius = r.uniform(.2,0.8)
    rs.AddSphere(pt,radius)



rs.AddPolyline(pts)
rs.AddCurve(pts)

rs.EnableRedraw(True)