import os
import pathlib
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment
from object import CLine
from Unitest1_polyline_points import point_list
from Unitest2_detA_sum import detA_sum
from Unitest3_find_horizon_line import find_horizon_line
from Unitest5_draw_cuting_vertical_line import cutting_point

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

        #Step4-3. get detA value of the polygon, which is created by the polyline
        sum_detA = detA_sum(IntPointNum,points).result()

        #Step4-5. get all horizon line in polyline
        horizon_line = find_horizon_line(IntPointNum,points).result()

        #Step4-6. create cutting points
        new_point_list = cutting_point(IntPointNum, points, sum_detA, horizon_line).result()

        #Step4-7. sort cutting points
        new_point_list = sorted(new_point_list, key=lambda x: (x.y, x.x))

        #Step4-8. draw cut horizon line
        new_horizon_line = []
        for i in range(len(new_point_list)-1):
            if new_point_list[i].y == new_point_list[i+1].y:
                new_line = CLine(new_point_list[i],new_point_list[i+1])
                new_horizon_line.append(new_line)
        
        for idx, h in enumerate(new_horizon_line):
            msp.add_line((h.p1.x,h.p1.y), (h.p2.x,h.p2.y), dxfattribs={"layer": "Horizon"})
            
        print(f"___________{LWPOLYLINE}___________")


    #Step5. Save processed file
    file_name_parts = input_file_path.split('.')
    output_file_path = file_name_parts[0] + "_DrawArea.dxf"
    doc.saveas(output_file_path)