import math

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.w=x2-x1+1
        self.h=y2-y1+1

    def centre(self):
        return (int((self.x1+self.x2)/2), int((self.y1+self.y2)/2))

    def intersect(self, ref):
        return (self.x1<=ref.x2 and self.x2>=ref.x1 and self.y1<=ref.y2 and self.y2>=ref.y1)

def distance_chebyshev(x1, y1, x2, y2):
    return max(abs(x2-x1), abs(y2-y1))

def distance_euclidian(x1, y1, x2, y2):
    return math.sqrt(float((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)))