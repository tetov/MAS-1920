import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import math as m

class Brick:
    def __init__(self, center_plane, x_size = 200, y_size = 80, z_size = 70):
        self.cp = center_plane
        self.xs = x_size
        self.ys = y_size
        self.zs = z_size
    
    def distance_to_other_brick(self, other_brick):
        rs.AddLine(self.cp.Origin, other_brick.cp.Origin)
        return self.cp.Origin.DistanceTo(other_brick.cp.Origin)
    
    def display(self):
        pt_1 = self.cp.Origin - self.cp.XAxis * self.xs * 0.5 - self.cp.YAxis * self.ys * 0.5
        pt_2 = self.cp.Origin - self.cp.XAxis * self.xs * 0.5 + self.cp.YAxis * self.ys * 0.5
        pt_3 = self.cp.Origin + self.cp.XAxis * self.xs * 0.5 + self.cp.YAxis * self.ys * 0.5
        pt_4 = self.cp.Origin + self.cp.XAxis * self.xs * 0.5 - self.cp.YAxis * self.ys * 0.5
        pt_5 = self.cp.Origin - self.cp.XAxis * self.xs * 0.5 - self.cp.YAxis * self.ys * 0.5 + self.cp.ZAxis * self.zs
        pt_6 = self.cp.Origin - self.cp.XAxis * self.xs * 0.5 + self.cp.YAxis * self.ys * 0.5 + self.cp.ZAxis * self.zs
        pt_7 = self.cp.Origin + self.cp.XAxis * self.xs * 0.5 + self.cp.YAxis * self.ys * 0.5 + self.cp.ZAxis * self.zs
        pt_8 = self.cp.Origin + self.cp.XAxis * self.xs * 0.5 - self.cp.YAxis * self.ys * 0.5 + self.cp.ZAxis * self.zs
        rs.AddBox([pt_1,pt_2,pt_3,pt_4,pt_5,pt_6,pt_7,pt_8])

bricks = []
for i in range(10):
    temp_plane = rg.Plane(rg.Point3d(i*300, 0, 0), rg.Vector3d.ZAxis)
    temp_plane.Rotate(m.radians(i*10), temp_plane.ZAxis, temp_plane.Origin)
    bricks.append(Brick(temp_plane))

for i,brick in enumerate(bricks):
    brick.display()
    try:
        print brick.distance_to_other_brick(bricks[i+1])
    except IndexError:
        None

