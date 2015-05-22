from scipy import interpolate as interpl
import numpy as np
import os
from pylinac import log_analyzer as lga

class Dyn_to_Dose:
    def __init__(self,my_dir):
        """class to import a folder full of dynalog files for a treatment"""
        self.my_logs = lga.MachineLogs();
        self.flip_fluences = list()
        self.interp_fluences = list()
        
        #TODO more rigorous checking of my_dir
        if not os.path.exists(my_dir):
            self.my_logs.load_dir_UI()
        else:
            self.my_logs.load_dir(my_dir)
            
    def do_calcs(self, res_mm=1.0):
        if len(self.my_logs) == 0:
            print("No valid log files loaded ...")
            return
        for log in self.my_logs:
            log.fluence.actual.calc_map(resolution=res_mm)
            
    def do_flip(self):
        for log in self.my_logs:
            tmp = log.fluence.actual.calc_map(resolution=1.0)
            self.flip_fluences.append(np.flipud(tmp))
            
    def make_interp(self,y_dim, x_dim):
        """y_dim must be 1D array containing co-ords in cms
        for fluence and x_dim 1D array likewise. x is parallel to leaf motion.
        For Varian, -- to ++ is top-left to bottom-right
        """
        flu_y = [-19.5, -18.5, -17.5, -16.5, -15.5, -14.5, -13.5, -12.5, -11.5, -10.5, -9.75, 
         -9.25, -8.75, -8.25, -7.75, -7.25, -6.75, -6.25, -5.75, -5.25, -4.75, -4.25, 
         -3.75, -3.25, -2.75, -2.25, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25,
         1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 
         8.25, 8.75, 9.25, 9.75, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5,
         19.5]
        flu_x = np.linspace(-19.95, 19.95, 400) #TODO get rid of hardcoding dimensions of 1mm res
        
        self.interp_fluences = list() # need to empty out list first
        for flu in self.flip_fluences:
            
            #first create interpolating object tmp
            tmp = interpl.RectBivariateSpline(flu_y, flu_x, flu)
            
            # now create new interpolated fluences and store
            self.interp_fluences.append(tmp(y_dim, x_dim))
            
        
