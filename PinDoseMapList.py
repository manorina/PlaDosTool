from pylinac.core import io as io
import PinDoseMap as pdm
import os

class PinDoseMapList:

	"""A wrapper class to hold PinDoseMap objects as a list.
	Intended to use for planar dose maps from Pinnacle for IMRT QA
    
	INPUT: 
	my_dir		: full path to desired folder (optional)"""
	
	def __init__(self, my_dir=''):
		self.pin_dose_folder = None
		self.pdm_list = list()
    
		if my_dir != '':
			if os.path.exists(my_dir):
				print ("Entries:\n=======\n\n")
                
				for f in os.listdir(my_dir):
					print("entry: %s" % f)
					
				self.populate_list(my_dir)
			else:
				print ("check this path exists: %s" % my_dir)
		else:
			self.pin_dose_folder = io.get_folder_UI()
			print("Pinnacle planar dose folder is %s" % self.pin_dose_folder)
			self.populate_list(self.pin_dose_folder)
		

        
	def populate_list(self, folder):
		missed = 0
		for f in os.listdir(folder):
			with open(os.path.join(folder, f), "r") as fh:
				if "Version" in fh.readline(): #"Version" in first line
											   # marks a Pinnacle Planar dose text file -
											   # only append these files to our list 
					g = self.get_G_Ang(f)
					x = pdm.PinDoseMap(os.path.join(folder,f), g)
					self.pdm_list.append(x)
					print('File is: {0} and gant is {1}'.format(f, g))
				else:
					missed+=1
					
				print("Skipped %d files. If non-zero, check the Pinnacle planar dose folder" % missed)
				
	def get_G_Ang(self, map_file):
		tmp = map_file.split('_') #FIXME poor implementation - requires angle to be in filenam
		print (tmp[1])
		return tmp[1]
            
