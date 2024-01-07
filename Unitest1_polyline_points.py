import os
import pathlib
import ezdxf
from object import CPoint

class point_list():
    def __init__(self, LWP_point:[]):
        self.LWP_point = LWP_point
    
    def result(self):
        points = []
        for inx, p in enumerate(self.LWP_point):
            points.append( CPoint(p[0],p[1]))
        return points


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


    for LWPOLYLINE in msp.query():
        print(f"___________{LWPOLYLINE}___________")
        dxf_points = LWPOLYLINE.get_points()
        points = []

        for inx, p in enumerate(dxf_points):
            points.append( CPoint(p[0],p[1]))
        
        for inx, p in enumerate(points):
            print(p.x)
        print(f"___________{LWPOLYLINE}___________")