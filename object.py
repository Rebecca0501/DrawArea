class CPoint():
    def __init__(self, x:float, y:float):
        self.x=x
        self.y=y

    def __str__(self):
        return f"x:{self.x}, y:{self.y}"

    def add(self, p2):
        return CPoint(self.x+p2.x, self.y+p2.y)

    def sub(self, p2):
        return CPoint(self.x-p2.x, self.y- p2.y)


class CLine():
    def __init__(self, p1:CPoint, p2:CPoint):
        self.p1=p1
        self.p2=p2

    def getLength(self):
        return  pow(self.p1.x - self.p2.x, 2 ) +pow(self) 

    def __str__(self):
        return f"Line: [{self.p1}, {self.p2}]"
    
    def is_horizon(self):
        x = round(abs(self.p1.x - self.p2.x),2)
        y = round(abs(self.p1.y - self.p2.y),2)
        if x >0 and y==0:
            return True

class CSqure():
    def __init__(self, line1:CLine, line2:CLine):
        self.l1=line1
        self.l2=line2
        self.p1 = line1.p1
        self.p2 = line1.p2
        self.p3 = line2.p2
        self.p4 = line2.p1

    def get_4_point(self):
        squre_points = [(self.p1.x,self.p1.y),(self.p2.x,self.p2.y),(self.p3.x,self.p3.y),(self.p4.x,self.p4.y),(self.p1.x,self.p1.y)]
        return squre_points
    
    def get_centor(self):
        centor_x = (self.p1.x+self.p3.x)/2
        centor_y = (self.p1.y+self.p3.y)/2
        centor = CPoint(centor_x,centor_y)
        return centor



class CPointVector():
    def __init__(self, p0=CPoint(0,0), p1=CPoint(1,1)):
        self.vx = p1.x-p0.x
        self.vy = p1.y-p0.y

    def __str__(self):
        return f"Vector: [{self.vx}, {self.vy}]"



if __name__=="__main__":
    pointA=CPoint(2.72,3.85)
    pointB=CPoint(6.05,4.12)
    pointC= pointA.add(pointB)
    print(pointC)

    vector1 = CPointVector(pointA,pointB)
    print(vector1)