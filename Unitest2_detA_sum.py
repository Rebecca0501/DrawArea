import os
import pathlib
import ezdxf
from Unitest1_polyline_points import point_list
import numpy as np
from object import CPointVector
from object import CPoint

class detA_sum():
    def __init__(self, point_num:int, point:[]):
        self.point_num = point_num
        self.point = point
    
    def result(self):
        origin_vector = []
        sum_detA = 0.000
        for i in range(self.point_num):
            vector_i = CPointVector(self.point[i],self.point[0])
            origin_vector.append(vector_i)

        for i in range(len(origin_vector)-1):
            matrix = [[origin_vector[i].vx,origin_vector[i].vy],
                      [origin_vector[i+1].vx,origin_vector[i+1].vy]]
            #print(f"Matrix {i+1} = {matrix}")
            s= np.linalg.det(matrix)*0.5
            sum_detA += s
        return sum_detA
 

if __name__=="__main__":

    #Step1. Get CAD file path
    str_CAD_file_name="example 1.dxf"
    pathInputFilePath=pathlib.Path(os.getcwd())
    pathInputFilePath=pathInputFilePath.joinpath(str_CAD_file_name)
    input_file_path = str(pathInputFilePath)
    print(input_file_path)


    #Step2. Open CAD file and model space
    doc = ezdxf.readfile(input_file_path)
    msp = doc.modelspace()


    #Step4. Process every polyline
    for LWPOLYLINE in msp.query():
        print(f"___________{LWPOLYLINE}___________")

        #Step4-1. get point in polyline
        points = point_list(LWPOLYLINE.get_points()).result()

        #Step4-2. get point in polyline
        sum_detA = 0.000

        IntPointNum = len(points)
        if(LWPOLYLINE.is_closed==False):
            IntPointNum -= 1

        origin_vector = []
        for i in range(IntPointNum):
            vector_i = CPointVector(points[i],points[0])
            origin_vector.append(vector_i)
        
        #for idx, v in enumerate(origin_vector):
            #print(f"X_vector = {v.vx} ; Y_vector = {v.vy}")

        for i in range(len(origin_vector)-1):
            matrix = [[origin_vector[i].vx,origin_vector[i].vy],
                      [origin_vector[i+1].vx,origin_vector[i+1].vy]]
            #print(f"Matrix {i+1} = {matrix}")
            s= np.linalg.det(matrix)*0.5
            sum_detA += s
        print(f"sum of detA = {sum_detA}")
        print(f"___________{LWPOLYLINE}___________")
