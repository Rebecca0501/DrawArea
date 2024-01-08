import os
import pathlib
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment
from object import CLine
from object import CSqure
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
    # "Area" for rectangle, the color is yellow
    doc.layers.add(name="Area", color=2)
    # "Dimension" for Dimension line, the color is magenta
    doc.layers.add(name="Dimension", color=6)
    # "Vertical" for vertical line, the color is green
    doc.layers.add(name="Vertical", color=3)
    # "PointNumber" for PointNumber label, the color is white
    doc.layers.add(name="PointNumber")


    #Step4. Process every polyline
    for LWPOLYLINE in msp.query():
        print(f"___________{LWPOLYLINE}___________")

        #Step4-1. get point in polyline
        points = point_list(LWPOLYLINE.get_points()).result()

        #Step4-2. add number label on each point
        IntPointNum = len(points)
        if(LWPOLYLINE.is_closed==False):
            IntPointNum -= 1
        # for i in range(IntPointNum):
        #     msp.add_text(i+1,height=40,dxfattribs={"layer": "PointNumber"}).set_placement(
        #         (points[i].x,points[i].y),
        #         align=TextEntityAlignment.MIDDLE_RIGHT
        #     )

        #Step4-3. get detA value of the polygon, which is created by the polyline
        sum_detA = detA_sum(IntPointNum,points).result()

        #Step4-4. add label of 1. clockwise, 2.polygon area, 3. number of point, on the centor of polyline
        # if sum_detA<0:
        #     msp.add_text("clockwise",height=40).set_placement(
        #         (points[0].x,points[0].y),
        #         align=TextEntityAlignment.MIDDLE_RIGHT
        #     )
        # else:
        #     msp.add_text("countorclockwise",height=40).set_placement(
        #         (points[0].x,points[0].y),
        #         align=TextEntityAlignment.MIDDLE_RIGHT
        #     )
        # msp.add_text("Area:"+str(abs(round(sum_detA, 2))),height=40).set_placement(
        #     (points[0].x,points[0].y-100),
        #     align=TextEntityAlignment.MIDDLE_RIGHT
        # )
        # msp.add_text("Point number:"+str(IntPointNum),height=40).set_placement(
        #     (points[0].x,points[0].y-200),
        #     align=TextEntityAlignment.MIDDLE_RIGHT
        # )
        
        #Step4-5. get all horizon line in polyline
        horizon_line = find_horizon_line(IntPointNum,points).result()

        #Step4-6. create cutting points
        new_point_list = cutting_point(IntPointNum, points, sum_detA, horizon_line).result()

        #Step4-7. sort cutting points
        new_point_list = sorted(new_point_list, key=lambda p: (p.y, p.x))

        #Step4-8. draw cut horizon line
        new_horizon_line = []
        for i in range(len(new_point_list)-1):
            if new_point_list[i].y == new_point_list[i+1].y:
                new_line = CLine(new_point_list[i],new_point_list[i+1])
                new_horizon_line.append(new_line)
        
        #Step4-9. sorting cut horizon line
        new_horizon_line = sorted(new_horizon_line, key=lambda p: (p.p1.x, p.p2.x, p.p1.y))
        
        #Step4-10. create rectangle
        rectangle = []
        for i in range(len(new_horizon_line)-1):
            if round(new_horizon_line[i].p1.x,3) == round(new_horizon_line[i+1].p1.x,3) and round(new_horizon_line[i].p2.x,3) == round(new_horizon_line[i+1].p2.x,3):
                new_rectangle = CSqure(new_horizon_line[i],new_horizon_line[i+1])
                rectangle.append(new_rectangle)
        
        for idx, r in enumerate(rectangle):
            corner = r.get_4_point()
            msp.add_lwpolyline(corner, dxfattribs={"layer": "Area"})

            centor = r.get_centor()
            msp.add_text(chr(idx+65),height=40).set_placement(
                (centor.x,centor.y),
                align=TextEntityAlignment.MIDDLE_CENTER
            )

            width = round(abs(r.p1.x-r.p2.x),2)
            heigth = round(abs(r.p2.y-r.p3.y),2)
            msp.add_text(f"{width} x {heigth} = {round(width*heigth,2)}",height=20).set_placement(
                (centor.x,centor.y-40),
                align=TextEntityAlignment.MIDDLE_CENTER
            )

            msp.add_linear_dim(
                base=(r.p3.x, r.p3.y+10),  # location of the dimension line
                p1=(r.p3.x, r.p3.y),  # 1st measurement point
                p2=(r.p4.x, r.p4.y),  # 2nd measurement point
                override={
                    "dimtxsty": "Standard",
                    "dimtxt": 30
                }
            ).render()

            msp.add_aligned_dim(  # location of the dimension line
                p1=(r.p1.x, r.p1.y),  # 1st measurement point
                p2=(r.p4.x, r.p4.y),  # 2nd measurement point
                distance=0,
                override={
                    "dimtxsty": "Standard",
                    "dimtxt": 30
                }
            ).render()
        

        print(f"___________{LWPOLYLINE}___________")


    #Step5. Save processed file
    file_name_parts = input_file_path.split('.')
    output_file_path = file_name_parts[0] + "_DrawArea.dxf"
    doc.saveas(output_file_path)
    

