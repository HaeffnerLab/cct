'''
Analytic derivatives of the solid angle of rectangles.
'''

from sympy import *

class analytic_derivatives():

    def __init__(self, axes_permutation=0):
        x1, x2, y1, y2, x, y, z = symbols('x1 x2 y1 y2 x y z')

        if axes_permutation == 0:
            self.term = ( atan( ((x2 - x)*(y2 - z)) / (y*sqrt( (x2 - x)**2 + (y2 - z)**2 + y**2))) -
                          atan( ((x1 - x)*(y2 - z)) / (y*sqrt( (x1 - x)**2 + (y2 - z)**2 + y**2))) -
                          atan( ((x2 - x)*(y1 - z)) / (y*sqrt( (x2 - x)**2 + (y1 - z)**2 + y**2))) +
                          atan( ((x1 - x)*(y1 - z)) / (y*sqrt( (x1 - x)**2 + (y1 - z)**2 + y**2))) )
            

        if axes_permutation == 1:
            self.term = ( atan( ((x2 - x)*(y2 - y)) / (z*sqrt( (x2 - x)**2 + (y2 - y)**2 + z**2 )) ) -
                          atan( ((x1 - x)*(y2 - y)) / (z*sqrt( (x1 - x)**2 + (y2 - y)**2 + z**2 )) ) -
                          atan( ((x2 - x)*(y1 - y)) / (z*sqrt( (x2 - x)**2 + (y1 - y)**2 + z**2 )) ) +
                          atan( ((x1 - x)*(y1 - y)) / (z*sqrt( (x1 - x)**2 + (y1 - y)**2 + z**2 )) ) )

        self.symbols = [x1, x2, y1, y2, x, y, z]

        self.functions_dict = {}
        self.functions_dict['phi0'] = lambdify(self.symbols, self.term)

        self.first_order()
        self.second_order()
        self.third_order()
        self.fourth_order()

    def first_order(self):

        x1, x2, y1, y2, x, y, z = self.symbols

        self.functions_dict['ddx'] = lambdify(self.symbols, self.term.diff(x))
        self.functions_dict['ddy'] = lambdify(self.symbols, self.term.diff(y))
        self.functions_dict['ddz'] = lambdify(self.symbols, self.term.diff(z))

    def second_order(self):
        x1, x2, y1, y2, x, y, z = self.symbols
        
        self.functions_dict['d2dx2'] = lambdify(self.symbols, self.term.diff(x,2))
        self.functions_dict['d2dy2'] = lambdify(self.symbols, self.term.diff(y,2))
        self.functions_dict['d2dz2'] = lambdify(self.symbols, self.term.diff(z,2))
        self.functions_dict['d2dxdy'] = lambdify(self.symbols, self.term.diff(x,y))
        self.functions_dict['d2dxdz'] = lambdify(self.symbols, self.term.diff(x,z))
        self.functions_dict['d2dydz'] = lambdify(self.symbols, self.term.diff(y,z))

    def third_order(self):
        x1, x2, y1, y2, x, y, z = self.symbols
        
        #self.functions_dict['d3dx3'] = lambdify(self.symbols, self.term.diff(x,3))
        #self.functions_dict['d3dy3'] = lambdify(self.symbols, self.term.diff(y,3))
        self.functions_dict['d3dz3'] = lambdify(self.symbols, self.term.diff(z,3))
        self.functions_dict['d3dxdz2'] = lambdify(self.symbols, self.term.diff(x,z,2))
        self.functions_dict['d3dydz2'] = lambdify(self.symbols, self.term.diff(y,z,2))

    def fourth_order(self):
        x1, x2, y1, y2, x, y, z = self.symbols
        
        #self.functions_dict['d4dx4'] = lambdify(self.symbols, self.term.diff(x,4))
        #self.functions_dict['d4dy4'] = lambdify(self.symbols, self.term.diff(y,4))
        self.functions_dict['d4dz4'] = lambdify(self.symbols, self.term.diff(z,4))
        self.functions_dict['d4dx2dz2'] = lambdify(self.symbols, self.term.diff(x,2,z,2))
        self.functions_dict['d4dy2dz2'] = lambdify(self.symbols, self.term.diff(y,2,z,2))
