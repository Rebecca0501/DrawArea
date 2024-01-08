import os
import pathlib
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment
from Unitest1_polyline_points import point_list
from Unitest2_detA_sum import detA_sum
from Unitest3_find_horizon_line import find_horizon_line
from object import CPointVector
from object import CPoint

class cutting_point():
    def __init__(self, point_num:int, point:[], sum_detA: float, horizon_line:[]):
        self.point_num = point_num
        self.point = point
        self.sum_detA = sum_detA
        self.horizon_line = horizon_line
    
    def result(self):
        new_point_list = self.point[:] 
        for i in range(self.point_num):
            pi_before = CPoint(0.000,0.000)
            pi = CPoint(0.000,0.000)
            pi_after = CPoint(0.000,0.000)
            if i ==0:
                pi_before = self.point[self.point_num-1]
                pi = self.point[i]
                pi_after = self.point[i+1]
            elif i < self.point_num-1:
                pi_before = self.point[i-1]
                pi = self.point[i]
                pi_after = self.point[i+1]
            else:
                pi_before = self.point[i-1]
                pi = self.point[i]
                pi_after = self.point[0]

            v1 = CPointVector(pi_before,pi)
            v2 = CPointVector(pi,pi_after)
            matrix = [[v1.vx,v1.vy],
                      [v2.vx,v2.vy]]
            s= np.linalg.det(matrix)*0.5

            #when det(A)<0 the point order is clockwise, s of concave corner will>0
            #when det(A)>0 the point order is counterclockwise, s of concave corner will<0
            if self.sum_detA*s<0:  
                if abs(v1.vy)>abs(v2.vy):
                    if pi_before.y>pi.y:
                        for idx, h in enumerate(self.horizon_line):
                            if(h.p1.y< pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
                    else:
                        for idx, h in enumerate(self.horizon_line):
                            if(h.p1.y> pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
                else:
                    if pi_after.y>pi.y:
                        for idx, h in enumerate(self.horizon_line):
                            if(h.p1.y< pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
                    else:
                        for idx, h in enumerate(self.horizon_line):
                            if(h.p1.y> pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break

        return new_point_list


if __name__=="__main__":

    #Step1. Get CAD file path
    #input_file_path = input("请输入CAD文件的路径：")
    str_CAD_file_name="example 1.dxf"
    pathInputFilePath=pathlib.Path(os.getcwd())
    pathInputFilePath=pathInputFilePath.joinpath(str_CAD_file_name)
    input_file_path = str(pathInputFilePath)
    print(input_file_path)


    #Step2. Open CAD file and model space
    doc = ezdxf.readfile(input_file_path)
    msp = doc.modelspace()

    #Step3. Create new layers
    # "allpoint" for allpoint, the color is red
    doc.layers.add(name="allpoint", color=1)

    #Step4. Process every polyline
    for LWPOLYLINE in msp.query():
        print(f"___________{LWPOLYLINE}___________")

        #Step4-1. get point in polyline
        points = point_list(LWPOLYLINE.get_points()).result()

        #Step4-2. add number label on each point
        IntPointNum = len(points)
        if(LWPOLYLINE.is_closed==False):
            IntPointNum -= 1
        for i in range(IntPointNum):
            msp.add_text(i+1,height=40,dxfattribs={"layer": "PointNumber"}).set_placement(
                (points[i].x,points[i].y),
                align=TextEntityAlignment.MIDDLE_RIGHT
            )

        #Step4-3. get detA value of the polygon, which is created by the polyline
        sum_detA = detA_sum(IntPointNum,points).result()

        #Step4-5. get all horizon line in polyline
        horizon_line = find_horizon_line(IntPointNum,points).result()
        for idx, h in enumerate(horizon_line):
            msp.add_line((h.p1.x, h.p1.y), (h.p2.x, h.p2.y), dxfattribs={"layer": "Horizon"})

        #Step4-6. using freeman chain code concept to find concave corner
        
        #copy all elements in points to new list
        new_point_list = points[:] 

        for i in range(IntPointNum):
            pi_before = CPoint(0.000,0.000)
            pi = CPoint(0.000,0.000)
            pi_after = CPoint(0.000,0.000)
            if i ==0:
                pi_before = points[IntPointNum-1]
                pi = points[i]
                pi_after = points[i+1]
            elif i < IntPointNum-1:
                pi_before = points[i-1]
                pi = points[i]
                pi_after = points[i+1]
            else:
                pi_before = points[i-1]
                pi = points[i]
                pi_after = points[0]

            v1 = CPointVector(pi_before,pi)
            v2 = CPointVector(pi,pi_after)
            matrix = [[v1.vx,v1.vy],
                      [v2.vx,v2.vy]]
            s= np.linalg.det(matrix)*0.5

            #when det(A)<0 the point order is clockwise, s of concave corner will>0
            #when det(A)>0 the point order is counterclockwise, s of concave corner will<0
            if sum_detA*s<0:  
                if abs(v1.vy)>abs(v2.vy):
                    if pi_before.y>pi.y:
                        for idx, h in enumerate(horizon_line):
                            if(h.p1.y< pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
                    else:
                        for idx, h in enumerate(horizon_line):
                            if(h.p1.y> pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
                else:
                    if pi_after.y>pi.y:
                        for idx, h in enumerate(horizon_line):
                            if(h.p1.y< pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
                    else:
                        for idx, h in enumerate(horizon_line):
                            if(h.p1.y> pi.y and h.p1.x< pi.x and h.p2.x >pi.x):
                                point_new = CPoint(pi.x,h.p1.y)
                                new_point_list.append(point_new)
                                break
        
        for idx, p in enumerate(new_point_list):
            msp.add_circle((p.x, p.y), radius=10, dxfattribs={"layer": "allpoint"})
                            
                        


        print(f"___________{LWPOLYLINE}___________")
    
    
    #Step5. Save processed file
    print("Step5")
    file_name_parts = input_file_path.split('.')
    output_file_path = file_name_parts[0] + "_DrawArea.dxf"
    doc.saveas(output_file_path)
