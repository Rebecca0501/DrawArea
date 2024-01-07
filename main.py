import os
import pathlib
import ezdxf


if __name__=="__main__":
    print("Hello World")

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


    #Step4. Process every polyline


    #Step5. Save processed file
    file_name_parts = input_file_path.split('.')
    output_file_path = file_name_parts[0] + "_DrawArea.dxf"
    doc.saveas(output_file_path)

