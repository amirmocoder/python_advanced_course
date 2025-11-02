# امیرعلی محمدی
# 4011833239
from math import pi
class cylinder:
    def __init__(self,radius,hight):
        self.radius = radius
        self.hight = hight
    def V(self):
        print(f'V is {(pi * self.radius ** 2 * self.hight):.2f}')
    def S(self):
        print(f'S is {((2 * pi * self.radius ** 2 ) + (2 * pi * self.radius * self.hight)):.2f}')
r = float(input('ENTER RADIUS '))
h = float(input('ENTER HIGHT '))
obj1 = cylinder(r, h)
obj1.V()
obj1.S()
