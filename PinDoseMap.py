import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from scipy import interpolate as interpl
import csv
import os

class PinDoseMap:
    """A class to represent a Pinnacle planar dose map. 
    Attributes: 
    	self.hdr is dictionary of header data
    	self.itrp_dose_array is numpy array of planar dose from Pinnacle
    	
    Assume that maps are at 100cm SPD, and 5cm deep as per local
    dose calc conventions for IMRT QA"""
        # TODO open file once and pass around file handle
    def __init__(self, my_file):
        assert os.path.exists(my_file), "check path you gave is correct and exists: %s" % my_file
        
        self.map_file = my_file
        self.hdr = None		#dictionary of planar dose header params (like pat name)
        self.x_pos = None
        self.y_pos = None
        self.raw_dose_array = None
        self.itrp_dose_array = None
        self.get_hdr(self.map_file)
        self.get_dose_map(self.map_file)
        
    def get_hdr(self, map_file):
        p = dict() 
        
        with open(map_file, "r") as fh:
            
            for line_elems in (x.split(':,') for x in fh.read().split('\n')):
                if line_elems[0] == '':  # empty line marks end of header
                    break
                else:
                    p[line_elems[0]] = line_elems[1]
                    
        self.hdr = p
    
    def get_dose_map(self, map_file):
        rawdat = np.genfromtxt(map_file, delimiter=',', skiprows=11,
                               missing_values='') # skip first 11 rows of header data
        self.y_pos = rawdat[1: ,0] #get everything after first position ([1: )in 1st col ( ,0])   
        self.x_pos = rawdat[0, 1:-1] #in first row ([0, ), get all except first and last ( ,1:-1])
        self.raw_dose_array = rawdat[1:, 1:-1]  # here is the dose array
        my_temp = interpl.RectBivariateSpline(self.y_pos, self.x_pos, self.raw_dose_array)
        self.itrp_dose_array = my_temp(self.y_pos, self.x_pos)
        
    def do_plot(self):
        # TODO check array exists before plotting
        fig = plt.figure(figsize=(6, 3.2))
        ax1 = fig.add_subplot(111)
        ax1.set_title('TestPinFlu')
        plt.imshow(self.itrp_dose_array)
        
        



