import os
import pathlib
import ezdxf
from Unitest1_polyline_points import point_list
from object import CLine


class find_horizon_line():
    def __init__(self, point_num:int, point:[]):
        self.point_num = point_num
        self.point = point
    
    def result(self):
        horizon_line = []
        for i in range(self.point_num):
            if i < self.point_num-1:
                if CLine(self.point[i],self.point[i+1]).is_horizon():
                    if self.point[i].x < self.point[i+1].x:
                        horizon_line.append(CLine(self.point[i],self.point[i+1]))
                    else:
                        horizon_line.append(CLine(self.point[i+1],self.point[i]))
            else:
                if CLine(self.point[i],self.point[0]).is_horizon():
                    if self.point[i].x < self.point[0].x:
                        horizon_line.append(CLine(self.point[i],self.point[0]))
                    else:
                        horizon_line.append(CLine(self.point[0],self.point[i]))
        
        
        return horizon_line
    

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
    # "Horizon" for horizon line, the color is magenta
    doc.layers.add(name="Horizon", color=6)

    #Step4. Process every polyline
    for LWPOLYLINE in msp.query():
        print(f"___________{LWPOLYLINE}___________")

        #Step4-1. get point in polyline
        points = point_list(LWPOLYLINE.get_points()).result()

        #Step4-2. add number label on each point
        IntPointNum = len(points)
        if(LWPOLYLINE.is_closed==False):
            IntPointNum -= 1

        #Step4-5. get all horizon line in polyline
        horizon_line = []
        for i in range(IntPointNum):
            if i < IntPointNum-1:
                if CLine(points[i],points[i+1]).is_horizon():
                    horizon_line.append(CLine(points[i],points[i+1]))
            else:
                if CLine(points[i],points[0]).is_horizon():
                    horizon_line.append(CLine(points[i],points[0]))
        
        for idx, h in enumerate(horizon_line):
            msp.add_line((h.p1.x,h.p1.y), (h.p2.x,h.p2.y), dxfattribs={"layer": "Horizon"})
            #print(f"horizon line {idx+1}=> p1:{h.p1}; p2:{h.p1}")

        print(f"___________{LWPOLYLINE}___________")

    #Step5. Save processed file
    file_name_parts = input_file_path.split('.')
    output_file_path = file_name_parts[0] + "_DrawArea.dxf"
    doc.saveas(output_file_path)