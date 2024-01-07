import os
import pathlib
import ezdxf
from ezdxf.enums import TextEntityAlignment
from Unitest1_polyline_points import point_list
from Unitest2_detA_sum import detA_sum
from Unitest3_find_horizon_line import find_horizon_line

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
    # "Horizon" for horizon line, the color is magenta
    doc.layers.add(name="Horizon", color=6)
    # "Vertical" for vertical line, the color is green
    doc.layers.add(name="Vertical", color=3)
    # "PointNumber" for PointNumber label, the color is white
    doc.layers.add(name="PointNumber")


    #Step4. Process every polyline
    for LWPOLYLINE in msp.query():
        print(LWPOLYLINE)

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

        #Step4-3. get point in polyline
        sum_detA = detA_sum(IntPointNum,points).result()

        #Step4-4. add label of 1. clockwise, 2.polygon area, 3. number of point, on the centor of polyline
        if sum_detA<0:
            msp.add_text("clockwise",height=40).set_placement(
                (points[0].x,points[0].y),
                align=TextEntityAlignment.MIDDLE_RIGHT
            )
        else:
            msp.add_text("countorclockwise",height=40).set_placement(
                (points[0].x,points[0].y),
                align=TextEntityAlignment.MIDDLE_RIGHT
            )
        msp.add_text("Area:"+str(abs(round(sum_detA, 2))),height=40).set_placement(
            (points[0].x,points[0].y-100),
            align=TextEntityAlignment.MIDDLE_RIGHT
        )
        msp.add_text("Point number:"+str(IntPointNum),height=40).set_placement(
            (points[0].x,points[0].y-200),
            align=TextEntityAlignment.MIDDLE_RIGHT
        )
        
        #Step4-5. get all horizon line in polyline
        horizon_line = find_horizon_line(IntPointNum,points).result()
        for idx, h in enumerate(horizon_line):
            msp.add_line((h.p1.x, h.p1.y), (h.p2.x, h.p2.y), dxfattribs={"layer": "Horizon"})


    #Step5. Save processed file
    print("Step5")
    file_name_parts = input_file_path.split('.')
    output_file_path = file_name_parts[0] + "_DrawArea.dxf"
    doc.saveas(output_file_path)
    

